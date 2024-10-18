# pylint: disable=no-member
from allauth.account.models import EmailAddress
from django.conf import settings
from django.contrib.auth.models import Group
from django.utils import timezone

from auth import constants, models
from auth.token import RestoreAccountTokenGenerator
from company import models as company_models
from company import utils
from job_seeker import models as js_models
from leet import emaillib, enums
from notification_center import models as notif_models
from permission import utils as permission_utils


class UserAccountService:

    def __init__(self, user):
        self.user = user

    def soft_delete_user_account(self, reason=None):
        self.user.is_active = False
        self.user.deletion_reason, _ = (
            models.DeletionReason.objects.update_or_create(
                user=self.user,
                defaults={
                    'text': reason
                }
            )
        )
        self.user.save()
        if hasattr(self.user, 'job_seeker'):
            self.soft_delete_job_seeker_profile(self.user.job_seeker)
        self.send_restore_account_email(
            constants.ACCOUNT_WAS_DELETED_TEMPLATE_NAME)

    @staticmethod
    def soft_delete_job_seeker_profile(job_seeker):
        job_seeker.is_deleted = True
        job_seeker.deleted_at = timezone.now()
        job_seeker.save()

    def send_restore_account_email(self, template_name):
        token = RestoreAccountTokenGenerator().make_token(self.user)
        url = settings.RECOVER_ACCOUNT_TEMPLATE_URL.format(
            http=settings.HTTP_SCHEME,
            id=self.user.id,
            token=token,
            domain_name=settings.DOMAIN_NAME
        )
        context = {
            'url': url,
            'user': self.user,
            'domain_name': settings.DOMAIN_NAME
        }
        emaillib.send_email(template_name, [self.user.email], context)

    def restore_user_account(self, password):
        self.user.is_active = True
        self.user.deletion_reason.delete()
        self.user.set_password(password)
        self.user.save()
        if hasattr(self.user, 'job_seeker'):
            self.restore_job_seeker_profile(self.user.job_seeker)

    @staticmethod
    def restore_job_seeker_profile(job_seeker):
        job_seeker.is_deleted = False
        job_seeker.deleted_at = None
        job_seeker.save()

    def activate_invited_company_user(self, password):
        self.user.is_active = True
        self.user.set_password(password)
        self.user.save()
        self.user.company_user.status = enums.CompanyUserStatusEnum.ACTIVE.name
        self.user.company_user.save()
        EmailAddress.objects.filter(user=self.user).update(verified=True)


def create_job_seeker(user, is_password_set=True):
    js_group = Group.objects.get_by_natural_key(
        enums.AuthGroupsEnum.JOB_SEEKER.value)
    js_group.user_set.add(user)

    user.job_seeker = js_models.JobSeeker.objects.create(
        user=user, is_password_set=is_password_set)
    notif_types = notif_models.NotificationType.objects.filter(
        groups__id=js_group.id)
    user.subscribed_notifications.add(*notif_types)
    return user


def create_company_user(user, company, is_owner):
    if isinstance(company, str):
        company = company_models.Company.objects.create(name=company)
    else:
        company = company

    cu_group = Group.objects.get_by_natural_key(
        enums.AuthGroupsEnum.COMPANY_USER.value)
    cu_group.user_set.add(user)

    user.company_user = company_models.CompanyUser.objects.create(
        user=user,
        company=company,
        status=enums.CompanyUserStatusEnum.ACTIVE.name
    )

    utils.set_viewed_candidates_statuses(user.company_user)
    notif_types = notif_models.NotificationType.objects.filter(
        groups__id=cu_group.id)
    user.subscribed_notifications.add(*notif_types)

    if is_owner:
        permission_utils.add_permission_initial_company_user(user)

    user.save()
    return user
