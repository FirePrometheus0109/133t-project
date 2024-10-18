from allauth import utils
from allauth.account import adapter
from allauth.socialaccount import adapter as soc_adapter
from allauth.socialaccount import models
from django import urls
from django.conf import settings
from django.contrib import auth
from django.core import exceptions
from django.utils import crypto

from auth import constants
from permission import utils as permission_utils

User = auth.get_user_model()


class BaseAllauthAdapter(adapter.DefaultAccountAdapter):

    def get_email_confirmation_url(self, request, emailconfirmation):
        """Overriden to customize url name"""
        template_url = settings.VERIFY_EMAIL_TEMPLATE_URL
        domain_name = settings.DOMAIN_NAME
        http_scheme = settings.HTTP_SCHEME
        return template_url.format(domain_name=domain_name,
                                   code=emailconfirmation.key,
                                   http=http_scheme)

    def respond_email_verification_sent(self, request, user):
        url = urls.reverse('auth:api_v1:account_email_verification_sent')
        return utils.build_absolute_uri(request, url)

    def generate_unique_username(self, *args, **kwargs):    # noqa
        username = crypto.get_random_string()
        while User.objects.filter(username=username):
            username = crypto.get_random_string()
        return username

    def is_open_for_signup(self, request):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)


class SocialAccountAdapter(soc_adapter.DefaultSocialAccountAdapter):

    def is_open_for_signup(self, request, sociallogin):
        return getattr(settings, "ACCOUNT_ALLOW_REGISTRATION", True)

    def pre_social_login(self, request, sociallogin):
        user = sociallogin.user
        if user.id:
            return

        user = User.objects.filter(email=user.email)
        # user with such email is already registered, create social account
        if user.exists():
            user = user.first()
            if permission_utils.is_company_user(user):
                raise exceptions.ValidationError(
                    constants.SOCIAL_SIGNUP_IS_NOT_ALLOWED
                )
            models.SocialAccount.objects.get_or_create(
                user=user,
                provider=sociallogin.account.provider,
                uid=sociallogin.account.uid)
            sociallogin.lookup()
        return
