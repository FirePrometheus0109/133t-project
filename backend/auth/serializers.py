# pylint: disable=abstract-method
from django.conf import settings
from django.contrib import auth
from django.contrib.auth import models as ca_models
from rest_auth import serializers as auth_serializers
from rest_auth.registration import serializers as rar_serializers
from rest_framework import fields
from rest_framework import serializers

from auth import constants
from auth import forms
from auth import models
from auth import services
from auth import validators
from company import serializers as company_serializers
from job_seeker import serializers as js_serializers
from leet import enums
from permission import utils as perm_utils

User = auth.get_user_model()


class EmailSerializer(serializers.Serializer):

    email = serializers.EmailField()


class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ca_models.Permission
        fields = (
            'id',
            'name',
            'codename'
        )


class BaseSignUpSerializer(rar_serializers.RegisterSerializer):

    email = fields.EmailField(
        max_length=256,
        error_messages={
            'max_length': constants.MAX_LENGTH_OF_EMAIL_ADDRESS_ERROR
        })
    username = fields.CharField(read_only=True)
    first_name = fields.CharField(max_length=255)
    last_name = fields.CharField(max_length=255)
    password1 = fields.CharField(write_only=True, min_length=8, max_length=32)

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username'),
            'password1': self.validated_data.get('password1'),
            'email': self.validated_data.get('email'),
            'first_name': self.validated_data.get('first_name'),
            'last_name': self.validated_data.get('last_name'),
        }


class CompanyUserSignUpSerializer(BaseSignUpSerializer):
    company_name = fields.CharField(max_length=255)

    def custom_signup(self, request, user):
        company_name = self.validated_data.get('company_name')
        return services.create_company_user(
            user,
            company_name,
            is_owner=True
        )


class JobSeekerSignUpSerializer(BaseSignUpSerializer):

    def custom_signup(self, request, user):
        return services.create_job_seeker(user)


class UserDetailsSerializer(auth_serializers.UserDetailsSerializer):
    is_profile_draft = fields.SerializerMethodField()
    job_seeker = fields.SerializerMethodField()
    company = fields.SerializerMethodField()
    permissions = fields.SerializerMethodField()

    class Meta(auth_serializers.UserDetailsSerializer.Meta):
        fields = auth_serializers.UserDetailsSerializer.Meta.fields + (
            'is_profile_draft', 'job_seeker', 'company', 'permissions')

    @staticmethod
    def get_permissions(user):
        """Return all permissions of user."""
        perms = perm_utils.get_all_user_permissions_qs(user)
        return PermissionSerializer(perms, many=True).data

    @staticmethod
    def get_is_profile_draft(user):
        is_company_user = user.groups.filter(
            name=enums.AuthGroupsEnum.COMPANY_USER.value)  # noqa
        if is_company_user:
            company = user.company_user.company
            return not all([company.address, company.phone])
        return not all([user.first_name, user.last_name, user.email])

    @staticmethod
    def get_company(user):
        if hasattr(user, 'company_user'):
            return company_serializers.CompanySerializer(
                user.company_user.company).data
        return None

    def get_job_seeker(self, user):
        if hasattr(user, 'job_seeker'):
            return js_serializers.JobSeekerSerializer(
                user.job_seeker, context=self.context).data
        return None


class DeletionReasonSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.DeletionReason
        fields = (
            'text',
            'user',
        )
        read_only_fields = ('user',)


class UserIdPasswordAndTokenSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(is_active=False)
    )
    token = serializers.CharField()
    new_password = serializers.CharField()

    @staticmethod
    def validate_new_password(password):
        validators.BaseCharacterPasswordValidator.validate(password)
        return password

    def validate(self, attrs):
        user = attrs['user']
        token = attrs['token']
        validators.validate_account_token(user, token)
        return attrs


class InvitedCompanyUserSignUpSerializer(UserIdPasswordAndTokenSerializer):

    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(job_seeker__isnull=True))
    new_password_confirm = serializers.CharField()

    @staticmethod
    def validate_new_password_confirm(password):
        validators.BaseCharacterPasswordValidator.validate(password)
        return password

    def validate(self, attrs):
        password = attrs['new_password']
        password_confirm = attrs['new_password_confirm']
        validators.validate_password_and_paswsword_confirm(
            password, password_confirm)
        return super().validate(attrs)


class UserUpdateDetailSerializer(auth_serializers.UserDetailsSerializer):

    class Meta(auth_serializers.UserDetailsSerializer.Meta):
        read_only_fields = (
            auth_serializers.UserDetailsSerializer.Meta.read_only_fields
            + ('username',)
        )


class UserPasswordChangeSerializer(auth_serializers.PasswordChangeSerializer):
    new_password = serializers.CharField(max_length=128)

    set_password_form_class = forms.UserSetPasswordForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('new_password1')
        self.fields.pop('new_password2')

    def validate_old_password(self, value):
        invalid_password_conditions = (
            self.old_password_field_enabled,
            self.user,
            not self.user.check_password(value)
        )

        if all(invalid_password_conditions):
            raise serializers.ValidationError(
                constants.USER_PASSWORD_CHANGE_OLD_PASSWORD_ERROR)
        return value


class UserPasswordResetSerializer(auth_serializers.PasswordResetSerializer):
    password_reset_form_class = forms.PasswordResetForm

    @staticmethod
    def make_reset_password_url():
        url = settings.PASSWORD_RESET_TEMPLATE_URL.format(
            http=settings.HTTP_SCHEME,
            domain_name=settings.DOMAIN_NAME
        )
        return url

    def get_email_options(self):
        return {
            'subject_template_name':
                constants.EMAIL_CONFIRMATION_PASSWORD_RESET_SUBJECT,
            'email_template_name':
                constants.EMAIL_CONFIRMATION_PASSWORD_RESET_MESSAGE,
            'html_email_template_name':
                constants.EMAIL_CONFIRMATION_PASSWORD_RESET_MESSAGE,
            'extra_email_context': {
                'reset_password_url': self.make_reset_password_url()
            },
        }


class LoginSerializer(auth_serializers.LoginSerializer):
    """Company user with disabled status can not be login."""
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        user = auth.authenticate(**attrs)
        validators.validate_user_can_login(user)
        email = user.emailaddress_set.get(email=user.email)
        validators.validate_user_login_email(email)
        if perm_utils.is_company_user(user):
            validators.validate_user_ban_status(user.company_user)
            validators.validate_company_ban_status(user.company_user.company)
            validators.validate_company_user_status(user.company_user)
            validators.validate_company_user_isnt_disabled_by_subscription(
                user.company_user)
        elif perm_utils.is_job_seeker(user):
            validators.validate_user_ban_status(user.job_seeker)
        attrs['user'] = user
        return attrs


class PasswordResetConfirmSerializer(
        auth_serializers.PasswordResetConfirmSerializer):
    new_password = serializers.CharField(max_length=128)
    new_password_confirm = serializers.CharField(max_length=128)

    set_password_form_class = forms.UserResetPasswordForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('new_password1')
        self.fields.pop('new_password2')


class UserPasswordSetSerializer(auth_serializers.PasswordChangeSerializer):
    """
    Serializer that used for setting password after job seeker social login.
    Once password set job seeker can't use this endpoint anymore.
    """
    new_password = serializers.CharField(max_length=128)
    new_password_confirm = serializers.CharField(max_length=128)

    set_password_form_class = forms.UserSetPasswordForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_password_field_enabled = False
        self.fields.pop('new_password1')
        self.fields.pop('new_password2')
        self.fields.pop('old_password')

    def save(self):
        super().save()
        job_seeker = self.context['request'].user.job_seeker
        job_seeker.is_password_set = True
        job_seeker.save()
