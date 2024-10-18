from tests import utils
from leet import enums
EXPECTED_JOB_SEEKER_EDUCATION_LIST = [
    {
        'id': utils.Any(int),
        'owner': utils.Any(int),
        'institution': 'education2',
        'field_of_study': 'study',
        'degree': '',
        'date_from': utils.Any(str),
        'date_to': None,
        'location': 'location',
        'description': 'descripion',
        'is_current': True,
        'created_at': utils.Any(str)
    },
    {
        'id': utils.Any(int),
        'owner': utils.Any(int),
        'institution': 'education3',
        'field_of_study': 'study',
        'degree': '',
        'date_from': utils.Any(str),
        'date_to': utils.Any(str),
        'location': 'location',
        'description': 'descripion',
        'is_current': False,
        'created_at': utils.Any(str)
    },
    {
        'id': utils.Any(int),
        'owner': utils.Any(int),
        'institution': 'education1',
        'field_of_study': 'study',
        'degree': '',
        'date_from': utils.Any(str),
        'date_to': utils.Any(str),
        'location': 'location',
        'description': 'descripion',
        'is_current': False,
        'created_at': utils.Any(str)
    }
]

EXPECTED_JOB_SEEKER_CERTIFICATION_LIST = [
    {
        'id': utils.Any(int),
        'owner': utils.Any(int),
        'institution': 'certification2',
        'field_of_study': 'study',
        'licence_number': None,
        'graduated': None,
        'location': 'location',
        'description': 'descripion',
        'is_current': True,
        'created_at': utils.Any(str)
    },
    {
        'id': utils.Any(int),
        'owner': utils.Any(int),
        'institution': 'certification3',
        'field_of_study': 'study',
        'licence_number': '10001aoooa',
        'graduated': utils.Any(str),
        'location': 'location',
        'description': 'descripion',
        'is_current': False,
        'created_at': utils.Any(str)
    },
    {
        'id': utils.Any(int),
        'owner': utils.Any(int),
        'institution': 'certification1',
        'field_of_study': 'study',
        'licence_number': '10001aoooa',
        'graduated': utils.Any(str),
        'location': 'location',
        'description': 'descripion',
        'is_current': False,
        'created_at': utils.Any(str)
    }
]

EXPECTED_JOB_EXPERIENCE = {
    'id': utils.Any(int),
    'owner': utils.Any(int),
    'company': 'job seeker company',
    'job_title': 'title',
    'description': 'some description',
    'date_from': '2018-01-01T00:00:00Z',
    'date_to': None,
    'is_current': True,
    'employment': 'FULL_TIME'
}

EXPECTED_JOB_DOCUMENT = {
    'id': utils.Any(int),
    'owner': utils.Any(int),
    'name': 'test doc',
    'extension': 'doc',
    'file': utils.Any(str)
}

EXPECTED_COVER_LETTER = {
    'id': utils.Any(int),
    'owner': utils.Any(int),
    'title': utils.Any(str),
    'body': 'body',
    'is_default': False,
}

EXPECTED_LOGS_IN_PROFILE_AFTER_PURCHASE = [
    {
        'id': utils.Any(int),
        'owner': {
            'id': utils.Any(int),
            'name': 'cufirstname culastname'
        },
        'time': utils.Any(str),
        'message': "purchased Candidate's profile.",
        'other_info': {}
    }
]

EXPECTED_JS_PROFILE_DETAILS_FOR_OWNER = {
    'id': utils.Any(int),
    'user': {
        'id': utils.Any(int),
        'email': '0email@mail.com',
        'last_name': 'jslastname',
        'first_name': 'jsfirstname'
    },
    'photo': None,
    'phone': '+375297777777',
    'address': {
        'id': utils.Any(int),
        'address': '6942 Mccoy Lakes',
        'country': {
            'id': utils.Any(int),
            'name': 'USA'
        },
        'city': {
            'id': utils.Any(int),
            'name': 'New York',
            'state': {
                'id': utils.Any(int),
                'name': 'New York',
                'abbreviation': 'NY'
            }
        },
        'zip': {
            'id': utils.Any(int),
            'code': '10001'
        }
    },
    'about': 'about',
    'position_type': 'CONTRACT',
    'education': 'ASSOCIATES_DEGREE',
    'salary_public': True,
    'salary_min': 200,
    'salary_max': 400,
    'clearance': enums.ClearanceTypesEnum.CONFIDENTIAL.name,
    'experience': 'FROM_1_TO_2',
    'benefits': 'FOUR_OH_ONE_KEY',
    'travel': 'NO_TRAVEL',
    'is_public': True,
    'profile_completion': utils.Any(dict),
    'industries': [
        {
            'id': utils.Any(int),
            'name': 'Construction'
        }
    ],
    'skills': [
        {
            'id': utils.Any(int),
            'name': 'Document management software'
        },
        {
            'id': utils.Any(int),
            'name': 'Electronic mail software'
        },
        {
            'id': utils.Any(int),
            'name': 'Operating system software'
        }
    ],
    'is_shared': False,
    'is_password_set': True
}
