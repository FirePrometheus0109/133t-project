from tests import utils


EXPECTED_LOGS_AFTER_PURCHASE_PROFILE = [
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

EXPECTED_LOGS_AFTER_ASSIGN_CANDIDATE = [
    {
        'id': utils.Any(int),
        'owner': {
            'id': utils.Any(int),
            'name': 'cufirstname culastname'
        },
        'time': utils.Any(str),
        'message': 'assigned Candidate to JP1.',
        'other_info': {}
    },
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

EXPECTED_LOGS_AFTER_APPLY = [
    {
        'id': utils.Any(int),
        'owner': {},
        'time': utils.Any(str),
        'message': 'Candidate applied for JP1.',
        'other_info': {}
    },
]

EXPECTED_LOGS_AFTER_AUTOAPPLY = [
    {
        'id': utils.Any(int),
        'owner': {},
        'time': utils.Any(str),
        'message': 'Candidate applied for title.',
        'other_info': {}
    },
]

EXPECTED_LOGS_AFTER_REAPPLY = [
    {
        'id': utils.Any(int),
        'owner': {},
        'time': utils.Any(str),
        'message': 'Candidate applied for JP1.',
        'other_info': {}
    },
    {
        'id': utils.Any(int),
        'owner': {},
        'time': utils.Any(str),
        'message': 'Candidate applied for JP1.',
        'other_info': {}
    }
]

EXPECTED_LOGS_AFTER_CHANGED_WORKFLOW = [
    {
        'id': utils.Any(int),
        'owner': {
            'id': utils.Any(int),
            'name': 'cufirstname culastname'
        },
        'time': utils.Any(str),
        'message': 'changed Candidate\'s status from Applied to Rejected in JP1',
        'other_info': {}
    },
    {
        'id': utils.Any(int),
        'owner': {},
        'time': utils.Any(str),
        'message': 'Candidate applied for JP1.',
        'other_info': {}
    }
]

EXPECTED_LOGS_AFTER_CHANGING_RATE = [
    {
        'id': utils.Any(int),
        'owner': {
            'id': utils.Any(int),
            'name': 'cufirstname culastname'
        },
        'time': utils.Any(str),
        'message': "changed Candidate's rate to Good in JP1.",
        'other_info': {}
    },
    {
        'id': utils.Any(int),
        'owner': {},
        'time': utils.Any(str),
        'message': 'Candidate applied for JP1.',
        'other_info': {}
    }
]

EXPECTED_LOGS_AFTER_REMOVING_RATE = [
    {
        'id': utils.Any(int),
        'owner': {
            'id': utils.Any(int),
            'name': 'cufirstname culastname'
        },
        'time': utils.Any(str),
        'message': "removed Candidate's rate in JP1.",
        'other_info': {}
    },
    {
        'id': utils.Any(int),
        'owner': {},
        'time': utils.Any(str),
        'message': 'Candidate applied for JP1.',
        'other_info': {}
    }
]

EXPECTED_LOGS_AFTER_ADDING_COMMENT_JS = [
    {
        'id': utils.Any(int),
        'owner': {
            'id': utils.Any(int),
            'name': 'cufirstname culastname'
        },
        'time': utils.Any(str),
        'message': 'left a comment.',
        'other_info': {}
    }
]

EXPECTED_LOGS_AFTER_EDIT_COMMENT_JS = [
    {
        'id': utils.Any(int),
        'owner': {
            'id': utils.Any(int),
            'name': 'cufirstname culastname'
        },
        'time': utils.Any(str),
        'message': 'edited a comment.',
        'other_info': {}
    },
    {
        'id': utils.Any(int),
        'owner': {
            'id': utils.Any(int),
            'name': 'cufirstname culastname'
        },
        'time': utils.Any(str),
        'message': 'left a comment.',
        'other_info': {}
    }
]

EXPECTED_LOGS_AFTER_DELETE_COMMENT_JS = [
    {
        'id': utils.Any(int),
        'owner': {
            'id': utils.Any(int),
            'name': 'cufirstname culastname'
        },
        'time': utils.Any(str),
        'message': 'deleted a comment.',
        'other_info': {
            'deleted_comment': {
                'title': 'what',
                'user': {
                    'id': utils.Any(int),
                    'name': 'cufirstname culastname',
                    'company_user': {
                        'id': utils.Any(int),
                    }
                },
                'submit_date': utils.Any(str),
                'comment': 'ever'
            }
        }
    },
    {
        'id': utils.Any(int),
        'owner': {
            'id': utils.Any(int),
            'name': 'cufirstname culastname'
        },
        'time': utils.Any(str),
        'message': 'left a comment.',
        'other_info': {}
    }
]


EXPECTED_LOGS_AFTER_CREATING_JOB = [
    {
        'id': utils.Any(int),
        'owner': {
            'id': utils.Any(int),
            'name': 'cufirstname culastname'
        },
        'message': 'created the job posting.',
        'time': utils.Any(str),
        'other_info': {}
    }
]


EXPECTED_LOGS_AFTER_DELETING_JOB = [
    {
        'id': utils.Any(int),
        'owner': {
            'id': utils.Any(int),
            'name': 'cufirstname culastname'
        },
        'message': 'deleted the job posting.',
        'time': utils.Any(str),
        'other_info': {}
    }
] + EXPECTED_LOGS_AFTER_CREATING_JOB


EXPECTED_LOGS_AFTER_CHANGING_JOB_STATUS = [
    {
        'id': utils.Any(int),
        'owner': {
            'id': utils.Any(int),
            'name': 'cufirstname culastname'
        },
        'message': 'changed status to Draft.',
        'time': utils.Any(str),
        'other_info': {}
    },
    {
        'id': utils.Any(int),
        'owner': {
            'id': utils.Any(int),
            'name': 'cufirstname culastname'
        },
        'message': 'created the job posting.',
        'time': utils.Any(str),
        'other_info': {}
    }
]

EXPECTED_LOGS_AFTER_EDITING_JOB = [
    {
        'id': utils.Any(int),
        'owner': {
            'id': utils.Any(int),
            'name': 'cufirstname culastname'
        },
        'message': 'edited the job posting.',
        'time': utils.Any(str),
        'other_info': {}
    },
    {
        'id': utils.Any(int),
        'owner': {
            'id': utils.Any(int),
            'name': 'cufirstname culastname'
        },
        'message': 'created the job posting.',
        'time': utils.Any(str),
        'other_info': {}
    }
]

EXPECTED_LOGS_AFTER_SAVING_OF_JOB_SEEKER = [
    {
        'id': utils.Any(int),
        'owner': {
            'id': utils.Any(int),
            'name': 'cufirstname culastname'
        },
        'message': 'added profile to Saved.',
        'time': utils.Any(str),
        'other_info': {}
    },
]

EXPECTED_LOGS_AFTER_EVENT_CREATION = {
    'id': utils.Any(int),
    'owner': {
        'id': utils.Any(int),
        'name': 'cufirstname culastname'
    },
    'message': utils.Any(str),
    'time': utils.Any(str),
    'other_info': {}
}
