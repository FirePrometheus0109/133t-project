MAX_COUNT_OF_JOB_EXPERIENCE = 10
MAX_COUNT_OF_DOCUMENTS = 10
MAX_COUNT_OF_EDUCATION = 30
MAX_COUNT_OF_COVER_LETTERS = 5
MAX_COUNT_OF_INDUSTRIES = 6
MAX_COUNT_OF_SKILLS = 20
VALID_DOCUMENT_EXTENSIONS = ['doc', 'docx', 'pdf', 'txt', 'rtf', 'odt']


MAXIMUM_OF_JOB_EXPERIENCE_ERROR = (
    'User can have only {} job experience.'.format(MAX_COUNT_OF_JOB_EXPERIENCE)
)
MAXIMUM_OF_DOCUMENTS_ERROR = (
    'You have exceeded the limit for uploading documents. '
    'Only {} documents can be uploaded.'.format(MAX_COUNT_OF_DOCUMENTS)
)
DOCUMENT_MAX_FILE_SIZE_MB = 1
NOT_VALID_DOCUMENT_EXTENSION_ERROR = (
    'The extension is not valid. Valid extensions: {}'
        .format(', '.join(VALID_DOCUMENT_EXTENSIONS))
)
DOCUMENT_FILE_SIZE_ERROR = (
    "Your file exceeds the file limit ({}MB). Please upload a file that "
    "doesn't exceed the limit.".format(DOCUMENT_MAX_FILE_SIZE_MB)
)
DATE_FROM_GREATER_DATE_TO_ERROR = (
    'Field date_from should be less than date_to.'
)
DATES_FROM_FUTURE_ERROR = (
    'Selected dates are from future.'
)
DATE_TO_AND_IS_CURRENT_ERROR = (
    'Field date_to should be empty if job is current.'
)
NO_DATE_TO_AND_NOT_IS_CURRENT_ERROR = (
    'Field date_to should not be empty if job is not current.'
)
MAXIMUM_OF_EDUCATION_ENTRIES_ERROR = (
    'Maximum count of education\'s experience is {}.'.format(
        MAX_COUNT_OF_EDUCATION))
CERTIFICATION_IS_CURRENT_ERROR = (
    'Not ended certification can not contain graduated or licence_number'
)
CERTIFICATION_IS_NOT_CURRENT_ERROR = (
    'Ended certification should contain date of graduated and licence_number'
)
NO_ACTIONS_FOR_ADDING_TO_SAVED_ERROR = (
    'There are no actions.'
)
TWO_ACTIONS_FOR_ADDING_TO_SAVED_ERROR = (
    'Can handle only one action.'
)
PROFILE_CANT_BE_PUBLIC_ERROR = (
    'Unable to make profile public.'
)

PROFILE_IS_HIDDEN_ERROR = (
    'This profile was hidden by its owner.'
)

COVER_LETTER_TITLE_SHOULD_BE_UNIQUE = (
    'Cover letter title should be unique.'
)

MIN_SALARY_SHOULD_NOT_BE_GREATER_THAN_MAX = (
    'Minimum salary shouldn\'t be greater than maximum salary.'
)

MAXIMUM_OF_COVER_LETTER_ENTRIES_ERROR = (
    'Maximum count of cover letters is {}.'.format(MAX_COUNT_OF_COVER_LETTERS))

INVALID_PHONE_NUMBER_ERROR = (
    'Invalid phone number.'
)

SAVED_JOB_SEEKER_ALREADY_CANDIDATE_ERROR = (
    '{} has already applied to a job.'
)

SAVED_JOB_SEEKER_ALREADY_PURCHASED_ERROR = (
    '{} has already been purchased.'
)

SAVED_JOB_SEEKER_BANNED_ERROR = (
    '{} - account deleted.'
)

MAP_LISTS_OF_SINGLE_VALUE_FIELDS = (
    ['phone'],
    ['about'],
    ['position_type'],
    ['education'],
    ['experience'],
    ['user', 'first_name'],
    ['user', 'last_name'],
    ['address', 'country'],
    ['address', 'city'],
    ['address', 'zip'],
)

MAP_LISTS_OF_MANY_VALUES_FIELDS = (
    ['job_experience'],
    ['skills']
)

MAP_LISTS_SPECIAL_RULES_VALUES_FIELDS = (
    ['educations'],
)

FILEDS_WEIGHTS_FOR_PROFILE_COMPLETION = {
    'user': 10,
    'phone': 10,
    'address': 10,
    'about': 10,
    'position_type': 10,
    'education': 10,
    'experience': 10,
    'job_experience': 10,
    'educations': 10,
    'skills': 10
}

VIEW_PROFILES_TEMPLATE_NAME = 'profile_views.html'

MAXIMUM_OF_INDUSTRIES_ERROR = (
    'Maximum count of selected industries is {}'.format(
        MAX_COUNT_OF_INDUSTRIES
    )
)

MAXIMUM_OF_SKILLS_ERROR = (
    'Maximum count of selected skills is {}'.format(
        MAX_COUNT_OF_SKILLS
    )
)
