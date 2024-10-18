NOTIFICATION_FORMAT_WEB = '133T'
NOTIFICATION_FORMAT_EMAIL = 'Email'

NOTIFICATION_TYPE_AUTO_APPLY_RESULTS = 'Auto apply results notifications'
NOTIFICATION_TYPE_PROFILE_VIEWS = 'Profile views'
NOTIFICATION_TYPE_INVITATION_RECEIVED = 'Invitation received'
NOTIFICATION_TYPE_RESPONSE_TO_INVITATION = 'Response to invitation'
NOTIFICATION_TYPE_END_OF_TRIAL = 'End of trial'
NOTIFICATION_TYPE_PACKAGE_DELETION = 'Package deletion'
NOTIFICATION_TYPE_PRICE_CHANGES = 'Price changes'

NOTIFICATION_VERB_FINISHED_AUTOAPPLY = 'finished auto apply'
NOTIFICATION_VERB_FIND_NEW_JOB_AUTOAPPLY = 'finished auto apply'
NOTIFICATION_VERB_SENT_INVITATION = 'has sent invitation'
NOTIFICATION_VERB_UPDATED_INVITATION = 'has updated invitation'
NOTIFICATION_VERB_DELETED_INVITATION = 'has deleted invitation'
NOTIFICATION_VERB_RESPONSE_TO_INVITATION = 'has responsed invitation'
NOTIFICATION_VERB_END_OF_TRIAL = 'Ended Trial'
NOTIFICATION_VERB_PACKAGE_WILL_DELETED = 'Package will be deleted'
NOTIFICATION_VERB_PACKAGE_WAS_DELETED = 'Package was deleted'
NOTIFICATION_VERB_PACKAGE_PRICE_CHANGED = 'Package price was changed'

NOTIFICATION_DESCRIPTION_FIND_NEW_JOB_AUTOAPPLY = (
    'Auto apply clickabletitle: new jobs found.'
)
NOTIFICATION_DESCRIPTION_FINISHED_AUTOAPPLY = (
    'Auto apply clickabletitle: finished execution.'
)
NOTIFICATION_DESCRIPTION_END_OF_TRIAL = (
    'Trial period expires {}. You will loose the access to all options. '
    'Choose a package to continue using the platform.'
)

NOTIFICATION_DESCRIPTION_PACKAGE_WILL_DELETED = (
    'Starting from {}, your package {}  will be deleted. Please select one '
    'of the other packages - linktodashboard. In case the new package is not '
    'selected, your package will be change to {}.'
)

NOTIFICATION_DESCRIPTION_PACKAGE_WAS_DELETED = (
    'Your package {} was deleted from the system. '
    'Your current package is {}.'
)

NOTIFICATION_DESCRIPTION_PRICE_WAS_CHANGED = (
    'Starting from {price_apply_date}, your subscription price will be '
    '{new_price}$ per month. This increase will take effect on your next '
    'billing date on or after {price_apply_date}.'
)

NOTIFICATION_DESCRIPTION_SENT_INVITATION = 'Invitation from {}.'
NOTIFICATION_DESCRIPTION_UPDATED_INVITATION = 'Updated: Invitation from {}.'
NOTIFICATION_DESCRIPTION_CANCELLED_INVITATION = (
    'Cancelled: Invitation from {}.'
)
NOTIFICATION_DESCRIPTION_RESPONSE_INVITATION = '{} has {} invitation.'

NOTIFICATION_TYPES_CAN_DISABLE_JOB_SEEKER = [
    {
        'name': NOTIFICATION_TYPE_AUTO_APPLY_RESULTS,
        'format': NOTIFICATION_FORMAT_EMAIL
    },
    {
        'name': NOTIFICATION_TYPE_AUTO_APPLY_RESULTS,
        'format': NOTIFICATION_FORMAT_WEB
    },
    {
        'name': NOTIFICATION_TYPE_PROFILE_VIEWS,
        'format': NOTIFICATION_FORMAT_EMAIL
    },
    {
        'name': NOTIFICATION_TYPE_INVITATION_RECEIVED,
        'format': NOTIFICATION_FORMAT_EMAIL
    },
]

EVENT_NOTIF_SUBJECT_PREFIX_INVITED = 'Invited'
EVENT_NOTIF_SUBJECT_PREFIX_UPDATED = 'Updated'
EVENT_NOTIF_SUBJECT_PREFIX_CANCELLED = 'Cancelled'

NOTIF_DESCRIPTION_EVENT_SUBJECT_MAP = {
    EVENT_NOTIF_SUBJECT_PREFIX_INVITED:
        NOTIFICATION_DESCRIPTION_SENT_INVITATION,
    EVENT_NOTIF_SUBJECT_PREFIX_UPDATED:
        NOTIFICATION_DESCRIPTION_UPDATED_INVITATION,
    EVENT_NOTIF_SUBJECT_PREFIX_CANCELLED:
        NOTIFICATION_DESCRIPTION_CANCELLED_INVITATION
}
