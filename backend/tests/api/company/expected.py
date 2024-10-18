from tests import utils

EXPECTED_ADDRESS_DATA_DRAFT_COMPANY = {
    'id': utils.Any(int),
    'address': 'address',
    'country': {
        'id': utils.Any(int),
        'name': 'USA'
    },
    'city': {
        'id': utils.Any(int),
        'name': 'Ashville',
        'state': {
            'id': utils.Any(int),
            'name': 'Alabama',
            'abbreviation': 'AL'
        }
    },
    'zip': {
        'id': utils.Any(int),
        'code': '35953'
    }
}
