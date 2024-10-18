# pylint: disable=no-member
import collections
import copy
import json

from django.conf import settings
from django.db import models as orm
from django.utils import timezone

from geo import models as geo_models
from job import constants
from job import models
from leet import constants as base_constants
from leet import emaillib
from leet import enums
from leet import models as base_models
from leet import services as base_services
from log import constants as log_constants
from log import utils as log_utils
from survey import utils as survey_utils

APPLIED = orm.Q(status__name=base_constants.CANDIDATE_STATUS_APPLIED)
SCREENED = orm.Q(status__name=base_constants.CANDIDATE_STATUS_SCREENED)
INTERVIEWED = orm.Q(status__name=base_constants.CANDIDATE_STATUS_INTERVIEWED)
OFFERED = orm.Q(status__name=base_constants.CANDIDATE_STATUS_OFFERED)
HIRED = orm.Q(status__name=base_constants.CANDIDATE_STATUS_HIRED)
REJECTED = orm.Q(status__name=base_constants.CANDIDATE_STATUS_REJECTED)


def is_publish_day_today(publish_date, today):
    return publish_date.date() == today.date()


def publish_delayed_job(job, today):
    """
    Publish a job if one from two rules is met.
    Job is delayed.
    First rule:
        A job without publish date should be publush immediately.
    Second rule:
        A job has publish date which is equal today.
    """
    active = enums.JobStatusEnum.ACTIVE.name
    delayed = enums.JobStatusEnum.DELAYED.name
    if ((not job.publish_date or is_publish_day_today(job.publish_date, today))
            and job.status == delayed):
        job.publish_date = today
        job.status = active


def add_publish_date(job, today):
    """Job with active status should contain publish date."""
    active = enums.JobStatusEnum.ACTIVE.name
    if not job.publish_date and job.status == active:
        job.publish_date = today


def add_skills(job, skills, is_required):
    """Add required or not required skills to job."""
    data = [{
        'job': job,
        'skill': s,
        'is_required': is_required
    } for s in skills]
    models.JobSkill.objects.bulk_create(models.JobSkill(**i) for i in data)


def create_job(data):
    """
    Creating job with status and skills.

    If job is saving with status 'active'
        it is publishing immediately.
    If job is saving with status 'delayed'
        (should be active on certain date) without publish date
        or with publish date == today -> job published immediately.
    """
    today = timezone.now()
    req_skills_ids = data.pop('required_skills')
    opt_skills_ids = data.pop('optional_skills', [])
    questions_data = data.pop('questions', [])
    location = data.pop('location')
    location = geo_models.Address.objects.create(
        country=location['country'],
        city=location['city'],
        zip=location.get('zip')
    )
    job = models.Job.objects.create(location=location, **data)

    if is_job_going_to_became_active(new_status=data['status']):
        decrease_jobs_balance(data['company'].customer.balance)

    publish_delayed_job(job, today)
    add_publish_date(job, today)

    add_skills(job, req_skills_ids, True)
    add_skills(job, opt_skills_ids, False)

    create_questions(questions_data, job)

    job.save()
    log_utils.create_log(
        job.owner.user,
        log_constants.LogEnum.job_create.name,
        log_constants.LogEnum.job_create.value,
        job)
    return job


def update_job(user, job, data):
    today = timezone.now()
    req_skills = data.pop('required_skills', [])
    opt_skills = data.pop('optional_skills', [])
    questions_data = data.pop('questions', [])
    location = data.pop('location', {})
    job_skills = job.job_skill_set.all()
    job_comparer = JobComparer(job, location, req_skills, opt_skills, data)

    if is_job_going_to_became_active(job=job, new_status=data['status']):
        decrease_jobs_balance(job.company.customer.balance)
    elif is_job_going_to_became_inactive(job=job, new_status=data['status']):
        increase_jobs_balance(job.company.customer.balance)

    for attr, val in data.items():
        setattr(job, attr, val)

    publish_delayed_job(job, today)
    add_publish_date(job, today)

    job_skills.delete()
    add_skills(job, req_skills, True)
    add_skills(job, opt_skills, False)

    # TODO (i.bogretsov) ask BA about questions and job's logs.
    # There is no opportunity to check questions.
    job.questions.clear()
    create_questions(questions_data, job)

    for attr, val in location.items():
        setattr(job.location, attr, val)
    job.location.save()

    if job.status == enums.JobStatusEnum.CLOSED.name:
        move_job_candidates_to_rejected(job)

    job.save()
    create_job_logs_after_editing(job_comparer, user, job)

    return job


def create_job_logs_after_editing(job_comparer, user, job):
    if job_comparer.is_job_status_changed:
        log_message = log_constants.LogEnum.job_status_change.value.format(
            job.get_status_display())
        log_utils.create_log(
            user, log_constants.LogEnum.job_status_change.name,
            log_message, job)
    if job_comparer.is_job_edited:
        log_utils.create_log(
            user, log_constants.LogEnum.job_edit.name,
            log_constants.LogEnum.job_edit.value, job)


def decrease_jobs_balance(balance):
    balance.jobs_remain = (orm.F('jobs_remain') - 1)
    balance.save()


def increase_jobs_balance(balance):
    balance.jobs_remain = (orm.F('jobs_remain') + 1)
    balance.save()


def get_allowed_educations_list(js_education):
    if not js_education:
        return ()
    education_types = (enums.EducationTypesEnum.HIGH_SCHOOL.name,
                       enums.EducationTypesEnum.CERTIFICATION.name,
                       enums.EducationTypesEnum.ASSOCIATES_DEGREE.name,
                       enums.EducationTypesEnum.BACHELORS_DEGREE.name,
                       enums.EducationTypesEnum.MASTERS_DEGREE.name,
                       enums.EducationTypesEnum.PHD.name)
    js_education_value = education_types.index(js_education)
    return education_types[:js_education_value + 1]


def create_questions(data, job):
    """
    If question's data has 'add_to_saved_questions' flag
    it's needed to create question with original data in saved questions list
    and create job's question. It is two different and separate questions.
    """
    questions = []
    if not data:
        return questions
    for q in data:
        if q.pop('add_to_saved_questions', False):
            survey_utils.create_one_question(company=job.company, **q)
        question = survey_utils.create_one_question(job=job, **q)
        questions.append(question)
    return questions


def soft_delete_job_list(jobs, user):
    for job in jobs:
        soft_delete_job(job, user)


def soft_delete_job(job, user):
    job.is_deleted = True
    job.deleted_at = timezone.now()
    job.status = ''
    move_job_candidates_to_rejected(job)
    job.save()
    log_utils.create_log(user, log_constants.LogEnum.job_delete.name,
                         log_constants.LogEnum.job_delete.value, job)


def restore_job(job):
    job.is_deleted = False
    job.deleted_at = None
    job.status = enums.JobStatusEnum.DRAFT.name
    job.save()
    return job


def move_job_candidates_to_rejected(job):
    candidates = job.candidates.all()
    status = base_models.CandidateStatus.get_rejected_status()
    for c in candidates:
        c.workflow_steps.create(status=status)
    candidates.update(status=status)


def is_clearance_match(job, job_seeker):
    return job.clearance <= (job_seeker.clearance or 0)


def is_questionnaire_answered(job, job_seeker):
    questions = job.questions.all()
    if questions.exists():
        return job_seeker.answers.filter(question__in=questions).exists()
    return True


def is_cover_letter_provided(job, cover_letter):
    return not job.is_cover_letter_required or cover_letter

def is_required_skills_match(job, job_seeker):
    if not job.manual_apply_strict_required_skills_matching:
        return True
    job_skills = set(job.required_skills)
    js_skills = set(job_seeker.skills.all())
    return job_skills.issubset(js_skills)

def get_count_candidates(queryset):
    """Return count candidates' with different statuses.

    param: queryset, candidates' Queryset.
    return: result, dict
    """

    def _count(filters):
        return orm.Count('id', filter=filters)

    qs = (queryset
          .annotate(
              applied=_count(APPLIED),
              screened=_count(SCREENED),
              interviewed=_count(INTERVIEWED),
              offered=_count(OFFERED),
              hired=_count(HIRED),
              rejected=_count(REJECTED))
          .values(
              'applied',
              'screened',
              'interviewed',
              'offered',
              'hired',
              'rejected'))

    result = collections.OrderedDict([
        (status.lower(), 0) for status in base_constants.CANDIDATE_STATUSES
    ])
    for entry in qs:
        for k in entry.keys():
            result[k] += entry[k]
    return result


def get_jobs_for_notification_about_closing_date(closing_date):
    """Return queryset of jobs which soon will be close."""
    return (models.Job.objects
                      .filter(
                          status=enums.JobStatusEnum.ACTIVE.name,  # noqa
                          closing_date__date=closing_date)
                      .annotate(
                          f_name=orm.F('owner__user__first_name'),
                          l_name=orm.F('owner__user__last_name'),
                          email=orm.F('owner__user__email'))
                      .values(
                          'id',
                          'email',
                          'f_name',
                          'l_name',
                          'title'))


def ban_company_jobs(company):
    # candidates for banned job should stay unchanged
    company.jobs.update(ban_status=enums.BanStatusEnum.BANNED.name,
                        status=enums.JobStatusEnum.DRAFT.name)


def unban_company_jobs(company):
    base_services.unban_entities(company.jobs)


def is_job_going_to_became_active(new_status, job=None):
    if new_status in constants.ACTIVE_OR_DELAYED_JOB_STATUSES:
        old_status = job.status if job else None
        return old_status not in constants.ACTIVE_OR_DELAYED_JOB_STATUSES
    return False


def is_job_going_to_became_inactive(new_status, job):
    return (new_status in constants.CLOSED_OR_DRAFT_JOB_STATUSES
            and job.status in constants.ACTIVE_OR_DELAYED_JOB_STATUSES)


class JobComparer:
    """Service that compares job's attrs after editing for creating log."""

    def __init__(  # noqa
            self, job, location_data,
            required_skills, optional_skills, single_attrs):
        self.is_changed = False
        # need deepcopy because we check attrs after `save` job's method
        self.job_old = copy.deepcopy(job)
        self.job_old_skills = [s for s in self.job_old.job_skill_set.all()]
        self.loca_data_new = location_data
        self.req_skills_new = set(required_skills)
        self.opt_skills_new = set(optional_skills)
        self.single_attrs_new = single_attrs

    def __are_attrs_changed(self, obj, data):
        """
        Use for compare single attrs of obj like 'title'.
        Job status is compared separately (separe log 'job_status_change')
        NOTE: this checking does not work with M2M fields.
        """
        if self.is_changed:
            return self.is_changed

        for attr, val in data.items():
            is_job_status = isinstance(obj, models.Job) and attr == 'status'
            if not is_job_status and getattr(obj, attr) != val:
                self.is_changed = True
                break
        return self.is_changed

    def _are_attrs_changed(self):
        return self.__are_attrs_changed(self.job_old, self.single_attrs_new)

    def _is_location_changed(self):
        return self.__are_attrs_changed(
            self.job_old.location, self.loca_data_new)

    def _are_skills_changed(self):
        if self.is_changed:
            return self.is_changed

        for s in self.job_old_skills:
            if (s.is_required and s.skill not in self.req_skills_new
                    or
                    not s.is_required and s.skill not in self.opt_skills_new):
                self.is_changed = True
                break

        return self.is_changed

    @property
    def is_job_status_changed(self):
        new_status = self.single_attrs_new.get('status', '')
        return new_status and new_status != self.job_old.status

    @property
    def is_job_edited(self):
        rules = (
            self._are_attrs_changed,
            self._is_location_changed,
            self._are_skills_changed
        )
        return any(r() for r in rules)


def share_job_by_email(job_seeker, job, email, url):
    location = '{} ({})'.format(
        job.location.city.name, job.location.city.state.abbreviation,
    )
    context = {
        'user': job_seeker.user,
        'url': url,
        'job': job,
        'company_name': job.company.name,
        'location': location,
        'domain_name': settings.DOMAIN_NAME
    }
    emaillib.send_email(constants.SHARE_JOB_TEMPLATE_NAME, [email], context)


def save_job_search(job_seeker, query_dict):
    # remove pagination params if exists
    query_params_dict = dict(query_dict.lists())
    query_params_dict.pop('limit', None)
    query_params_dict.pop('offset', None)
    query_params_dict.update(
        # do this tricky manipulations with filter values
        # because of frontend bug (filter duplications in query params)
        # TODO (m.nizovtsova): remove value casting after frontend fix
        (key, sorted(list(set(value))))
        for key, value in query_params_dict.items()
    )
    obj, created = job_seeker.searches.update_or_create(
        owner=job_seeker,
        criteria=json.dumps(query_params_dict, sort_keys=True)
    )
    if not created:
        obj.count = orm.F('count') + 1
        obj.save()
