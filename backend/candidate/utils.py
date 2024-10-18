import collections
import copy
import itertools

from django.db import models as orm
from django.db.models import functions

from candidate import models
from job import services
from leet import constants as base_constants
from leet import enums
from leet import models as base_models
from log import constants as log_constants
from log import utils as log_utils
from notification_center import constants as notif_constants
from notification_center import services as notif_services


def get_data_for_assign(combinations, status):
    data = [{
        'job_seeker_id': js_id,
        'job_id': job_id,
        'status': status
    } for js_id, job_id in combinations]
    return data


def split_combinations(combinations):
    js_ids = set(js_id for js_id, _ in combinations)
    jobs_ids = set(job_id for _, job_id in combinations)
    return list(js_ids), list(jobs_ids)


def get_assigned_candidates_qs(js_ids, jobs_ids, exclude_ids=None):
    """
    Return assigned candidates from database.
    This function used two times in 'assign candidates'.
    First time this funcion return already assigned candidates for company.
    Second time this function return just assigned candidates for company.
    """

    rejected_status = base_models.CandidateStatus.get_rejected_status()
    candidates = (models.Candidate.objects
                        .filter(
                            job_seeker__id__in=js_ids,
                            job__id__in=jobs_ids)
                        .exclude(
                            workflow_steps__status=rejected_status)
                        .annotate(
                            f_name=orm.F('job_seeker__user__first_name'),
                            l_name=orm.F('job_seeker__user__last_name'))
                        .values(
                            'id',
                            'job_seeker_id',
                            'job_id',
                            'job__title',
                            'f_name',
                            'l_name')
                        .order_by('f_name', 'l_name', 'job__title'))
    if exclude_ids:
        candidates = candidates.exclude(id__in=exclude_ids)
    return candidates


def get_data_for_response(candidates):

    def key(item):
        return (item['job_seeker_id'], item['f_name'], item['l_name'])

    result = []
    grouped_candidates = itertools.groupby(candidates, key=key)
    for candidate, grouped_data in grouped_candidates:
        result.append({
            'candidate': '{0} {1}'.format(candidate[1], candidate[2]),
            'jobs': [i['job__title'] for i in grouped_data]
        })
    return result


def exclude_already_assigned(combinations, already_assigned_qs):
    grouped = itertools.groupby(
        already_assigned_qs, key=lambda i: (i['job_seeker_id'], i['job_id']))
    excluded = set(pair for pair, _ in grouped)
    combinations = list(set(combinations) - excluded)
    return combinations


def assign_candidates(company_user, validated_data):
    """
    Bulk assign many job seeker on many jobs.
    If job seeker already assigned or applied and not rejected to job
    do not assign second time.
    """
    result = collections.OrderedDict()
    js_ids = [i['id'] for i in validated_data['job_seekers']]
    jobs_ids = [i['id'] for i in validated_data['jobs']]
    combinations = list(itertools.product(js_ids, jobs_ids))

    already_assigned = get_assigned_candidates_qs(js_ids, jobs_ids)
    allready_assigned_ids = [i['id'] for i in already_assigned]
    result['already_assigned'] = get_data_for_response(already_assigned)

    combinations = exclude_already_assigned(combinations, already_assigned)
    status = base_models.CandidateStatus.get_applied_status()
    data = get_data_for_assign(combinations, status)
    models.Candidate.objects.bulk_create(models.Candidate(**i) for i in data)
    js_ids, jobs_ids = split_combinations(combinations)
    assigned = get_assigned_candidates_qs(
        js_ids,
        jobs_ids,
        exclude_ids=allready_assigned_ids)

    assigned_candidates_ids = [i['id'] for i in assigned]
    data = [{
        'candidate_id': i,
        'status': status,
        'owner': company_user
    } for i in assigned_candidates_ids]
    models.WorkflowStep.objects.bulk_create(
        models.WorkflowStep(**i) for i in data)
    create_log_candidate_assign(company_user, assigned_candidates_ids)

    result['assigned'] = get_data_for_response(assigned)
    return result


def create_log_candidate_assign(company_user, candidates_ids):
    # NOTE it is slow behaviour
    candidates = (models.Candidate.objects
                                  .select_related('job_seeker', 'job')
                                  .filter(id__in=candidates_ids))
    user = company_user.user
    for candidate in candidates:
        log_type = log_constants.LogEnum.candidate_assign.name
        log_message = log_constants.LogEnum.candidate_assign.value.format(
            candidate.job.title)
        log_utils.create_log(user, log_type, log_message, candidate.job_seeker)


def update_or_create_rating(candidate, company_user, rating):
    defaults = {
        'owner': company_user,
        'rating': rating
    }
    rating, _ = models.Rating.objects.update_or_create(
        candidate=candidate,
        defaults=defaults)
    job_title = candidate.job.title
    log_type = log_constants.LogEnum.rate_change.name
    log_message = log_constants.LogEnum.rate_change.value.format(
        rating.get_rating_display(),
        job_title)
    if rating.rating == enums.RatingEnum.NO_RATING.name:  # noqa
        log_type = log_constants.LogEnum.rate_remove.name
        log_message = log_constants.LogEnum.rate_remove.value.format(job_title)
    log_utils.create_log(
        company_user.user, log_type, log_message, candidate.job_seeker)
    return rating


def annotate_candidate_with_applied_date(qs):
    rejected_status = base_models.CandidateStatus.get_rejected_status()
    rejected_candidates = (qs
                           .filter(
                               workflow_steps__status=rejected_status)
                           .values_list('id', flat=True))
    applied_date = orm.Case(
        orm.When(
            orm.Q(id__in=rejected_candidates),
            then=orm.F('previous_applied_date')),
        orm.When(
            orm.Q(apply__isnull=False),
            then=orm.F('apply__applied_at')),
        default=orm.F('created_at'))
    qs = qs.annotate(applied_date=applied_date)
    return qs


def annotate_candidates_qs_with_candidate_data(qs):
    disqual_answers_cnt = orm.Count(orm.Case(
        orm.When(
            orm.Q(job__answers__owner=orm.F('job_seeker'))
            &
            orm.Q(job__answers__answer=orm.F('job_seeker__answers__answer'))
            &
            ~orm.Q(job__answers__question__disqualifying_answer='')
            &
            orm.Q(job__answers__question__disqualifying_answer=orm.F(
                'job_seeker__answers__answer__yes_no_value')),
            then=1
        )), output_field=orm.IntegerField())
    is_disqual_for_questionnaire = orm.Case(
        orm.When(
            ~orm.Q(apply=None)
            &
            orm.Q(disqualified_answers_cnt__gt=0), then=True
        ), default=False, output_field=orm.BooleanField()
    )
    qs = annotate_candidate_with_applied_date(qs)
    qs = qs.annotate(
        disqualified_answers_cnt=disqual_answers_cnt,
        is_disqualified_for_questionnaire=is_disqual_for_questionnaire,
    )
    return qs


def update_workflow_steps(company_user, candidate, status):
    """Update workflow step of candidate.
    If new status is next or is 'rejected' in workflow just create new step
        with this status.
    If new status's is previous (return candidate on previous step in workflow)
        then delete all steps which workflow value more
        than new status workflow value.
    Create log about changing status
        if new status is not equal previous status.
    If candidate is rejected and he is attendee in some events
        delete candidate from event and
        send notification about deleteing from event.
    :param company_user: CompanyUser instance.
    :param candidate: Candidate instance.
    :param status: CandidateStatus instance.
    :return: WorkflowStep instance (new).
    """
    steps = candidate.workflow_steps.all()
    step_from = steps.last()
    if step_from.status.workflow_value >= status.workflow_value:
        (steps
         .filter(status__workflow_value__gt=status.workflow_value)
         .delete())
        step_to = steps.last()
    else:
        step_to = candidate.workflow_steps.create(
            status=status,
            owner=company_user)
    if step_from != step_to:
        log_type = log_constants.LogEnum.workflow_change.name
        log_message = log_constants.LogEnum.workflow_change.value.format(
            step_from.status.name,
            step_to.status.name,
            candidate.job.title)
        log_utils.create_log(
            company_user.user,
            log_type,
            log_message,
            candidate.job_seeker)
    if step_to.status.name == base_constants.CANDIDATE_STATUS_REJECTED:
        events = (company_user.company.events.filter(job=candidate.job))
        for event in events:
            notif_service = notif_services.EventAttendeeNotification(event)
            to_delete_attendee = event.attendees.filter(
                user=candidate.job_seeker.user)
            if to_delete_attendee.exists():
                attendee = copy.deepcopy(to_delete_attendee[0])
                to_delete_attendee.delete()
                notif_service.notify_attendee(
                    attendee,
                    notif_constants.EVENT_NOTIF_SUBJECT_PREFIX_CANCELLED)
    return step_to


def get_candidate_workflow_steps_stats(queryset, statuses=None):
    if statuses is None:
        statuses = base_models.CandidateStatus.objects.order_by(
            'workflow_value')
    stats = services.get_count_candidates(queryset)
    result = []
    for s in statuses:
        result.append({
            'id': s.id,
            'name': s.name,
            'n_candidates': stats[s.name.lower()]
        })
    return result


def get_candidate_status_time_series(queryset, candidate_status, basis):
    return (queryset
            .filter(status__name=candidate_status)
            .annotate(date=functions.Trunc('created_at', basis))
            .values('date')
            .annotate(count=orm.Count('candidate'))
            .order_by('date'))
