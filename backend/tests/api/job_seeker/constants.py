from leet import enums
from tests import constants


JOB_SEEKERS_DATA_FOR_TESTING_FILTERS = (
    {
        'user_data': {
            'first_name': 'john',
            'last_name': 'last_name_one',
            'password': constants.DEFAULT_PASSWORD,
        },
        'js_data':
        {
            'position_type': enums.PositionTypesEnum.CONTRACT.name,
            'education': enums.EducationTypesEnum.BACHELORS_DEGREE.name,
            'clearance': enums.ClearanceTypesEnum.PUBLIC_TRUST.name,
            'experience': enums.ExperienceEnum.MORE_THAN_10.name,
            'travel': enums.JSTravelOpportunitiesEnum.WILLING_TO_TRAVEL.name,
            'about': 'some data with weights for tests. Packman keyword'
        },
        'city': 'New York',
        'add_more_skills': True
    },
    {
        'user_data': {
            'first_name': 'bob',
            'last_name': 'john',
            'password': constants.DEFAULT_PASSWORD,
        },
        'js_data':
        {
            'position_type': enums.PositionTypesEnum.CONTRACT.name,
            'education': enums.EducationTypesEnum.MASTERS_DEGREE.name,
            'clearance': enums.ClearanceTypesEnum.CONFIDENTIAL.name,
            'experience': enums.ExperienceEnum.MORE_THAN_10.name,
            'travel': enums.JSTravelOpportunitiesEnum.NO_TRAVEL.name,
            'about': 'nothing interesting.'
        },
        'city': 'New York'
    },
    {
        'user_data': {
            'first_name': 'mike',
            'last_name': 'last_name_six',
            'password': constants.DEFAULT_PASSWORD,
        },
        'js_data':
        {
            'position_type': enums.PositionTypesEnum.FULL_TIME.name,
            'education': enums.EducationTypesEnum.BACHELORS_DEGREE.name,
            'clearance': enums.ClearanceTypesEnum.TOP_SECRET.name,
            'experience': enums.ExperienceEnum.MORE_THAN_10.name,
            'travel': enums.JSTravelOpportunitiesEnum.NO_TRAVEL.name,
            'about': 'my zip-code 10001. This is false. noname. BOOOM'
        },
        'city': 'Ashville',
        'add_more_skills': True,
    },
    {
        'user_data': {
            'first_name': 'roberto',
            'last_name': 'last_name_seven',
            'password': constants.DEFAULT_PASSWORD,
        },
        'js_data':
        {
            'position_type': enums.PositionTypesEnum.PART_TIME.name,
            'education': enums.EducationTypesEnum.ASSOCIATES_DEGREE.name,
            'clearance': enums.ClearanceTypesEnum.TOP_SECRET.name,
            'experience': enums.ExperienceEnum.MORE_THAN_10.name,
            'travel': enums.JSTravelOpportunitiesEnum.NO_TRAVEL.name,
            'about': 'foo bar, document'
        },
        'city': 'Ashville'
    },
    {
        'user_data': {
            'first_name': 'noname',
            'last_name': 'last_name_ten',
            'password': constants.DEFAULT_PASSWORD,
        },
        'js_data':
        {
            'position_type': enums.PositionTypesEnum.TEMPORARY.name,
            'education': enums.EducationTypesEnum.HIGH_SCHOOL.name,
            'clearance': enums.ClearanceTypesEnum.PUBLIC_TRUST.name,
            'experience': enums.ExperienceEnum.FROM_1_TO_2.name,
            'travel': enums.JSTravelOpportunitiesEnum.WILLING_TO_TRAVEL.name,
            'about': 'roberto data. Many words, boom, title'
        },
        'city': 'Ashville',
        'add_more_skills': True
    },
    {
        'user_data': {
            'first_name': 'packman',
            'last_name': 'name',
            'password': constants.DEFAULT_PASSWORD,
        },
        'js_data':
        {
            'position_type': enums.PositionTypesEnum.TEMPORARY.name,
            'education': enums.EducationTypesEnum.HIGH_SCHOOL.name,
            'clearance': enums.ClearanceTypesEnum.PUBLIC_TRUST.name,
            'experience': enums.ExperienceEnum.FROM_1_TO_2.name,
            'travel': enums.JSTravelOpportunitiesEnum.WILLING_TO_TRAVEL.name,
            'about': 'Packman is from Packwood'
        },
        'city': 'Packwood',
        'add_more_skills': True
    }
)
