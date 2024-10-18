# pylint: disable=no-member
import re

from django.conf import settings
from django.contrib import auth
from django.contrib.auth import validators
from django.core import exceptions

from auth import constants
from auth import token as auth_token
from leet import enums
from permission import utils as perm_utils

User = auth.get_user_model()


class UsernameValidator(validators.UnicodeUsernameValidator):
    """'@' removed from default Django regex to forbid '@' in username"""
    regex = r'^[\w.+-]+$'
    message = constants.USERNAME_HELP_MESSAGE


custom_username_validators = [UsernameValidator]


class BaseCharacterPasswordValidator:
    """
    Validate whether the password contains at least one lowercase letter,
    one uppercase letter and one digit.
    """
    @staticmethod
    def validate(password, user=None):  # pylint: disable=unused-argument
        if not re.match(
                getattr(settings, "VALIDATION_REGEXPS")['password_validator'],
                password):
            raise exceptions.ValidationError(
                constants.USER_PASSWORD_CHANGE_NEW_PASSWORD_ERROR,
                code='password_doesnt_contain_required_symbols')

    @staticmethod
    def get_help_text():
        return constants.USER_PASSWORD_CHANGE_NEW_PASSWORD_HELP_MESSAGE


def validate_account_token(user, token):
    if not auth_token.RestoreAccountTokenGenerator().check_token(user, token):
        raise exceptions.ValidationError(constants.INVALID_TOKEN_ERROR)


def validate_password_and_paswsword_confirm(password, password_confrim):
    if password != password_confrim:
        raise exceptions.ValidationError(constants.PASSWORDS_DONT_MATCH_ERROR)


def validate_company_user_status(company_user):
    if company_user.status == enums.CompanyUserStatusEnum.DISABLED.name:
        raise exceptions.ValidationError(
            constants.DISABLED_COMPANY_USER_LOGIN_ERROR)


def validate_company_user_isnt_disabled_by_subscription(company_user):
    if company_user.is_disabled_by_subscription:
        raise exceptions.ValidationError(
            constants.DISABLED_BECAUSE_OF_SUBSCRIPTION_LOGIN_ERROR)


def validate_user_ban_status(user):
    if user.ban_status == enums.BanStatusEnum.BANNED.name:
        raise exceptions.ValidationError(constants.USER_BANNED_ERROR)


def validate_company_ban_status(company):
    if company.ban_status == enums.BanStatusEnum.BANNED.name:
        raise exceptions.ValidationError(constants.COMPANY_BANNED_ERROR)


def validate_user_can_login(user):
    if user:
        if not user.is_active and perm_utils.is_job_seeker(user):
            emsg = constants.LOGIN_JOB_SEEKER_DELETED_ACCOUNT_ERROR
            raise exceptions.ValidationError(emsg.format(
                user.email
            ))
        elif not user.is_active:
            emsg = constants.LOGIN_COMPANY_USER_IS_NOT_ACTIVE_ERROR
            raise exceptions.ValidationError(emsg)
    else:
        emsg = constants.LOGIN_INVALID_CREDENTIALS_ERROR
        raise exceptions.ValidationError(emsg)


def validate_user_login_email(email):
    if not email.verified:
        emsg = constants.LOGIN_NOT_VERIFIED_EMAIL_ERROR
        raise exceptions.ValidationError(emsg)
