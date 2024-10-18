from tests import utils

from notification_center import constants


EXPECTED_LIST_AVAILABLE_TO_CHANGE_NOTIFICATION_TYPES = {
    constants.NOTIFICATION_FORMAT_WEB: [
        {
            'id': utils.Any(int),
            'name': constants.NOTIFICATION_TYPE_AUTO_APPLY_RESULTS
        }
    ],
    constants.NOTIFICATION_FORMAT_EMAIL: [
        {
            'id': utils.Any(int),
            'name': constants.NOTIFICATION_TYPE_AUTO_APPLY_RESULTS
        },
        {
            'id': utils.Any(int),
            'name': constants.NOTIFICATION_TYPE_PROFILE_VIEWS
        },
        {
            'id': utils.Any(int),
            'name': constants.NOTIFICATION_TYPE_INVITATION_RECEIVED
        }
    ]
}

EXPECTED_NOTIFICATIONS_SHORT_AFTER_NEW_JOB_IN_AUTOAPPLY = [
    {
        'id': utils.Any(int),
        'description': constants.NOTIFICATION_DESCRIPTION_FIND_NEW_JOB_AUTOAPPLY,
        'timestamp': utils.Any(str),
        'data': {
            'autoapply': {
                'id': utils.Any(int),
                'title': 'My autoapply'
            }
        }
    }
]

EXPECTED_NOTIFICATIONS_SHORT_AFTER_FINISHED_AUTOAPPLY = [
    {
        'id': utils.Any(int),
        'description': constants.NOTIFICATION_DESCRIPTION_FINISHED_AUTOAPPLY,
        'timestamp': utils.Any(str),
        'data': {
            'autoapply': {
                'id': utils.Any(int),
                'title': 'My autoapply'
            }
        }
    }
]

EXPECTED_NOTIFICATIONS_AFTER_NEW_JOB_IN_AUTOAPPLY = {
    'count': 1,
    'next': None,
    'previous': None,
    'results': [
        {
            'id': utils.Any(int),
            'data': {
                'autoapply': {
                    'id': utils.Any(int),
                    'title': 'My autoapply',
                    'description': constants.NOTIFICATION_DESCRIPTION_FIND_NEW_JOB_AUTOAPPLY,
                }
            },
            'timestamp': utils.Any(str),
        }
    ]
}

EXPECTED_NOTIFICATIONS_AFTER_FINISHED_AUTOAPPLY = {
    'count': 1,
    'next': None,
    'previous': None,
    'results': [
        {
            'id': utils.Any(int),
            'data': {
                'autoapply': {
                    'id': utils.Any(int),
                    'title': 'My autoapply',
                    'description': constants.NOTIFICATION_DESCRIPTION_FINISHED_AUTOAPPLY,
                }
            },
            'timestamp': utils.Any(str),
        }
    ]
}

EXPECTED_NOTIFS_COMPANY_USER_SHORT_END_OF_TRIAL = [
    {
        'id': utils.Any(int),
        'data': None,
        'description': 'Trial period expires 09th of March. '
                       'You will loose the access to all options. '
                       'Choose a package to continue using the platform.',
        'timestamp': utils.Any(str),
    }
]

EXPECTED_NOTIFS_COMPANY_USER_FULL_END_OF_TRIAL = {
    'count': 1,
    'next': None,
    'previous': None,
    'results': [
        {
            'id': utils.Any(int),
            'data': {
                'subscription': {
                    'description': 'Trial period expires 09th of March. '
                                   'You will loose the access to all options. '
                                   'Choose a package to continue using the platform.'
                }
            },
            'timestamp': utils.Any(str),
        }
    ]
}


EXPECTED_NOTIFS_COMPANY_USER_SHORT_PACKAGE_DELETED = [
    {
        'id': utils.Any(int),
        'data': None,
        'description': 'Your package Enterprise Corporate Package-50 '
                       'was deleted from the system. Your current package '
                       'is Corporate Package-40.',
        'timestamp': utils.Any(str),
    }
]

EXPECTED_NOTIFS_COMPANY_USER_FULL_PACKAGE_DELETED = {
    'count': 1,
    'next': None,
    'previous': None,
    'results': [
        {
            'id': utils.Any(int),
            'data': {
                'plan': {
                    'description': 'Your package '
                                   'Enterprise Corporate Package-50 was '
                                   'deleted from the system. Your current '
                                   'package is Corporate Package-40.'
                }
            },
            'timestamp': utils.Any(str),
        }
    ]
}


EXPECTED_NOTIF_SHORT_EVENT_INVITATION = [
    {
        'id': utils.Any(int),
        'data': {
            'event': {
                'description': 'Invitation from first Company.'
            }
        },
        'timestamp': utils.Any(str),
        'description': 'Invitation from first Company.'
    }
]

EXPECTED_NOTIF_FULL_EVENT_INVITATION = {
    'count': 1,
    'next': None,
    'previous': None,
    'results': [
        {
            'id': utils.Any(int),
            'data': {
                'event': {
                    'event_description': 'description',
                    'event_owner_full_name': 'cufirstname culastname',
                    'company_name': 'first Company',
                    'company_address': utils.Any(str),
                    'time_from': utils.Any(str),
                    'time_to': utils.Any(str),
                    'timezone': utils.Any(str),
                    'country_name': 'USA',
                    'city_name': utils.Any(str),
                    'state_abbreviation': utils.Any(str),
                    'address': 'address',
                    'zip_code': '10001',
                    'job_details_url': utils.Any(str),
                    'job_title': 'title',
                    'event_subject': 'subject',
                    'attendee_id': utils.Any(int),
                }
            },
            'timestamp': utils.Any(str)
        }
    ]
}

EXPECTED_NOTIF_SHORT_EVENT_UPDATED_INVITATION = [
    {
        'id': utils.Any(int),
        'data': {
            'event': {
                'description': 'Updated: Invitation from first Company.'
            }
        },
        'timestamp': utils.Any(str),
        'description': 'Updated: Invitation from first Company.'
    },
    {
        'id': utils.Any(int),
        'data': {
            'event': {
                'description': 'Invitation from first Company.'
            }
        },
        'timestamp': utils.Any(str),
        'description': 'Invitation from first Company.'
    }
]

EXPECTED_NOTIF_SHORT_EVENT_CANCELLED_INVITATION = [
    {
        'id': utils.Any(int),
        'data': {
            'event': {
                'description': 'Cancelled: Invitation from first Company.'
            }
        },
        'timestamp': utils.Any(str),
        'description': 'Cancelled: Invitation from first Company.'
    },
    {
        'id': utils.Any(int),
        'data': {
            'event': {
                'description': 'Invitation from first Company.'
            }
        },
        'timestamp': utils.Any(str),
        'description': 'Invitation from first Company.'
    }
]

EXPECTED_NOTIF_FULL_EVENT_UPDATED_INVITATION = {
    'count': 2,
    'next': None,
    'previous': None,
    'results': [
        {
            'id': utils.Any(int),
            'data': {
                'event': {
                    'event_description': 'new unique description',
                    'event_owner_full_name': 'cufirstname culastname',
                    'company_name': 'first Company',
                    'company_address': utils.Any(str),
                    'time_from': utils.Any(str),
                    'time_to': utils.Any(str),
                    'timezone': utils.Any(str),
                    'country_name': 'USA',
                    'city_name': utils.Any(str),
                    'state_abbreviation': utils.Any(str),
                    'address': 'address',
                    'zip_code': '10001',
                    'job_details_url': utils.Any(str),
                    'job_title': 'title',
                    'event_subject': 'Updated: subject',
                    'attendee_id': utils.Any(int),
                }
            },
            'timestamp': utils.Any(str),
        },
        {
            'id': utils.Any(int),
            'data': {
                'event': {
                    'event_description': 'description',
                    'event_owner_full_name': 'cufirstname culastname',
                    'company_name': 'first Company',
                    'company_address': utils.Any(str),
                    'time_from': utils.Any(str),
                    'time_to': utils.Any(str),
                    'timezone': utils.Any(str),
                    'country_name': 'USA',
                    'city_name': utils.Any(str),
                    'state_abbreviation': utils.Any(str),
                    'address': 'address',
                    'zip_code': utils.Any(str),
                    'job_details_url': utils.Any(str),
                    'job_title': 'title',
                    'event_subject': 'subject',
                    'attendee_id': utils.Any(int),
                }
            },
            'timestamp': utils.Any(str)
        }
    ]
}


EXPECTED_NOTIF_FULL_EVENT_CANCELLED_INVITATION = {
    'count': 2,
    'next': None,
    'previous': None,
    'results': [
        {
            'id': utils.Any(int),
            'data': {
                'event': {
                    'event_description': 'description',
                    'event_owner_full_name': 'cufirstname culastname',
                    'company_name': 'first Company',
                    'company_address': utils.Any(str),
                    'time_from': utils.Any(str),
                    'time_to': utils.Any(str),
                    'timezone': utils.Any(str),
                    'country_name': 'USA',
                    'city_name': utils.Any(str),
                    'state_abbreviation': utils.Any(str),
                    'address': 'address',
                    'zip_code': '10001',
                    'job_details_url': utils.Any(str),
                    'job_title': 'title',
                    'event_subject': 'Cancelled: subject',
                    'cancelled': True,
                    'attendee_id': utils.Any(int),
                }
            },
            'timestamp': utils.Any(str),
        },
        {
            'id': utils.Any(int),
            'data': {
                'event': {
                    'event_description': 'description',
                    'event_owner_full_name': 'cufirstname culastname',
                    'company_name': 'first Company',
                    'company_address': utils.Any(str),
                    'time_from': utils.Any(str),
                    'time_to': utils.Any(str),
                    'timezone': utils.Any(str),
                    'country_name': 'USA',
                    'city_name': utils.Any(str),
                    'state_abbreviation': utils.Any(str),
                    'address': 'address',
                    'zip_code': utils.Any(str),
                    'job_details_url': utils.Any(str),
                    'job_title': 'title',
                    'event_subject': 'subject',
                    'cancelled': True,
                    'attendee_id': utils.Any(int),
                }
            },
            'timestamp': utils.Any(str)
        }
    ]
}

EXPECTED_NOTIF_SHORT_EVENT_RESPONSE_INVITATION = [
    {
        'id': utils.Any(int),
        'data': {
            'event': {
                'description': 'jsfirstname jslastname has accepted invitation.'
            }
        },
        'timestamp': utils.Any(str),
        'description': 'jsfirstname jslastname has accepted invitation.'
    },
]


EXPECTED_NOTIF_FULL_EVENT_RESPONSE_INVITATION = {
    'count': 1,
    'next': None,
    'previous': None,
    'results': [
        {
            'id': utils.Any(int),
            'data': {
                'event': {
                    'event_description': 'description',
                    'event_owner_full_name': 'cufirstname culastname',
                    'company_name': 'first Company',
                    'company_address': utils.Any(str),
                    'time_from': utils.Any(str),
                    'time_to': utils.Any(str),
                    'timezone': utils.Any(str),
                    'country_name': utils.Any(str),
                    'city_name': utils.Any(str),
                    'state_abbreviation': utils.Any(str),
                    'address': 'address',
                    'zip_code': utils.Any(str),
                    'job_details_url': utils.Any(str),
                    'job_title': 'title',
                    'attendee_status': 'accepted',
                    'attendee_full_name': 'jsfirstname jslastname'
                }
            },
            'timestamp': utils.Any(str)
        }
    ]
}
