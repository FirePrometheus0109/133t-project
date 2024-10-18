# pylint: disable=no-member
import dateutil
import pytz
from django.conf import settings
from rest_framework import exceptions

from event import constants
from leet import constants as base_constants
from leet import enums


def validate_job(company, job):
    is_valid_job = company.jobs.filter(
        status=enums.JobStatusEnum.ACTIVE.name,
        id=job.id)
    if not is_valid_job:
        emsg = constants.INVALID_JOB_FOR_EVENT.format(job.title)
        raise exceptions.ValidationError(emsg)


def _validate_count_attendees(attendees, max_count, emsg):
    if len(attendees) > max_count:
        raise exceptions.ValidationError(emsg.format(max_count))


def validate_count_candidates(candidates):
    _validate_count_attendees(
        candidates,
        settings.MAX_COUNT_OF_CANDIDATES_FOR_EVENT,
        constants.MAX_COUNT_OF_CANDIDATES_FOR_EVENT_ERROR
    )


def validate_count_colleagues(colleagues):
    _validate_count_attendees(
        colleagues,
        settings.MAX_COUNT_OF_COLLEAGUES_FOR_EVENT,
        constants.MAX_COUNT_OF_COLLEAGUES_FOR_EVENT_ERROR
    )


def validate_candidates(job, candidates):
    errors = []
    available_user_ids = set(
        job.candidates
           .exclude(
               status__name=base_constants.CANDIDATE_STATUS_REJECTED)
           .values_list('job_seeker__user__id', flat=True))
    for i in candidates:
        if i.id not in available_user_ids:
            emsg = constants.INVALID_CANDIDATE_FOR_EVENT_ERROR.format(
                i.get_full_name())
            errors.append(emsg)
    if errors:
        raise exceptions.ValidationError(errors)


def validate_colleagues(company, colleagues, current_user):
    errors = []
    available_user_ids = set(
        company.company_users
               .filter(
                   status=enums.CompanyUserStatusEnum.ACTIVE.name)  # noqa
               .values_list('user__id', flat=True))
    for i in colleagues:
        if i.id not in available_user_ids:
            emsg = constants.INVALID_COLLEAGUE_FOR_EVENT_ERROR.format(
                i.get_full_name())
            errors.append(emsg)
    if current_user not in colleagues:
        errors.append(
            constants.ATTENDEES_LIST_SHOULD_CONTAIN_EVENT_OWNER_ERROR)
    if errors:
        raise exceptions.ValidationError(errors)


def validate_event_time(time):
    if time.minute not in settings.VALID_TIME_MINUTE_VALUE_FOR_EVENT:
        raise exceptions.ValidationError(constants.INVALID_EVENT_TIME_ERROR)


def validate_event_from_to_time(time_from, time_to):
    if time_to < time_from:
        raise exceptions.ValidationError(
            constants.INVALID_TIME_FROM_TIME_TO_ERROR)


def validate_timezone_utcoffset_time_utcoffset(
        tz_name, time_from, time_to):
    # make sure that time_from and time_to offsets match to specified timezone
    tz = pytz.timezone(tz_name)
    time_from = dateutil.parser.parse(time_from).isoformat()
    time_to = dateutil.parser.parse(time_to).isoformat()
    localized_time_from = dateutil.parser.parse(time_from).astimezone(tz)
    localized_time_to = dateutil.parser.parse(time_to).astimezone(tz)
    if (time_from != localized_time_from.isoformat()
            or time_to != localized_time_to.isoformat()):
        emsg = constants.TIMEZONE_OFFSET_DOES_NOT_EQUAL_TIME_TZ_OFFSET
        raise exceptions.ValidationError(emsg)


def validate_query_params_for_list_of_events(query_params):
    errors = []
    tz = query_params.get('tz')
    if not tz:
        errors.append(constants.TIMEZONE_IS_REQUIRED_ERROR)
    day = query_params.get('day')
    month = query_params.get('month')
    if not any((day, month)):
        errors.append(constants.LIST_EVENTS_QUERY_PARAMS_DAY_OR_MONTH_ERROR)
    if all((day, month)):
        errors.append(constants.LIST_EVENTS_QUERY_PARAMS_DAY_OR_MONTH_ERROR)
    if errors:
        raise exceptions.ValidationError(errors)


def validate_attendee_event_status(attendee, status):
    if status == enums.EventAttendeeStatusEnum.INVITED.name:
        raise exceptions.ValidationError(
            constants.IMPOSSIBLE_TO_SET_INVITED_STATUS
        )
    if attendee.status in (enums.EventAttendeeStatusEnum.ACCEPTED.name,
                           enums.EventAttendeeStatusEnum.REJECTED.name):
        raise exceptions.ValidationError(
            constants.ATTENDEE_HAS_ALREADY_RESPONDED
        )
