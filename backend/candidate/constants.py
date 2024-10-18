# pylint: disable=no-member
from leet import enums


JOB_STATUSES_FOR_ASSIGNING_CANDIDATES = [
    enums.JobStatusEnum.ACTIVE.name,
    enums.JobStatusEnum.DELAYED.name
]

MAX_COUNT_OF_JOB_SEEKERS = 50
MAX_COUNT_OF_JOBS = 50

TIME_BASIS_DAY = 'day'
TIME_BASIS_WEEK = 'week'
TIME_BASIS_MONTH = 'month'


SUPPORTED_TIME_SERIES_BASES = (
    TIME_BASIS_DAY,
    TIME_BASIS_WEEK,
    TIME_BASIS_MONTH
)

INVALID_TIME_SERIES_BASIS_ERROR_MESSAGE = (
    'Unsupported daily basis. Pick one of: {}'
)

MAX_COUNT_OF_JOB_SEEKERS_ERROR = (
    'You can assign not more than 50 profiles at a time. Select less profiles.'
)

MAX_COUNT_OF_JOBS_ERROR = (
    'You can assign profiles not more than to 50 job postings at a time. '
    'Select less job postings.'
)

NOT_VALID_JOB_STATUS_FOR_ASSIGNING = (
    'You can assign candidates to job posting "{0}" '
    'because it has status "{1}". Job Posting should have status '
    '"ACTIVE" or "DELAYED".'
)

NOT_VALID_JOB_SEEKER_FOR_ASSIGNING = (
    'You can not assign this job seeker {0} {1}.'
)

RESTORE_CANDIDATE_ERROR = (
    'It is impossible to restore not rejected candidate.'
)

NOT_VALID_CANDIDATE_FOR_CHANGE_STATUS = (
    'It is impossible to change status rejected candidate.'
)

ANSWERS_CREATE_ERROR = (
    'Not applied job seeker can not create answers one more time.'
)

CANDIDATE_BANNED_ERROR = 'Job seeker {0} - account deleted'

REJECTED_CANDIDATE_ALREADY_REAPPLIED_ERROR = (
    'Candidate reapplied for this job posting on {}'
)

ANSWER_IS_REQUIRED_ON_QUESTION_ERROR = 'Answer on question "{}" is required.'
INVALID_COUNT_QUESTIONS_FOR_ANSWERS = 'Not valid count questions for job {}.'
INVALID_QUESTIONS_FOR_ANSWERS = 'Not valid questions for job {}.'

CANIDIDATE_ASSIGN_ACTIVITY = 'Assigned'
REJECTED_CANDIDATE_JOB_IS_DELETED_ERROR = (
    'Job posting was deleted. It is impossible to restore the candidate.'
)
REJECTED_CANDIDATE_JOB_IS_CLOSED_ERROR = (
    'Job posting was closed. It is impossible to restore the candidate.'
)
