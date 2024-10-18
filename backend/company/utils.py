# pylint: disable=no-member
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import models as auth_models
from django.contrib.auth.tokens import default_token_generator

from leet import emaillib
from leet import enums
from leet import models as leet_models
from notification_center import models as notif_models
from permission import constants
from permission import utils

User = get_user_model()


def restore_company_user(user):
    user.company_user.is_active = True
    user.company_user.status = enums.CompanyUserStatusEnum.NEW.name
    user.company_user.save()
    return user.company_user


# TODO (m.nizovtsova): implement one method for company user creation,
# remove this functionality from auth module and use current
def create_or_restore_company_user(data, company, request):
    perms_groups = data.pop('permissions_groups')
    email = data.pop('email')
    username = get_adapter().generate_unique_username()
    data.update({'username': username, 'is_active': True})

    user, created = User.objects.get_or_create(
        email=email,
        defaults=data)
    cu_group = auth_models.Group.objects.get_by_natural_key(
        enums.AuthGroupsEnum.COMPANY_USER.value)
    if created:
        setup_user_email(request, user, [])
        company_user = company.company_users.create(user=user)
        cu_group.user_set.add(user)
    else:
        company_user = restore_company_user(user)

    set_viewed_candidates_statuses(company_user)
    notif_types = notif_models.NotificationType.objects.filter(
        groups__id=cu_group.id)
    user.subscribed_notifications.add(*notif_types)

    utils.add_permission_company_user(user, perms_groups)
    update_subscription_permissions(user)
    return company_user, created


def update_subscription_permissions(user):
    company = user.company_user.company
    active_subscription = company.customer.subscriptions.filter(
        status=enums.SubscriptionStatusEnum.ACTIVE.name).first()
    if active_subscription and not active_subscription.plan.price:
        utils.delete_permissions_for_user_list(
            [user], constants.STARTER_SUBSCRIPTION_RESTRICTED_PERMS,
            enums.CustomPermissionReasonEnum.SUBSCRIPTION_LIMIT.name)


def _update_user_fields(user, data):
    user.last_name = data['last_name']
    user.first_name = data['first_name']

    user.groups.clear()
    utils.add_permission_company_user(
        user,
        data['permissions_groups'])

    user.save()


def _update_company_user_fields(company_user, data):
    company_user.status = data.get('status', company_user.status)
    company_user.save()


def update_company_user(company_user, data):
    _update_company_user_fields(company_user, data)
    _update_user_fields(company_user.user, data)
    return company_user


def send_invited_user_email(
        template_name, invited_user, company_user):
    token = default_token_generator.make_token(invited_user.user)
    url = settings.INVITED_COMPANY_USER_TEMPLATE_URL.format(
        http=settings.HTTP_SCHEME,
        domain_name=settings.DOMAIN_NAME,
        id=invited_user.user.id,
        token=token)
    context = {
        'invited_user': invited_user.user,
        'company_user': company_user,
        'domain_name': settings.DOMAIN_NAME,
        'url': url
    }
    emaillib.send_email(template_name, [invited_user.user.email], context)


def get_count_active_and_new_company_users(company):
    return (company.company_users
                   .exclude(
                       status=enums.CompanyUserStatusEnum.DISABLED.name)
                   .count())


def soft_delete_company_user(company_user):
    company_user.is_active = False
    company_user.user.is_active = False
    company_user.save()
    company_user.user.save()
    company_user.user.emailaddress_set.all().update(verified=False)


def is_deleted_company_user(email, company):
    user = User.objects.filter(
        is_active=False,
        email=email,
        company_user__company=company,
        company_user__is_active=False)
    return user.exists()


def set_viewed_candidates_statuses(company_user):
    viewed_statuses = leet_models.CandidateStatus.objects.all()
    company_user.candidate_statuses.add(*viewed_statuses)
    company_user.save()
    return company_user
