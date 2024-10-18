DEFAULT_QUESTIONS = (
    'Are you willing to relocate?',
    'Are you willing to travel locally?',
    'Do you live within driving distance of this position?',
    'Do you have reliable transportation?',
    'Do you have the required education for this position?',
    'Do you have the experience needed for this position?',
    'Do you have an associates degree?',
    'Do you have a bachelor\'s degree?',
    'Do you have a Ph.D.?',
    'Do you have the required clearance for this position?',
    'Do you have a masters degree?'
)

MAX_COUNT_SAVED_QUESTIONS = 30
MAX_COUNT_SURVEYS = 50
MAX_COUNT_QUESTIONS_IN_SURVEY = 10

MAX_COUNT_SAVED_QUESTIONS_ERROR = (
    'Max count of saved questions is 30 per company.'
)
MAX_COUNT_SURVEYS_ERROR = (
    'Company cah have only 50 question lists.'
)
MAX_COUNT_QUESTIONS_IN_SURVEY_ERROR = (
    'Question list can contain only 10 questions.'
)
NOT_UNIQUE_SURVEY_TITLE = (
    'Title of question list should be unique.'
)
CAN_NOT_EDIT_DEFAULT_QUESTIONS_ERROR = (
    'It is impossible to edit default questions.'
)
INVALID_DISQUALIFYING_ANSWER = (
    'Disqualifying answer can be only "Yes" or "No".'
)
ONLY_TITLE_CAN_PARTIAL_UPDATE_IN_SURVEY = (
    'Only title can update.'
)
