# pylint: disable=no-member,too-many-locals
import datetime

from django import http
from django.db import models as orm
from django.conf import settings
from django.utils import timezone

from constance import config

from apply import constants
from apply import exceptions
from apply import models
from apply import filters
from job import models as job_models
from job import services as job_services
from leet import enums
from leet import services as base_services
from leet import models as base_models
from log import constants as log_constants
from log import utils as log_utils


def filter_jobs_by_title(queryset, value):
    """Filter jobs by title.
    This method used for interactive searching
        and calculating of count jobs in autoapply"""
    return queryset.filter(
        orm.Q(title__icontains=value)
        |
        orm.Q(company__name__icontains=value)
    )


def filter_jobs_by_location(queryset, state_id, city_id):
    """Filter jobs by location.
    This method used for interactive searching
        and calculating of count jobs in autoapply"""
    return queryset.filter(
        orm.Q(location__city__state_id=state_id)
        |
        orm.Q(location__city_id=city_id)
    )


def exclude_jobs(queryset, value):
    """Exclude some jobs from list of jobs.
    This method used for interactive searching
    and calculating of count jobs in autoapply"""
    return queryset.exclude(id__in=value)


def get_job_seeker_applied_jobs(job_seeker):
    """
    Returns job with applied_at date that user's been applied for.
    """
    qs = job_models.Job.objects.get_all_with_relations().filter(
        applies__owner=job_seeker,
        applies__status=enums.ApplyStatusEnum.APPLIED.name
    ).annotate(
        applied_at=orm.F('applies__applied_at')
    )
    return qs


def get_autoapply_days_to_completion(autoapply):
    """
    Returns number of days that left to autoapply end. For not in progress
    autoapplies returns None.
    """
    if autoapply.status == enums.AutoapplyStatusEnum.IN_PROGRESS.name:
        period_length = config.AUTOAPPLY_PERIOD_LENGTH
        end_date = autoapply.started_at.date() + datetime.timedelta(
            days=period_length)
        now = timezone.now().date()
        time_left = end_date - now
        return time_left.days if time_left.days >= 0 else 0
    return None


def get_autoapply_new_jobs_count(autoapply):
    """
    Returns count of jobs that was founded for autoapply and that
    user hasn't seen by job seeker.
    """
    # legacy?
    return autoapply.apply_set.filter(
        status=enums.ApplyStatusEnum.NEW.name
    ).count()


class ApplyService:

    job_published_qs = job_models.Job.objects.get_published()
    job_qs = job_models.Job.objects.get_all_with_relations()

    def __init__(self, job_seeker):
        self.job_seeker = job_seeker

    def add_job_seeker_to_candidates(self, job, apply):
        status = base_models.CandidateStatus.get_applied_status()
        candidate, created = self.job_seeker.candidate_set.update_or_create(
            job=job,
            status=status,
            defaults={
                'apply': apply,
            }
        )
        if created:
            # when job_seeker was assigned as candidate to job
            # and than was rejected and than he applied to the job
            # save rejected candidate created_at as previous_applied_date
            (self.job_seeker
                 .candidate_set
                 .exclude(status=status)
                 .update(previous_applied_date=orm.F('created_at')))
            # create step in candidate workflow with applied status's step
            candidate.workflow_steps.create(status=status)


class AutoapplyService(ApplyService):

    def __init__(self, job_seeker, autoapply=None):
        super().__init__(job_seeker)
        self.autoapply = autoapply

    def get_autoapply_jobs(self):
        jobs = self.job_published_qs
        if self.autoapply:
            aa_status = self.autoapply.status
            if aa_status == enums.AutoapplyStatusEnum.SAVED.name:
                # For saved autoapply it's needed to return all jobs excluding
                # deleted and already applied or need review jobs.
                deleted_jobs_ids = self.autoapply.deleted_jobs.values_list(
                    'id', flat=True
                )
                jobs = exclude_jobs(jobs, deleted_jobs_ids)
                jobs = self.exclude_js_applied_or_need_review_jobs(jobs)
                # filter by query params
                jobs = self.filter_jobs_by_autoapply_query_params(jobs)
            else:
                # For in progress autoapply it's needed to update autoapply
                # job list.
                if aa_status == enums.AutoapplyStatusEnum.IN_PROGRESS.name:
                    jobs_to_apply = self.actualize_autoapply_jobs_list()
                    self.autoapply_to_jobs(jobs_to_apply)
                jobs = self.autoapply.jobs.get_all_with_relations()
        else:
            # For the new autoapply it's needed to return all jobs excluding
            # jobs that job seeker's already applied for or need review
            jobs = self.exclude_js_applied_or_need_review_jobs(jobs)
        jobs = self.filter_jobs_by_position(jobs)
        jobs = self.annotate_jobs_with_apply_statuses(jobs)
        jobs = self.annotate_jobs_with_matching_criteria(jobs)
        jobs = self.order_autoapply_jobs(jobs)
        return jobs

    def filter_jobs_by_position(self, jobs):
        position = self.job_seeker.position_type
        return jobs.filter(position_type=position)

    def filter_jobs_by_autoapply_query_params(self, jobs):
        # TODO (i.bogretsov) give parsed params to init of AutoapplyService
        query_params = http.QueryDict(self.autoapply.query_params)
        request = http.HttpRequest()
        request.GET = query_params
        # state_id = query_params.get('state_id')
        # city_id = query_params.get('city_id')
        title = query_params.get('search')
        if title:
            jobs = filter_jobs_by_title(jobs, title)
        aa_filter = filters.AutoapplyJobFilter(query_params, jobs)
        jobs = aa_filter.qs
        # if state_id or city_id:
        #     jobs = filter_jobs_by_location(jobs, state_id, city_id)
        return jobs

    def start_autoapply(self, jobs):
        applies = self.autoapply_to_jobs(jobs)
        if len(applies) < self.autoapply.number:
            self.autoapply.started_at = timezone.now()
            self.autoapply.status = enums.AutoapplyStatusEnum.IN_PROGRESS.name
        else:
            self.autoapply.status = enums.AutoapplyStatusEnum.FINISHED.name
            self.autoapply.finished_at = timezone.now()
        self.autoapply.save()
        return self.autoapply

    def autoapply_to_jobs(self, jobs):
        cover_letter = self.job_seeker.cover_letters.filter(
            is_default=True).first()
        jobs_qs_to_apply = self.job_qs.filter(id__in=[job.id for job in jobs])
        jobs_qs_to_apply.exclude(id__in=self.get_job_seeker_applied_jobs())
        jobs = self.annotate_jobs_with_matching_criteria(jobs_qs_to_apply)
        ready_for_apply_jobs = jobs.filter(
            is_clearance_match=True,
            is_required_skills_match=True,
            is_education_match=True,
            is_questionnaire_answered=True,
        )
        if (ready_for_apply_jobs.filter(is_cover_letter_required=True)
                and not cover_letter):
            ready_for_apply_jobs = ready_for_apply_jobs.exclude(
                is_cover_letter_required=True
            )
        need_review_jobs = jobs.exclude(
            id__in=[job.id for job in ready_for_apply_jobs])
        applied_jobs_data = [{
            'job': job,
            'status': enums.ApplyStatusEnum.APPLIED.name,
            'applied_at': timezone.now()
        } for job in ready_for_apply_jobs]
        need_review_jobs_data = [{
            'job': job,
            'status': enums.ApplyStatusEnum.NEED_REVIEW.name
        } for job in need_review_jobs]
        data = (applied_jobs_data + need_review_jobs_data)
        applies = []
        for d in data:
            apply_cover_letter = (
                cover_letter
                if d['job'].is_cover_letter_required
                else None)
            apply, _ = self.job_seeker.applies.update_or_create(
                job=d['job'],
                autoapply=self.autoapply,
                defaults={
                    'status': d['status'],
                    'applied_at': d.get('applied_at'),
                    'cover_letter': apply_cover_letter
                }
            )

            if d['status'] == enums.ApplyStatusEnum.APPLIED.name:
                self.add_job_seeker_to_candidates(d['job'], apply)
                create_apply_log(self.job_seeker, d['job'])

            applies.append(apply)
        return applies

    def autoapply_to_job(self, job):
        job_qs = self.job_qs.filter(id=job.id)
        job_qs = self.annotate_jobs_with_matching_criteria(job_qs)
        job_qs = self.annotate_jobs_with_apply_statuses(job_qs)
        job = job_qs[0]
        can_apply = all((
            job.is_clearance_match,
            job.is_required_skills_match,
            job.is_education_match,
            job.is_questionnaire_answered,
            job.is_cover_letter_provided or not job.is_cover_letter_required
        ))
        status = enums.ApplyStatusEnum.NEED_REVIEW.name
        applied_date = None

        if can_apply:
            status = enums.ApplyStatusEnum.APPLIED.name
            applied_date = timezone.now()

        defaults = {
            'autoapply': self.autoapply,
            'status': status,
            'applied_at': applied_date,
        }
        apply, _ = self.job_seeker.applies.update_or_create(
            job=job,
            defaults=defaults)

        if can_apply:
            self.add_job_seeker_to_candidates(job, apply)
            create_apply_log(self.job_seeker, job)

        return apply

    def annotate_jobs_with_matching_criteria(self, jobs_qs):
        """Annotates Jobs with criteria, that's needed for autoapply"""
        js_skills = self.job_seeker.skills.all()
        allowed_education = job_services.get_allowed_educations_list(
            self.job_seeker.education
        )

        is_clearance_match = orm.Case(
            orm.When(
                orm.Q(clearance__lte=self.job_seeker.clearance)
                |
                orm.Q(clearance=enums.ClearanceTypesEnum.NO_CLEARANCE.name),
                then=True
            ),
            default=False, output_field=orm.BooleanField()
        )
        is_education_match = orm.Case(
            orm.When(
                (orm.Q(education_strict=True) &
                 orm.Q(education__in=allowed_education)) |
                orm.Q(education_strict=False), then=True
            ), default=False, output_field=orm.BooleanField()
        )
        is_questionnaire_answered = orm.Case(
            orm.When(
                ~orm.Q(questions=None)
                &
                ~orm.Q(answers__owner=self.job_seeker),
                then=False
            ),
            default=True, output_field=orm.BooleanField(),
            distinct=True
        )
        matched_required_skills_count = orm.Count(
            'job_skill_set',
            filter=orm.Q(job_skill_set__skill__in=js_skills,
                         job_skill_set__is_required=True),
            distinct=True
        )
        all_required_skills_count = orm.Count(
            'job_skill_set',
            filter=orm.Q(job_skill_set__is_required=True),
            distinct=True
        )
        is_required_skills_match = orm.Case(
            orm.When(
                orm.Q(matching_percent__gte=orm.F('autoapply_minimal_percent'))
                |
                orm.Q(all_required_skills_count=0),
                then=True
            ), default=False, output_field=orm.BooleanField()
        )
        is_cover_letter_provided = orm.Case(
            orm.When(
                ~orm.Q(applies__cover_letter=None)
                &
                orm.Q(applies__autoapply=self.autoapply),
                then=True), default=False, output_field=orm.BooleanField()
        )
        jobs = base_services.annotate_jobs_with_matching_percent(
            self.job_seeker, jobs_qs)
        jobs = jobs.annotate(
            is_clearance_match=is_clearance_match,
            all_required_skills_count=all_required_skills_count,
            matched_required_skills_count=matched_required_skills_count,
            is_required_skills_match=is_required_skills_match,
            is_education_match=is_education_match,
            is_questionnaire_answered=is_questionnaire_answered,
            is_cover_letter_provided=is_cover_letter_provided,
        )
        return jobs

    @staticmethod
    def order_autoapply_jobs(qs):
        qs = qs.annotate(
            apply_status_order=orm.Case(
                orm.When(
                    orm.Q(
                        apply_job_status=enums.ApplyStatusEnum.NEW.name
                    ),
                    then=orm.Value(0)
                ), output_field=orm.IntegerField(), default=orm.Value(1)
            )
        ).order_by('-matching_percent', 'apply_status_order', 'created_at')
        return qs

    def annotate_jobs_with_apply_statuses(self, jobs_qs):
        is_current_autoapply_condition = (
            orm.Q(applies__autoapply__isnull=False)
            &
            orm.Q(applies__autoapply=self.autoapply)
        )
        apply_job_status = orm.Case(
            orm.When(
                is_current_autoapply_condition,
                then=orm.F('applies__status')), default=None
        )
        applied_at = orm.Case(
            orm.When(
                is_current_autoapply_condition,
                then=orm.F('applies__applied_at')), default=None
        )
        jobs = jobs_qs.annotate(
            apply_job_status=apply_job_status,
            applied_at=applied_at
        )
        return jobs

    def actualize_autoapply_jobs_list(self):
        """
        Finds new job for autoapply and delete outdated (doesn't fit to
        autoapply criteria anymore or were applied).
        return: queryset with jobs to apply
        """
        js_jobs = self.get_job_seeker_applied_jobs()
        actual_jobs = self.get_actual_jobs(self.job_published_qs, js_jobs)
        outdated_jobs = self.autoapply.jobs.exclude(pk__in=actual_jobs)
        self.remove_outdated_jobs(outdated_jobs)
        existing_jobs = self.autoapply.jobs.all()
        new_jobs = actual_jobs.exclude(pk__in=existing_jobs)
        new_jobs = self.cut_off_excess_jobs(new_jobs)
        data = [{
            'owner': self.job_seeker,
            'job': j,
            'autoapply': self.autoapply,
            'status': enums.ApplyStatusEnum.NEW.name
        } for j in new_jobs]
        self.job_seeker.applies.bulk_create(models.Apply(**i) for i in data)
        jobs_to_apply = job_models.Job.objects.filter(
            orm.Q(autoapply=self.autoapply) &
            (orm.Q(applies__status=enums.ApplyStatusEnum.NEW.name) |
             orm.Q(applies__status=enums.ApplyStatusEnum.VIEWED.name))
        )
        return jobs_to_apply

    def cut_off_excess_jobs(self, jobs):
        aa_number = self.autoapply.number
        existing_jobs_number = self.autoapply.jobs.count()
        free_jobs_number = aa_number - existing_jobs_number
        if free_jobs_number < jobs.count():
            jobs = jobs[:free_jobs_number]
        return jobs

    def get_job_seeker_applied_jobs(self):
        qs = self.job_qs.filter(
            applies__owner=self.job_seeker,
            applies__status__in=constants.APPLIED_OR_NEED_REVIEW
        )
        return qs

    def get_actual_jobs(self, all_jobs, job_seeker_jobs):

        deleted_job_ids = self.autoapply.deleted_jobs.values_list(
            'id', flat=True
        )
        actual_jobs = all_jobs.filter(
            ~orm.Q(id__in=deleted_job_ids)
            |
            ~orm.Q(id__in=job_seeker_jobs)
        )
        actual_jobs = self.filter_jobs_by_autoapply_query_params(actual_jobs)
        actual_jobs = self.filter_jobs_by_position(actual_jobs)
        actual_jobs = actual_jobs.exclude(
            orm.Q(applies__owner=self.job_seeker)
            &
            (
                ~orm.Q(applies__autoapply=self.autoapply)
                |
                orm.Q(applies__autoapply__isnull=True)
            )
            &
            orm.Q(applies__status__in=constants.APPLIED_OR_NEED_REVIEW)
        )

        return actual_jobs

    def remove_outdated_jobs(self, outdated_jobs):
        self.autoapply.apply_set.filter(
            orm.Q(job__in=outdated_jobs)
            &
            ~orm.Q(status__in=constants.APPLIED_OR_NEED_REVIEW)
        ).delete()

    def delete_autoapply(self):
        if self.autoapply.status != enums.AutoapplyStatusEnum.SAVED.name:
            self.autoapply.apply_set.filter(
                ~orm.Q(status=enums.ApplyStatusEnum.APPLIED.name)
            ).delete()
        self.autoapply.delete()

    def stop_autoapply(self):
        if self.is_autoapply_available_to_stop():
            self.autoapply.status = enums.AutoapplyStatusEnum.STOPPED.name
            self.autoapply.finished_at = timezone.now()
            self.autoapply.save()
        else:
            raise exceptions.ApplyException(
                constants.IMPOSSIBLE_TO_STOP_NOT_IN_PROGRESS_AUTOAPPLY_ERROR
            )
        return self.autoapply

    def restart_autoapply(self):
        if self.is_autoapply_available_to_restart():
            self.autoapply.status = enums.AutoapplyStatusEnum.IN_PROGRESS.name
            self.autoapply.started_at = timezone.now()
            self.autoapply.save()
        else:
            raise exceptions.ApplyException(
                constants.IMPOSSIBLE_TO_RESTART_AUTOAPPLY_ERROR
            )
        return self.autoapply

    def is_autoapply_available_to_stop(self):
        return (self.autoapply.status ==
                enums.AutoapplyStatusEnum.IN_PROGRESS.name)

    def is_autoapply_available_to_restart(self):
        return (self.autoapply.status in [
            enums.AutoapplyStatusEnum.FINISHED.name,
            enums.AutoapplyStatusEnum.STOPPED.name
        ] and self.autoapply.number > self.autoapply.jobs.count())

    def exclude_js_applied_or_need_review_jobs(self, jobs_qs):
        jobs_qs = jobs_qs.exclude(
            applies__owner=self.job_seeker,
            applies__status__in=constants.APPLIED_OR_NEED_REVIEW
        )
        return jobs_qs


class ManualApplyService(ApplyService):

    def __init__(self, job_seeker, job, cover_letter):
        super().__init__(job_seeker)
        self.job = job
        self.cover_letter = (
            cover_letter if job.is_cover_letter_required else None
        )

    def apply_to_job(self):
        """
        Create apply instance for the job by job_seeker
        and add job_seeker to candidates.
        """
        defaults = {
            'applied_at': timezone.now(),
            'status': enums.ApplyStatusEnum.APPLIED.name,
            'autoapply': None,
            'cover_letter': self.cover_letter
        }
        apply, _ = self.job_seeker.applies.get_or_create(
            job=self.job,
            defaults=defaults)

        self.add_job_seeker_to_candidates(self.job, apply)
        create_apply_log(self.job_seeker, self.job)
        return apply


def get_autoapplies_for_notification(notification_type, timedelta):
    """
    Returns autoapply queryset that contains in progress
    autoapplies or autoapplies that were finished not
    earlier than 1 day ago
    """
    autoapplies = models.Autoapply.objects.select_related(
        'owner__user'
    ).filter(
        orm.Q(status=enums.AutoapplyStatusEnum.IN_PROGRESS.name)
        |
        orm.Q(
            status__in=[enums.AutoapplyStatusEnum.STOPPED.name,
                        enums.AutoapplyStatusEnum.FINISHED.name],
            finished_at__gte=timedelta)
    ).annotate(
        applied_job_cnt=orm.Count(
            'apply',
            filter=orm.Q(apply__status=enums.ApplyStatusEnum.APPLIED.name)
        ),
        need_review_job_cnt=orm.Count(
            'apply',
            filter=orm.Q(apply__status=enums.ApplyStatusEnum.NEED_REVIEW.name)
        ),
        viewed_job_cnt=orm.Count(
            'apply',
            filter=orm.Q(apply__status=enums.ApplyStatusEnum.VIEWED.name)
        )
    ).order_by('owner')
    autoapplies = autoapplies.filter(
        owner__user__subscribed_notifications__id=notification_type.id
    )
    return autoapplies


def reapply_to_job(job_seeker, job, apply, cover_letter):
    """
    Update apply's applied date and cover_letter info.
    If candidate is not rejected and reapplies than just update
        previous applied date.
    Else
        If rejected than create new candidate instance with new workflow
    """
    previous_date = apply.applied_at
    apply.applied_at = timezone.now()
    apply.cover_letter = cover_letter
    apply.save()
    rejected_status = base_models.CandidateStatus.get_rejected_status()
    applied_status = base_models.CandidateStatus.get_applied_status()
    # get only active (not rejected) candidates
    candidates_qs = (job_seeker.candidate_set
                               .filter(apply=apply)
                               .exclude(
                                   workflow_steps__status=rejected_status
                               ))
    if candidates_qs.exists():
        candidates_qs.update(previous_applied_date=previous_date)
    else:
        candidate = candidates_qs.create(
            job_seeker=job_seeker,
            job=job,
            apply=apply,
            status=applied_status)
        candidate.workflow_steps.create(status=applied_status)
        # update previous applied date in last rejected candidate
        last_rejected = (job_seeker
                         .candidate_set
                         .filter(
                             apply=apply,
                             workflow_steps__status=rejected_status)
                         .order_by('-created_at'))[:1][0]
        last_rejected.previous_applied_date = previous_date
        last_rejected.save()
    create_apply_log(job_seeker, job)
    return apply


def are_js_required_skills_matched(job_seeker, job):
    job_skills = job.job_skill_set.values('skill__id', 'is_required')
    candidate_skills = set(job_seeker.skills.values_list('id', flat=True))
    required_skills = [
        sk['skill__id'] for sk in job_skills if sk['is_required']
    ]

    for sk in required_skills:
        if sk not in candidate_skills:
            return False
    return True


def create_apply_log(job_seeker, job):
    log_type = log_constants.LogEnum.candidate_apply.name
    log_message = log_constants.LogEnum.candidate_apply.value.format(job.title)
    log_utils.create_log(
        job_seeker.user,
        log_type,
        log_message,
        job_seeker,
        job_company=job.company)


def get_auto_applies_stats(user):
    number_of_aa = settings.NUMBER_OF_AUTOAPPLIES_FOR_STATS_FOR_DASHBOARD
    aa_qs = (
        models.Autoapply.objects
        .annotate(jobs_cnt=orm.Count(
            orm.Case(orm.When(
                apply__status__in=constants.APPLIED_OR_NEED_REVIEW,
                then=1), output_field=orm.IntegerField())))
        .filter(owner__user=user)
        .order_by('-modified_at')
    )
    in_progress_aa_qs = aa_qs.filter(
        status=enums.AutoapplyStatusEnum.IN_PROGRESS.name)[:number_of_aa]
    result_list = list(in_progress_aa_qs)
    number_of_aa -= len(result_list)
    # if len result_qs != number of autoapplies for stats for dashboard
    if number_of_aa != 0:
        aa_list = list(aa_qs.exclude(id__in=in_progress_aa_qs)[:number_of_aa])
        result_list.extend(aa_list)
    result = []
    for aa in result_list:
        progress_percents = (
            int((aa.jobs_cnt / aa.number) * 100)
        )
        result.append({
            'id': aa.id,
            'title': aa.title,
            'applied_jobs_cnt': aa.jobs_cnt,
            'progress_percents': progress_percents
        })
    return result
