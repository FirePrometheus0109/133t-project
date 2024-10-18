from tests import utils
from leet import enums

EXPECTED_JS_PROFILE = {
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
    'salary_min': 200,
    'salary_max': 400,
    'clearance': enums.ClearanceTypesEnum.CONFIDENTIAL.name,
    'experience': 'FROM_1_TO_2',
    'benefits': 'FOUR_OH_ONE_KEY',
    'travel': 'NO_TRAVEL',
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
    'educations': utils.Any(list),
    'certifications': utils.Any(list),
    'job_experience': utils.Any(list),
}


EXPECTED_JOB = {
    'id': utils.Any(int),
    'title': utils.Any(str),
    'company': {
        'id': utils.Any(int),
        'name': utils.Any(str)
    },
    'industry': {
        'id': utils.Any(int),
        'name': utils.Any(str)
    },
    'location': utils.Any(dict),
    'position_type': utils.Any(str),
    'description': utils.Any(str),
    'education': utils.Any(str),
    'clearance': utils.Any(int),
    'experience': utils.Any(str),
    'salary_min': utils.AnyOrNone(int),
    'salary_max': utils.AnyOrNone(int),
    'salary_negotiable': utils.Any(int),
    'benefits': utils.Any(str),
    'travel': utils.Any(str),
    'education_strict': utils.Any(int),
    'publish_date': utils.Any(str),
    'created_at': utils.Any(str),
    'required_skills': utils.Any(list),
    'optional_skills': utils.Any(list),
    'questions': utils.Any(list),
}
