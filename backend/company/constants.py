# pylint: disable=no-member
from leet import enums


MAX_COUNT_OF_COMPANY_USERS = 10

INVALID_RANGE_DATE_FILTER_ERROR_MESSAGE = 'Invalid `range_date` value.'

COMPANY_USER_CREATE_SUCCESS_MESSAGE = (
    'Your invitation has been sent successfully!'
)

USER_CAN_NOT_UPDATE_HIS_STATUS_ERROR = 'User can not update his status.'
CAN_NOT_UPDATE_STATUS_FOR_NEW_USER_ERROR = (
    'Can not update status for new user.'
)
CAN_NOT_DISABLE_PERMISSION_GROUP_ERROR = (
    "You can't save this account without '{0}' "
    "permission as there should be at least one user with this "
    "permission within the company"
)

CAN_NOT_DELETE_OWN_ACCOUNT = 'You can not delete your account.'


COMPANY_USER_WITH_CERTAIN_EMAIL_EXISTS = (
    'There is deleted user with certain email in company.'
)

NO_DELETED_COMPANY_USERS_ERROR = (
    'There are no deleted company users with certain email.'
)

INVITED_COMPANY_USER_TEMPLATE_NAME = 'invited_user.html'
RESTORED_COMPANY_USER_TEMPLATE_NAME = 'restored_company_user.html'

AVAILABLE_STATUSES_FOR_UPDATE = [
    enums.CompanyUserStatusEnum.ACTIVE.name,
    enums.CompanyUserStatusEnum.DISABLED.name
]

OUT_OF_PROFILE_VIEWS_ERROR = (
    'You are out of profile views. Update your subscription to purchase '
    'this profile.'
)

JOB_SEEKER_ALREADY_PURCHASED_ERROR = (
    'You can not purchase already purchased job seeker.'
)

PROFILE_IS_HIDDEN_ERROR = 'Profile is hidden.'
