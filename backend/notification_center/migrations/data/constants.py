from notification_center import constants


NOTIFICATIONS_JOB_SEEKER_TYPES_DATA = [
    {
        'name': constants.NOTIFICATION_TYPE_AUTO_APPLY_RESULTS,
        'can_disable': True,
        'format': constants.NOTIFICATION_FORMAT_EMAIL
    },
    {
        'name': constants.NOTIFICATION_TYPE_AUTO_APPLY_RESULTS,
        'can_disable': True,
        'format': constants.NOTIFICATION_FORMAT_WEB
    },
    {
        'name': constants.NOTIFICATION_TYPE_PROFILE_VIEWS,
        'can_disable': True,
        'format': constants.NOTIFICATION_FORMAT_EMAIL
    },
    {
        'name': constants.NOTIFICATION_TYPE_INVITATION_RECEIVED,
        'can_disable': True,
        'format': constants.NOTIFICATION_FORMAT_EMAIL
    },
    {
        'name': constants.NOTIFICATION_TYPE_INVITATION_RECEIVED,
        'can_disable': False,
        'format': constants.NOTIFICATION_FORMAT_WEB
    }
]


NOTIFICATIONS_JOB_SEEKER_VERBS_DATA = [
    {
        'name': constants.NOTIFICATION_VERB_FINISHED_AUTOAPPLY,
        'type': constants.NOTIFICATION_TYPE_AUTO_APPLY_RESULTS
    },
    {
        'name': constants.NOTIFICATION_VERB_FIND_NEW_JOB_AUTOAPPLY,
        'type': constants.NOTIFICATION_TYPE_AUTO_APPLY_RESULTS
    },
    {
        'name': constants.NOTIFICATION_VERB_SENT_INVITATION,
        'type': constants.NOTIFICATION_TYPE_INVITATION_RECEIVED
    },
    {
        'name': constants.NOTIFICATION_VERB_UPDATED_INVITATION,
        'type': constants.NOTIFICATION_TYPE_INVITATION_RECEIVED
    },
    {
        'name': constants.NOTIFICATION_VERB_DELETED_INVITATION,
        'type': constants.NOTIFICATION_TYPE_INVITATION_RECEIVED
    },
]


NOTIFICATIONS_COMPANY_USER_TYPES_DATA = [
    {
        'name': constants.NOTIFICATION_TYPE_RESPONSE_TO_INVITATION,
        'can_disable': False,
        'format': constants.NOTIFICATION_FORMAT_EMAIL
    },
    {
        'name': constants.NOTIFICATION_TYPE_RESPONSE_TO_INVITATION,
        'can_disable': False,
        'format': constants.NOTIFICATION_FORMAT_WEB
    },
    {
        'name': constants.NOTIFICATION_TYPE_END_OF_TRIAL,
        'can_disable': False,
        'format': constants.NOTIFICATION_FORMAT_EMAIL
    },
    {
        'name': constants.NOTIFICATION_TYPE_END_OF_TRIAL,
        'can_disable': False,
        'format': constants.NOTIFICATION_FORMAT_WEB
    },
    {
        'name': constants.NOTIFICATION_TYPE_INVITATION_RECEIVED,
        'can_disable': True,
        'format': constants.NOTIFICATION_FORMAT_EMAIL
    },
    {
        'name': constants.NOTIFICATION_TYPE_INVITATION_RECEIVED,
        'can_disable': False,
        'format': constants.NOTIFICATION_FORMAT_WEB
    }
]


NOTIFICATION_COMPANY_USER_VERBS_DATA = [
    {
        'name': constants.NOTIFICATION_VERB_RESPONSE_TO_INVITATION,
        'type': constants.NOTIFICATION_TYPE_RESPONSE_TO_INVITATION
    },
    {
        'name': constants.NOTIFICATION_VERB_END_OF_TRIAL,
        'type': constants.NOTIFICATION_TYPE_END_OF_TRIAL
    },
    {
        'name': constants.NOTIFICATION_VERB_SENT_INVITATION,
        'type': constants.NOTIFICATION_TYPE_INVITATION_RECEIVED
    },
    {
        'name': constants.NOTIFICATION_VERB_UPDATED_INVITATION,
        'type': constants.NOTIFICATION_TYPE_INVITATION_RECEIVED
    },
    {
        'name': constants.NOTIFICATION_VERB_DELETED_INVITATION,
        'type': constants.NOTIFICATION_TYPE_INVITATION_RECEIVED
    },
]
