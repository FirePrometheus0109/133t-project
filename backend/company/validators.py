# pylint: disable=no-member
from rest_framework import exceptions

from company import constants
from company import utils
from leet import enums
from leet import services
from permission import constants as perms_constants
from subscription import constants as subscription_constants
from subscription import utils as subscription_utils

def _validate_count_company_users(company):
    err_msg_tmpl = subscription_constants.PLAN_NUMBER_OF_USERS_EXCEEDED_ERROR
    current_active_users_cnt = utils.get_count_active_and_new_company_users(company)
    active_subscription = subscription_utils.get_active_subscription(company)
    if active_subscription:
        plan_limit = active_subscription.plan.users_number
        error_message = err_msg_tmpl.format(plan_limit)
        if current_active_users_cnt >= plan_limit:
            raise exceptions.ValidationError(error_message)


def validate_count_company_users_for_create(company):
    """Max count of creating users is 10."""
    _validate_count_company_users(company)


def validate_count_company_users_for_update(company, edited_user, status):
    """
    It Can not change status of disabled user if in company 10 users
    with statuses 'NEW' or 'ACTIVE'.
    """
    disabled = enums.CompanyUserStatusEnum.DISABLED.name
    active = enums.CompanyUserStatusEnum.ACTIVE.name
    if edited_user.status == disabled and status == active:
        _validate_count_company_users(company)


def validate_company_user_is_not_deleted(email, company):
    if utils.is_deleted_company_user(email, company):
        raise exceptions.ValidationError(
            constants.COMPANY_USER_WITH_CERTAIN_EMAIL_EXISTS)


def validate_company_user_restore_email(email, company):
    if not utils.is_deleted_company_user(email, company):
        raise exceptions.ValidationError(
            constants.NO_DELETED_COMPANY_USERS_ERROR)


def validate_user_can_update_status(request_company_user, instance, status):
    """User can not change his status."""
    if (request_company_user.id == instance.id
            and instance.status != status):
        raise exceptions.ValidationError(
            constants.USER_CAN_NOT_UPDATE_HIS_STATUS_ERROR)


def validate_status_edited_user(edited_user):
    """User can not change status of company user with satus 'NEW'."""
    if edited_user.status == enums.CompanyUserStatusEnum.NEW.name:
        raise exceptions.ValidationError(
            constants.CAN_NOT_UPDATE_STATUS_FOR_NEW_USER_ERROR)


def validate_user_can_disable_permission_group(
        edited_user, company, permission_groups):
    """
    In company should be at least one user with permissions groups
    'Manage company users' or 'Manage Subscription plan'.
    """
    # for validating we need only two groups names
    control_groups = perms_constants.CAN_NOT_DISABLE_IF_ONLY_ONE_USER_IN_GROUP
    groups_names = [
        i.name for i in permission_groups
        if i.name in control_groups]

    if len(groups_names) == len(control_groups):
        return

    errors = []
    groups_names = set(control_groups) - set(groups_names)
    for group_name in groups_names:
        users = (company.company_users
                        .filter(user__groups__name=group_name))
        if users.count() == 1 and users[0] == edited_user:
            emsg = constants.CAN_NOT_DISABLE_PERMISSION_GROUP_ERROR.format(
                group_name)
            errors.append(emsg)
    if errors:
        raise exceptions.ValidationError(errors)


def validate_user_can_be_deleted(company_user, edited_user):
    if company_user == edited_user:
        emsg = {
            'non_field_errors': [constants.CAN_NOT_DELETE_OWN_ACCOUNT]
        }
        raise exceptions.ValidationError(emsg)


def validate_company_job_seeker_balance(company):
    if company.customer.balance.job_seekers_remain == 0:
        emsg = {
            'non_field_errors': [constants.OUT_OF_PROFILE_VIEWS_ERROR]
        }
        raise exceptions.ValidationError(emsg)


def validate_job_seeker_profile_is_public(job_seeker):
    if not job_seeker.is_public:
        raise exceptions.ValidationError({
            'non_field_errors': [constants.PROFILE_IS_HIDDEN_ERROR]
        })


def validate_job_seeker_is_not_purchased_or_applied(company, job_seeker):
    if services.is_job_seeker_purchased(job_seeker, company):
        raise exceptions.ValidationError({
            'non_field_errors': [
                constants.JOB_SEEKER_ALREADY_PURCHASED_ERROR]
        })
