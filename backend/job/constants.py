# pylint: disable=no-member
from django.conf import settings
from leet import enums


MAX_COUNT_OF_SKILLS = 20

MIN_SALARY_MORE_THAN_MAX_SALARY_ERROR = (
    'Minimum salary shouldn\'t be greater than maximum salary.'
)

SKILLS_INTERSECT_ERROR = (
    'Required skill and optional skill sets shouldn\'t intersect.'
)

PUBLISH_DATE_IN_PAST_ERROR = (
    'You can\'t post the job with past date. '
    'To schedule the job select date in the future'
)

MORE_20_SKILLS_ERROR = (
    'Ensure this field has no more than 20 elements.'
)

JOB_ALREADY_DELETED = (
    'You can not delete already deleted job.'
)

JOB_IS_NOT_DELETED = (
    'You can not restore non-deleted job.'
)


MAX_SALARY_VALUE_ERROR = (
    'Salary can not be great than {0}'.format(settings.MAX_SALARY)
)

CLOSING_DATE_IN_THE_PAST_ERROR = (
    'You can\'t publish the job posting with past closing date. '
    'To publish the job posting select closing date in the future.'
)

PUBLISH_DATE_GREAT_THAN_CLOSING_DATE_ERROR = (
    'To publish job posting select closing date later than publishing date.'
)

NOT_VALID_STATUS_TO_CLOSING_JOB = (
    'It is possible change status to "CLOSED" only if job has status "ACTIVE".'
)

NOT_VALID_STATUS_FOR_CREATING_JOB = (
    'It is possible change status to "CLOSED" only if job has status "ACTIVE".'
)

CLOSE_JOBS_EMAIL_TEMPLATE = 'close_jobs.html'

JOB_BANNED_ERROR = 'Job posting was banned'

ACTIVE_OR_DELAYED_JOB_STATUSES = [
    enums.JobStatusEnum.ACTIVE.name,
    enums.JobStatusEnum.DELAYED.name,
]

CLOSED_OR_DRAFT_JOB_STATUSES = [
    enums.JobStatusEnum.CLOSED.name,
    enums.JobStatusEnum.DRAFT.name,
]

OUT_OF_JOB_ERROR = (
    'You are out of Job postings. Update your subscription to '
    'purchase additional Job postings'
)

SHARE_JOB_TEMPLATE_NAME = 'share_job.html'

CSV_DELIMITER = ';'
