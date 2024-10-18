from tests import utils


COMPANY_USERS_REPORT_ACTIVITY = [
    {
        'is_online': True,
        'user': {
            'id': utils.Any(int),
            'name': utils.Any(str)
        },
        'stats': [
            {
                'Created Job postings': 1
            },
            {
                'Screenings': 0
            },
            {
                'Interviews': 0
            },
            {
                'Offers': 0
            },
            {
                'Hired Candidates': 0
            },
            {
                'Rejected Candidates': 1
            },
            {
                'Saved Candidates': 0
            }
        ]
    },
    {
        'is_online': True,
        'user': {
            'id': utils.Any(int),
            'name': utils.Any(str)
        },
        'stats': [
            {
                'Created Job postings': 0
            },
            {
                'Screenings': 0
            },
            {
                'Interviews': 0
            },
            {
                'Offers': 0
            },
            {
                'Hired Candidates': 0
            },
            {
                'Rejected Candidates': 0
            },
            {
                'Saved Candidates': 0
            }
        ]
    }
]


COMPANY_USERS_REPORT_ACTIVITY_ONE_USER = [
    {
        'is_online': True,
        'user': {
            'id': utils.Any(int),
            'name': utils.Any(str)
        },
        'stats': [
            {
                'Created Job postings': 1
            },
            {
                'Screenings': 0
            },
            {
                'Interviews': 0
            },
            {
                'Offers': 0
            },
            {
                'Hired Candidates': 0
            },
            {
                'Rejected Candidates': 1
            },
            {
                'Saved Candidates': 0
            }
        ]
    },
]
