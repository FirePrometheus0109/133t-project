from leet import enums
from tests import utils

QUICK_VIEW_RESULTS_LIMIT = 1

EXPECTED_JOB_SEEKER_ANSWERS = [
    {
        'id': utils.Any(int),
        'question': {
            'id': utils.Any(int),
            'body': 'question1'
        },
        'answer': 'NO'
    },
    {
        'id': utils.Any(int),
        'question': {
            'id': utils.Any(int),
            'body': 'question2'
        },
        'answer': 'YES'
    },
    {
        'id': utils.Any(int),
        'question': {
            'id': utils.Any(int),
            'body': 'question3'
        },
        'answer': None
    }
]

EXPECTED_JOB_SEEKER_ANSWERS_FOR_COMPANY_USER = [
    {
        'id': utils.Any(int),
        'question': {
            'id': utils.Any(int),
            'body': 'question1'
        },
        'answer': 'NO',
        'is_disqualify': False
    },
    {
        'id': utils.Any(int),
        'question': {
            'id': utils.Any(int),
            'body': 'question2'
        },
        'answer': 'YES',
        'is_disqualify': False
    },
    {
        'id': utils.Any(int),
        'question': {
            'id': utils.Any(int),
            'body': 'question3'
        },
        'answer': None,
        'is_disqualify': False
    }
]

EXPECTED_ONE_CANDIDATE_ASSIGNED_TO_JOBS = {
    'assigned': [
        {
            'candidate': 'jsfirstname jslastname',
            'jobs': [
                'JP1',
                'JP2',
                'JP3',
                'JP4',
                'JP5',
                'JP6'
            ]
        }
    ],
    'already_assigned': []
}

EXPECTED_ONE_CANDIDATE_ALREADY_ASSIGNED_TO_JOBS = {
    'assigned': [],
    'already_assigned': [
        {
            'candidate': 'jsfirstname jslastname',
            'jobs': [
                'JP1',
                'JP2',
                'JP3',
            ]
        }
    ]
}

EXPECTED_TWO_CANDIDATES_ON_MANY_JOBS = {
    'assigned': [
        {
            'candidate': 'jsfirstname jslastname',
            'jobs': [
                'title'
            ]
        },
        {
            'candidate': 'jsfirstname_second jslastname_second',
            'jobs': [
                'JP1',
                'JP2',
                'JP3',
                'JP4',
                'JP5',
                'JP6',
                'title'
            ]
        }
    ],
    'already_assigned': [
        {
            'candidate': 'jsfirstname jslastname',
            'jobs': [
                'JP1',
                'JP2',
                'JP3',
                'JP4',
                'JP5',
                'JP6'
            ]
        }
    ]
}

EXPECTED_APPLIED_CANDIDATE_TO_JOB = {
    'assigned': [],
    'already_assigned': [
        {
            'candidate': 'jsfirstname jslastname',
            'jobs': [
                'JP1'
            ]
        }
    ]
}

EXPECTED_REJECTED_CANDIDATE_TO_JOB = {
    'assigned': [
        {
            'candidate': 'jsfirstname jslastname',
            'jobs': [
                'JP1'
            ]
        }
    ],
    'already_assigned': [],
}

EXPECTED_CANDIDATE_DATA = {
    'rating': {
        'owner': '',
        'rating': 'NO_RATING'
    },
    'status': {
        'id': utils.Any(int),
        'name': 'Applied'
    },
    'applied_date': utils.Any(str),
    'is_applied_after_assignment': False,
    'is_disqualified_for_questionnaire': False,
    'is_disqualified_for_skills': True,
    'created_at': utils.Any(str),
    'previous_applied_date': None,
    'cover_letter': None
}

EXPECTED_CANDIDATE_WORKFLOW_STEPS_ONLY_APPLIED = [
    {
        'id': utils.Any(int),
        'name': 'Applied',
        'n_candidates': 1
    },
    {
        'id': utils.Any(int),
        'name': 'Screened',
        'n_candidates': 0
    },
    {
        'id': utils.Any(int),
        'name': 'Interviewed',
        'n_candidates': 0
    },
    {
        'id': utils.Any(int),
        'name': 'Offered',
        'n_candidates': 0
    },
    {
        'id': utils.Any(int),
        'name': 'Hired',
        'n_candidates': 0
    },
    {
        'id': utils.Any(int),
        'name': 'Rejected',
        'n_candidates': 0
    }
]

EXPECTED_CANDIDATE_COMPLETED_WORKFLOW = [
    {
        'id': utils.Any(int),
        'name': 'Applied',
        'n_candidates': 1
    },
    {
        'id': utils.Any(int),
        'name': 'Screened',
        'n_candidates': 1
    },
    {
        'id': utils.Any(int),
        'name': 'Interviewed',
        'n_candidates': 1
    },
    {
        'id': utils.Any(int),
        'name': 'Offered',
        'n_candidates': 1
    },
    {
        'id': utils.Any(int),
        'name': 'Hired',
        'n_candidates': 1
    },
    {
        'id': utils.Any(int),
        'name': 'Rejected',
        'n_candidates': 0
    }
]

EXPECTED_CANDIDATE_COMPLETED_WORKFLOW_REJECTED = [
    {
        'id': utils.Any(int),
        'name': 'Applied',
        'n_candidates': 1
    },
    {
        'id': utils.Any(int),
        'name': 'Screened',
        'n_candidates': 1
    },
    {
        'id': utils.Any(int),
        'name': 'Interviewed',
        'n_candidates': 1
    },
    {
        'id': utils.Any(int),
        'name': 'Offered',
        'n_candidates': 1
    },
    {
        'id': utils.Any(int),
        'name': 'Hired',
        'n_candidates': 1
    },
    {
        'id': utils.Any(int),
        'name': 'Rejected',
        'n_candidates': 1
    }
]

EXPECTED_CANDIDATE_COMPLETED_WORKFLOW_RETURNED_SCREENED = [
    {
        'id': utils.Any(int),
        'name': 'Applied',
        'n_candidates': 1
    },
    {
        'id': utils.Any(int),
        'name': 'Screened',
        'n_candidates': 1
    },
    {
        'id': utils.Any(int),
        'name': 'Interviewed',
        'n_candidates': 0
    },
    {
        'id': utils.Any(int),
        'name': 'Offered',
        'n_candidates': 0
    },
    {
        'id': utils.Any(int),
        'name': 'Hired',
        'n_candidates': 0
    },
    {
        'id': utils.Any(int),
        'name': 'Rejected',
        'n_candidates': 0
    }
]


EXPECTED_CANDIDATE_APPLIED_REJECTED = [
    {
        'id': utils.Any(int),
        'name': 'Applied',
        'n_candidates': 1
    },
    {
        'id': utils.Any(int),
        'name': 'Screened',
        'n_candidates': 0
    },
    {
        'id': utils.Any(int),
        'name': 'Interviewed',
        'n_candidates': 0
    },
    {
        'id': utils.Any(int),
        'name': 'Offered',
        'n_candidates': 0
    },
    {
        'id': utils.Any(int),
        'name': 'Hired',
        'n_candidates': 0
    },
    {
        'id': utils.Any(int),
        'name': 'Rejected',
        'n_candidates': 1
    }
]

EXPECTED_CANDIDATE_SCREENED_REJECTED_SCREENED = [
    {
        'id': utils.Any(int),
        'name': 'Applied',
        'n_candidates': 1
    },
    {
        'id': utils.Any(int),
        'name': 'Screened',
        'n_candidates': 1
    },
    {
        'id': utils.Any(int),
        'name': 'Interviewed',
        'n_candidates': 0
    },
    {
        'id': utils.Any(int),
        'name': 'Offered',
        'n_candidates': 0
    },
    {
        'id': utils.Any(int),
        'name': 'Hired',
        'n_candidates': 0
    },
    {
        'id': utils.Any(int),
        'name': 'Rejected',
        'n_candidates': 0
    }
]

EXPECTED_CANDIDATE_COMPLETED_REJECTED_WORKFLOW_REAPPLY = [
    {
        'id': utils.Any(int),
        'name': 'Applied',
        'n_candidates': 2
    },
    {
        'id': utils.Any(int),
        'name': 'Screened',
        'n_candidates': 1
    },
    {
        'id': utils.Any(int),
        'name': 'Interviewed',
        'n_candidates': 1
    },
    {
        'id': utils.Any(int),
        'name': 'Offered',
        'n_candidates': 1
    },
    {
        'id': utils.Any(int),
        'name': 'Hired',
        'n_candidates': 1
    },
    {
        'id': utils.Any(int),
        'name': 'Rejected',
        'n_candidates': 1
    }
]

COMPANY_REPORT_ALL_DATE = [
    {
        'name': 'Applied',
        'series': [
            {'date': '2019-01-20T00:00:00Z', 'count': 120}
        ]
    },
    {
        'name': 'Screened',
        'series': [
            {'date': '2019-01-21T00:00:00Z', 'count': 1},
            {'date': '2019-01-23T00:00:00Z', 'count': 1},
            {'date': '2019-01-24T00:00:00Z', 'count': 1},
            {'date': '2019-01-26T00:00:00Z', 'count': 1},
            {'date': '2019-01-27T00:00:00Z', 'count': 1},
            {'date': '2019-01-29T00:00:00Z', 'count': 1},
            {'date': '2019-01-30T00:00:00Z', 'count': 1},
            {'date': '2019-02-01T00:00:00Z', 'count': 1},
            {'date': '2019-02-02T00:00:00Z', 'count': 1},
            {'date': '2019-02-04T00:00:00Z', 'count': 1},
            {'date': '2019-02-05T00:00:00Z', 'count': 1},
            {'date': '2019-02-07T00:00:00Z', 'count': 1},
            {'date': '2019-02-08T00:00:00Z', 'count': 1},
            {'date': '2019-02-10T00:00:00Z', 'count': 1},
            {'date': '2019-02-11T00:00:00Z', 'count': 1},
            {'date': '2019-02-13T00:00:00Z', 'count': 1},
            {'date': '2019-02-14T00:00:00Z', 'count': 1},
            {'date': '2019-02-16T00:00:00Z', 'count': 1},
            {'date': '2019-02-17T00:00:00Z', 'count': 1},
            {'date': '2019-02-19T00:00:00Z', 'count': 1}
        ]
    },
    {
        'name': 'Interviewed',
        'series': [
            {'date': '2019-01-21T00:00:00Z', 'count': 1},
            {'date': '2019-01-23T00:00:00Z', 'count': 1},
            {'date': '2019-01-24T00:00:00Z', 'count': 1},
            {'date': '2019-01-26T00:00:00Z', 'count': 1},
            {'date': '2019-01-27T00:00:00Z', 'count': 1},
            {'date': '2019-01-29T00:00:00Z', 'count': 1},
            {'date': '2019-01-30T00:00:00Z', 'count': 1},
            {'date': '2019-02-01T00:00:00Z', 'count': 1},
            {'date': '2019-02-02T00:00:00Z', 'count': 1},
            {'date': '2019-02-04T00:00:00Z', 'count': 1},
            {'date': '2019-02-05T00:00:00Z', 'count': 1},
            {'date': '2019-02-07T00:00:00Z', 'count': 1},
            {'date': '2019-02-08T00:00:00Z', 'count': 1},
            {'date': '2019-02-10T00:00:00Z', 'count': 1},
            {'date': '2019-02-11T00:00:00Z', 'count': 1},
            {'date': '2019-02-13T00:00:00Z', 'count': 1},
            {'date': '2019-02-14T00:00:00Z', 'count': 1},
            {'date': '2019-02-16T00:00:00Z', 'count': 1},
            {'date': '2019-02-17T00:00:00Z', 'count': 1},
            {'date': '2019-02-19T00:00:00Z', 'count': 1}
        ]
    },
    {
        'name': 'Offered',
        'series': [
            {'date': '2019-01-21T00:00:00Z', 'count': 1},
            {'date': '2019-01-23T00:00:00Z', 'count': 1},
            {'date': '2019-01-24T00:00:00Z', 'count': 1},
            {'date': '2019-01-26T00:00:00Z', 'count': 1},
            {'date': '2019-01-27T00:00:00Z', 'count': 1},
            {'date': '2019-01-29T00:00:00Z', 'count': 1},
            {'date': '2019-01-30T00:00:00Z', 'count': 1},
            {'date': '2019-02-01T00:00:00Z', 'count': 1},
            {'date': '2019-02-02T00:00:00Z', 'count': 1},
            {'date': '2019-02-04T00:00:00Z', 'count': 1},
            {'date': '2019-02-05T00:00:00Z', 'count': 1},
            {'date': '2019-02-07T00:00:00Z', 'count': 1},
            {'date': '2019-02-08T00:00:00Z', 'count': 1},
            {'date': '2019-02-10T00:00:00Z', 'count': 1},
            {'date': '2019-02-11T00:00:00Z', 'count': 1},
            {'date': '2019-02-13T00:00:00Z', 'count': 1},
            {'date': '2019-02-14T00:00:00Z', 'count': 1},
            {'date': '2019-02-16T00:00:00Z', 'count': 1},
            {'date': '2019-02-17T00:00:00Z', 'count': 1},
            {'date': '2019-02-19T00:00:00Z', 'count': 1}
        ]
    },
    {
        'name': 'Hired',
        'series': [
            {'date': '2019-01-21T00:00:00Z', 'count': 1},
            {'date': '2019-01-23T00:00:00Z', 'count': 1},
            {'date': '2019-01-24T00:00:00Z', 'count': 1},
            {'date': '2019-01-26T00:00:00Z', 'count': 1},
            {'date': '2019-01-27T00:00:00Z', 'count': 1},
            {'date': '2019-01-29T00:00:00Z', 'count': 1},
            {'date': '2019-01-30T00:00:00Z', 'count': 1},
            {'date': '2019-02-01T00:00:00Z', 'count': 1},
            {'date': '2019-02-02T00:00:00Z', 'count': 1},
            {'date': '2019-02-04T00:00:00Z', 'count': 1},
            {'date': '2019-02-05T00:00:00Z', 'count': 1},
            {'date': '2019-02-07T00:00:00Z', 'count': 1},
            {'date': '2019-02-08T00:00:00Z', 'count': 1},
            {'date': '2019-02-10T00:00:00Z', 'count': 1},
            {'date': '2019-02-11T00:00:00Z', 'count': 1},
            {'date': '2019-02-13T00:00:00Z', 'count': 1},
            {'date': '2019-02-14T00:00:00Z', 'count': 1},
            {'date': '2019-02-16T00:00:00Z', 'count': 1},
            {'date': '2019-02-17T00:00:00Z', 'count': 1},
            {'date': '2019-02-19T00:00:00Z', 'count': 1}
        ]
    },
    {
        'name': 'Rejected',
        'series': [
            {'date': '2019-01-21T00:00:00Z', 'count': 1},
            {'date': '2019-01-23T00:00:00Z', 'count': 1},
            {'date': '2019-01-24T00:00:00Z', 'count': 1},
            {'date': '2019-01-26T00:00:00Z', 'count': 1},
            {'date': '2019-01-27T00:00:00Z', 'count': 1},
            {'date': '2019-01-29T00:00:00Z', 'count': 1},
            {'date': '2019-01-30T00:00:00Z', 'count': 1},
            {'date': '2019-02-01T00:00:00Z', 'count': 1},
            {'date': '2019-02-02T00:00:00Z', 'count': 1},
            {'date': '2019-02-04T00:00:00Z', 'count': 1},
            {'date': '2019-02-05T00:00:00Z', 'count': 1},
            {'date': '2019-02-07T00:00:00Z', 'count': 1},
            {'date': '2019-02-08T00:00:00Z', 'count': 1},
            {'date': '2019-02-10T00:00:00Z', 'count': 1},
            {'date': '2019-02-11T00:00:00Z', 'count': 1},
            {'date': '2019-02-13T00:00:00Z', 'count': 1},
            {'date': '2019-02-14T00:00:00Z', 'count': 1},
            {'date': '2019-02-16T00:00:00Z', 'count': 1},
            {'date': '2019-02-17T00:00:00Z', 'count': 1},
            {'date': '2019-02-19T00:00:00Z', 'count': 1}
        ]
    }]

COMPANY_REPORT_5_DAYS = [
    {
        'name': 'Applied',
        'series': [
            {'date': '2019-01-20T00:00:00Z', 'count': 120}
        ]
    },
    {
        'name': 'Screened',
        'series': [
            {'date': '2019-01-21T00:00:00Z', 'count': 1},
            {'date': '2019-01-23T00:00:00Z', 'count': 1},
            {'date': '2019-01-24T00:00:00Z', 'count': 1}
        ]
    },
    {
        'name': 'Interviewed',
        'series': [
            {'date': '2019-01-21T00:00:00Z', 'count': 1},
            {'date': '2019-01-23T00:00:00Z', 'count': 1},
            {'date': '2019-01-24T00:00:00Z', 'count': 1}
        ]
    },
    {
        'name': 'Offered',
        'series': [
            {'date': '2019-01-21T00:00:00Z', 'count': 1},
            {'date': '2019-01-23T00:00:00Z', 'count': 1},
            {'date': '2019-01-24T00:00:00Z', 'count': 1}
        ]
    }, {
        'name': 'Hired',
        'series': [
            {'date': '2019-01-21T00:00:00Z', 'count': 1},
            {'date': '2019-01-23T00:00:00Z', 'count': 1},
            {'date': '2019-01-24T00:00:00Z', 'count': 1}
        ]
    }, {
        'name': 'Rejected',
        'series': [
            {'date': '2019-01-21T00:00:00Z', 'count': 1},
            {'date': '2019-01-23T00:00:00Z', 'count': 1},
            {'date': '2019-01-24T00:00:00Z', 'count': 1}
        ]
    }
]

COMPANY_REPORT_4_WEEK = [
    {
        'name': 'Applied', 'series': [
        {'date': '2019-01-14T00:00:00Z', 'count': 120}
    ]
    },
    {
        'name': 'Screened',
        'series': [
            {'date': '2019-01-21T00:00:00Z', 'count': 5},
            {'date': '2019-01-28T00:00:00Z', 'count': 4},
            {'date': '2019-02-04T00:00:00Z', 'count': 5},
            {'date': '2019-02-11T00:00:00Z', 'count': 5}
        ]
    },
    {
        'name': 'Interviewed',
        'series': [
            {'date': '2019-01-21T00:00:00Z', 'count': 5},
            {'date': '2019-01-28T00:00:00Z', 'count': 4},
            {'date': '2019-02-04T00:00:00Z', 'count': 5},
            {'date': '2019-02-11T00:00:00Z', 'count': 5}
        ]
    },
    {
        'name': 'Offered',
        'series': [
            {'date': '2019-01-21T00:00:00Z', 'count': 5},
            {'date': '2019-01-28T00:00:00Z', 'count': 4},
            {'date': '2019-02-04T00:00:00Z', 'count': 5},
            {'date': '2019-02-11T00:00:00Z', 'count': 5}
        ]
    },
    {
        'name': 'Hired',
        'series': [
            {'date': '2019-01-21T00:00:00Z', 'count': 5},
            {'date': '2019-01-28T00:00:00Z', 'count': 4},
            {'date': '2019-02-04T00:00:00Z', 'count': 5},
            {'date': '2019-02-11T00:00:00Z', 'count': 5}
        ]
    },
    {
        'name': 'Rejected',
        'series': [
            {'date': '2019-01-21T00:00:00Z', 'count': 5},
            {'date': '2019-01-28T00:00:00Z', 'count': 4},
            {'date': '2019-02-04T00:00:00Z', 'count': 5},
            {'date': '2019-02-11T00:00:00Z', 'count': 5}
        ]
    }
]

COMPANY_REPORT_8_WEEKS_MONTH_BASIS = [
    {
        'name': 'Applied',
        'series': [
            {'date': '2019-01-01T00:00:00Z', 'count': 120}
        ]
    },
    {
        'name': 'Screened',
        'series': [
            {'date': '2019-01-01T00:00:00Z', 'count': 7},
            {'date': '2019-02-01T00:00:00Z', 'count': 13}
        ]
    },
    {
        'name': 'Interviewed',
        'series': [
            {'date': '2019-01-01T00:00:00Z', 'count': 7},
            {'date': '2019-02-01T00:00:00Z', 'count': 13}
        ]
    },
    {
        'name': 'Offered',
        'series': [
            {'date': '2019-01-01T00:00:00Z', 'count': 7},
            {'date': '2019-02-01T00:00:00Z', 'count': 13}
        ]
    },
    {
        'name': 'Hired',
        'series': [
            {'date': '2019-01-01T00:00:00Z', 'count': 7},
            {'date': '2019-02-01T00:00:00Z', 'count': 13}
        ]
    },
    {
        'name': 'Rejected',
        'series': [
            {'date': '2019-01-01T00:00:00Z', 'count': 7},
            {'date': '2019-02-01T00:00:00Z', 'count': 13}
        ]
    }
]

COMPANY_REPORT_EMPTY = [
    {'name': 'Applied', 'series': []},
    {'name': 'Screened', 'series': []},
    {'name': 'Interviewed', 'series': []},
    {'name': 'Offered', 'series': []},
    {'name': 'Hired', 'series': []},
    {'name': 'Rejected', 'series': []}
]

CANDIDATE_WORKFLOW_STATS_ALL = [
    {
        'id': utils.Any(int),
        'name': 'Applied',
        'n_candidates': 1
    },
    {
        'id': utils.Any(int),
        'name': 'Screened',
        'n_candidates': 1
    },
    {
        'id': utils.Any(int),
        'name': 'Interviewed',
        'n_candidates': 0
    },
    {
        'id': utils.Any(int),
        'name': 'Offered',
        'n_candidates': 1
    },
    {
        'id': utils.Any(int),
        'name': 'Hired',
        'n_candidates': 1
    },
    {
        'id': utils.Any(int),
        'name': 'Rejected',
        'n_candidates': 0
    }
]

CANDIDATE_WORKFLOW_STATS_PAST_SIXTY_DAYS = [
    {
        'id': utils.Any(int),
        'name': 'Applied',
        'n_candidates': 1
    },
    {
        'id': utils.Any(int),
        'name': 'Screened',
        'n_candidates': 0
    },
    {
        'id': utils.Any(int),
        'name': 'Interviewed',
        'n_candidates': 0
    },
    {
        'id': utils.Any(int),
        'name': 'Offered',
        'n_candidates': 1
    },
    {
        'id': utils.Any(int),
        'name': 'Hired',
        'n_candidates': 1
    },
    {
        'id': utils.Any(int),
        'name': 'Rejected',
        'n_candidates': 0
    }
]

CANDIDATE_WORKFLOW_STATS_PAST_THIRTY_DAYS = [
    {
        'id': utils.Any(int),
        'name': 'Applied',
        'n_candidates': 1
    },
    {
        'id': utils.Any(int),
        'name': 'Screened',
        'n_candidates': 0
    },
    {
        'id': utils.Any(int),
        'name': 'Interviewed',
        'n_candidates': 0
    },
    {
        'id': utils.Any(int),
        'name': 'Offered',
        'n_candidates': 0
    },
    {
        'id': utils.Any(int),
        'name': 'Hired',
        'n_candidates': 1
    },
    {
        'id': utils.Any(int),
        'name': 'Rejected',
        'n_candidates': 0
    }
]

CANDIDATE_WORKFLOW_STATS_PAST_TWO_WEEKS = [
    {
        'id': utils.Any(int),
        'name': 'Applied',
        'n_candidates': 1
    },
    {
        'id': utils.Any(int),
        'name': 'Screened',
        'n_candidates': 0
    },
    {
        'id': utils.Any(int),
        'name': 'Interviewed',
        'n_candidates': 0
    },
    {
        'id': utils.Any(int),
        'name': 'Offered',
        'n_candidates': 0
    },
    {
        'id': utils.Any(int),
        'name': 'Hired',
        'n_candidates': 0
    },
    {
        'id': utils.Any(int),
        'name': 'Rejected',
        'n_candidates': 0
    }
]

EXPECTED_CANDIDATES_ACTIVITIES_AFTER_APPLY = [
    {
        'candidate': {
            'id': utils.Any(int),
            'name': 'jsfirstname jslastname'
        },
        'activity': 'Applied',
        'job': {
            'id': utils.Any(int),
            'title': 'JP1'
        },
        'created_at': utils.Any(str)
    }
]

EXPECTED_CANDIDATES_ACTIVITIES_AFTER_ASSIGN = [
    {
        'candidate': {
            'id': utils.Any(int),
            'name': 'jsfirstname jslastname'
        },
        'activity': 'Assigned',
        'job': {
            'id': utils.Any(int),
            'title': 'JP1'
        },
        'created_at': utils.Any(str)
    }
]

CSV_EXPECTED_HEADERS = {
    'First name', 'Last name', 'Applied Job title', 'Applied Date', 'Location',
    'Date of profile update', 'Email', 'Phone', 'Address', 'Industry(s)',
    'Position type', 'Education', 'Years of experience', 'Travel opportunities',
    'Salary min', 'Salary max', 'Clearance', 'Benefits', 'Skills',
    'Education details', 'Experience details', 'Workflow step', 'Rate'

}