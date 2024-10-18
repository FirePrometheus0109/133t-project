from leet import enums

MAX_NUMBER_OF_JOBS_TO_AUTOAPPLY = 30

MORE_THAN_30_JOBS_ERROR = (
    "You can't specify more than 30 jobs for per one autoapply."
)

EMPTY_JOB_LIST_ERROR = (
    "Impossible to apply for empty list of jobs."
)

IMPOSSIBLE_TO_START_ALREADY_STARTED_AUTOAPPLY_ERROR = (
    "You can't start one more time already started Autoapply."
)

YOU_CANT_APPLY_FOR_ALREADY_APPLIED_JOB_ERROR = (
    "You can't apply for already applied job."
)

AUTOAPPLY_TITLE_SHOULD_BE_UNIQUE_ERROR = (
    "Specify unique name to save this Auto apply."
)

EDUCATION_DOESNT_MATCH_ERROR = (
    "You can't apply for the job: Education does not match."
)

CLEARANCE_DOESNT_MATCH_ERROR = (
    "You can't apply for the job: Clearance does not match."
)

IMPOSSIBLE_TO_STOP_NOT_IN_PROGRESS_AUTOAPPLY_ERROR = (
    "Impossible to stop Autoapply than isn't in progress."
)

REQUIRED_SKILLS_MATCH_ERROR = (
    "You can't apply for the job: Required skills don't match."
)

IMPOSSIBLE_TO_RESTART_AUTOAPPLY_ERROR = (
    "Impossible to restart Autoapply."
)

APPLIED_OR_NEED_REVIEW = (
    enums.ApplyStatusEnum.APPLIED.name,  # noqa
    enums.ApplyStatusEnum.NEED_REVIEW.name  # noqa
)

PROFILE_ISNT_PUBLIC_ERROR = (
    "To apply for the job you need to have public profile."
)

IMPOSSIBLE_TO_APPLY_FOR_NOT_ACTIVE_JOB_ERROR = (
    "Impossible to apply for not active job."
)

ANSWER_QUESTIONNAIRE_BEFORE_APPLYING_ERROR = (
    "Answer questionnaire before applying"
)

AUTOAPPLY_NOTIFICATION_TEMPLATE_NAME = 'autoapply_notification.html'

COVER_LETTER_IS_REQUIRED_FOR_APPLY = (
    "Cover letter is required to apply for this job."
)

INVALID_STATE_ID_IN_QUERY_PARAMS_ERROR = (
    'Invalid "state_id" in query_params.'
)

INVALID_CITY_ID_IN_QUERY_PARAMS_ERROR = (
    'Invalid "city_id" in query_params.'
)

AUTOAPPLY_NUMBER_EXCEED_ERROR = (
    'Count of applied jobs shouldn\'t exceed requested number.'
)
