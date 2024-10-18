from tests import utils
from leet import enums

COMPANY_USER_EXPECTED_JOB_DETAILS = {
    'id': utils.Any(int),
    'title': 'titletitle',
    'company': utils.Any(int),
    'industry': {
        'id': utils.Any(int),
        'name': 'Manufacturing'
    },
    'location': utils.Any(dict),
    'position_type': 'CONTRACT',
    'description': 'description',
    'status': 'ACTIVE',
    'education': 'ASSOCIATES_DEGREE',
    'clearance': enums.ClearanceTypesEnum.CONFIDENTIAL.name,
    'experience': 'FROM_1_TO_2',
    'salary_min': 200,
    'salary_max': 400,
    'salary_negotiable': False,
    'benefits': 'FOUR_OH_ONE_KEY',
    'travel': 'NO_TRAVEL',
    'education_strict': False,
    'publish_date': utils.Any(str),
    'manual_apply_strict_required_skills_matching': False,
    'owner': {
        'id': utils.Any(int),
        'name': 'cufirstname culastname'
    },
    'created_at': utils.Any(str),
    'required_skills': [
        {
            'id': utils.Any(int),
            'name': 'Electronic mail software'
        }
    ],
    'optional_skills': [
        {
            'id': utils.Any(int),
            'name': 'Operating system software'
        }
    ],
    'views_count': 0,
    'applies_count': 0,
    'autoapply_minimal_percent': 50,
    # actually here should be bool, but it's not extandable type
    'is_deleted': utils.Any(int),
    'deleted_at': utils.AnyOrNone(str),
    'questions': [
        {
            'id': utils.Any(int),
            'body': 'question1',
            'is_answer_required': True,
            'is_default': False,
            'disqualifying_answer': 'YES',
            'answer_type': 'YES_NO',
            'is_saved_question': False
        },
        {
            'id': utils.Any(int),
            'body': 'question2',
            'is_answer_required': False,
            'is_default': False,
            'disqualifying_answer': 'NO',
            'answer_type': 'YES_NO',
            'is_saved_question': False
        },
        {
            'id': utils.Any(int),
            'body': 'question3',
            'is_answer_required': False,
            'is_default': False,
            'disqualifying_answer': None,
            'answer_type': 'YES_NO',
            'is_saved_question': False
        }
    ],
    'is_cover_letter_required': False,
    'candidates_count': {
        'all': 0,
        'screened': 0,
        'applied': 0,
        'interviewed': 0,
        'offered': 0,
        'hired': 0,
        'rejected': 0
    },
    'closing_date': None,
    'modified_at': utils.Any(str),
    'guid': utils.Any(str)
}

JOB_SEEKER_EXPECTED_JOB_DETAILS = {
    'id': utils.Any(int),
    'title': 'titletitle',
    'company': {
        'id': utils.Any(int),
        'name': utils.Any(str)
    },
    'industry': {
        'id': utils.Any(int),
        'name': 'Manufacturing'
    },
    'location': utils.Any(dict),
    'position_type': 'CONTRACT',
    'description': 'description',
    'education': 'ASSOCIATES_DEGREE',
    'clearance': enums.ClearanceTypesEnum.CONFIDENTIAL.name,
    'experience': 'FROM_1_TO_2',
    'salary_min': 200,
    'salary_max': 400,
    'salary_negotiable': False,
    'benefits': 'FOUR_OH_ONE_KEY',
    'travel': 'NO_TRAVEL',
    'education_strict': False,
    'publish_date': utils.Any(str),
    'created_at': utils.Any(str),
    'saved_at': utils.AnyOrNone(str),
    'is_education_match': True,
    'is_clearance_match': True,
    'is_questionnaire_answered': False,
    'applied_at': utils.AnyOrNone(str),
    'required_skills': [
        {
            'id': utils.Any(int),
            'name': 'Electronic mail software',
            'match': True
        }
    ],
    'optional_skills': [
        {
            'id': utils.Any(int),
            'name': 'Operating system software',
            'match': True
        }
    ],
    'matching_percent': utils.Any(str),
    'questions': [
        {
            'id': utils.Any(int),
            'body': 'question1',
            'is_answer_required': True,
        },
        {
            'id': utils.Any(int),
            'body': 'question2',
            'is_answer_required': False,
        },
        {
            'id': utils.Any(int),
            'body': 'question3',
            'is_answer_required': False,
        }
    ],
    'is_cover_letter_required': False,
    'ban_status': 'ACTIVE',
    'guid': utils.Any(str)
}

DELETED_JOB_EXPECTED_DETAILS = {
    'id': utils.Any(int),
    'title': utils.Any(str),
    'is_deleted': True,
    'company': utils.Any(dict)
}

CSV_EXPECTED_HEADERS = {
    'Company', 'Job title', 'Created Date', 'Published Date', 'Author',
    'Status', 'Country', 'State', 'City', 'Zip', 'Industry',
    'Position type', 'Education', 'Years of experience',
    'Travel opportunities', 'Salary min', 'Salary max', 'Negotiable salary',
    'Clearance', 'Benefits', 'Description', 'Must Have Skills', 'Nice Have skills'
}
