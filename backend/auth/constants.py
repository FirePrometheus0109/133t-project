from django.conf import settings


USER_PASSWORD_CHANGE_SUCCESS_MESSAGE = (
    'Your password has been changed successfully.'
)

USER_PASSWORD_SET_SUCCESS_MESSAGE = (
    'Your password has been set successfully.'
)

USER_PASSWORD_CHANGE_OLD_PASSWORD_ERROR = (
    'You\'ve provided wrong password.'
)

USER_PASSWORD_CHANGE_NEW_PASSWORD_HELP_MESSAGE = (
    'Min 8 characters, min 1 uppercase and 1 lowercase letter, min 1 digit'
)

USER_PASSWORD_CHANGE_NEW_PASSWORD_ERROR = (
    'Password doesn\'t match password requirements.'
)

USERNAME_HELP_MESSAGE = (
    'Enter a valid username. This value may contain '
    'only letters, numbers, and ./+/-/_ characters.'
)

RESTORE_ACCOUNT_TEMPLATE_NAME = 'restore_account.html'

ACCOUNT_WAS_DELETED_TEMPLATE_NAME = 'account_was_deleted.html'

INVALID_TOKEN_ERROR = "Invalid token."

PASSWORDS_DONT_MATCH_ERROR = 'Password and confirm password should be match.'

DISABLED_COMPANY_USER_LOGIN_ERROR = (
    'This account is disabled. '
    'For more information contact your administrator.'
)

DISABLED_BECAUSE_OF_SUBSCRIPTION_LOGIN_ERROR = (
    'Your account is disabled because of limitations in the your subscription'
)

DEFAULT_DELETION_ACCOUNT_REASONS = (
    "I only needed to use this for a short period of time.",
    "I'm having to many technical issues.",
    "It's too complicated to use.",
    "I'll be back.",
)

MAX_LENGTH_OF_EMAIL_ADDRESS_ERROR = (
    'Max length Email address is {} characters.'.format(
        settings.MAX_EMAIL_LENGTH)
)

EMAIL_CONFIRMATION_PASSWORD_RESET_SUBJECT = (
    'email_confirmation_password_reset_subject.txt'
)

EMAIL_CONFIRMATION_PASSWORD_RESET_MESSAGE = (
    'email_confirmation_password_reset_message.txt'
)

COMPANY_BANNED_ERROR = 'Your company was banned. Please contact 133T'

USER_BANNED_ERROR = (
    'Your account was banned. Please contact administrator'
)

SET_SOCIAL_APPID_AND_SECRET_ERROR = (
    'Check your environment variables.\n'
    'For social providers are requeired next env vars:\n'
    'SOCIAL_AUTH_{provider name}_NAME. Value is in lower case.\n'
    'SOCIAL_AUTH_{provider name}_APP_ID.\n'
    'SOCIAL_AUTH_{provider name}_SECRET.\n'
)

SET_SOCIAL_APPID_AND_SECRET_SUCCESS = (
    '{} social application successfully created/updated.'
)

LOGIN_INVALID_CREDENTIALS_ERROR = 'Unable to log in with provided credentials.'
LOGIN_NOT_VERIFIED_EMAIL_ERROR = 'E-mail is not verified.'
LOGIN_COMPANY_USER_IS_NOT_ACTIVE_ERROR = 'User account is disabled.'
LOGIN_JOB_SEEKER_DELETED_ACCOUNT_ERROR = (
    'Your account has been deleted. '
    'Email has been sent to {} '
    'with further instructions to restore your account'
)

SOCIAL_SIGNUP_IS_NOT_ALLOWED = (
    'Signup with social media is not allowed.'
)
