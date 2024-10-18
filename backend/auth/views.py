from allauth.socialaccount.providers.facebook import views as fb_views
from allauth.socialaccount.providers.google import views as google_views
from django.contrib import auth
from django.contrib.auth import models
from rest_auth import views as auth_views
from rest_auth.registration import views as ra_views
from rest_framework import generics
from rest_framework import exceptions
from rest_framework import permissions as drf_permissions
from rest_framework import response
from rest_framework import status

from auth import constants
from auth import permissions
from auth import serializers
from auth import services
from permission import utils

User = auth.get_user_model()


class CompanyUserSignUpView(ra_views.RegisterView):
    serializer_class = serializers.CompanyUserSignUpSerializer


class JobSeekerSignUpView(ra_views.RegisterView):
    serializer_class = serializers.JobSeekerSignUpSerializer


class DeleteAccountView(generics.GenericAPIView):

    permission_classes = (drf_permissions.IsAuthenticated,)
    serializer_class = serializers.DeletionReasonSerializer
    queryset = User.objects.none()

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        reason = serializer.validated_data.get('text', '')
        services.UserAccountService(user).soft_delete_user_account(reason)
        return response.Response(status=status.HTTP_200_OK)


class RestoreAccountView(generics.GenericAPIView):

    permission_classes = (drf_permissions.AllowAny,)
    serializer_class = serializers.UserIdPasswordAndTokenSerializer
    queryset = User.objects.none()
    service_method = 'restore_user_account'

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        password = serializer.validated_data['new_password']
        service = services.UserAccountService(user)
        getattr(service, self.service_method)(password)
        return response.Response(status=status.HTTP_200_OK)


class ResendRestoreAccountEmailView(generics.GenericAPIView):

    permission_classes = (drf_permissions.AllowAny,)
    serializer_class = serializers.EmailSerializer
    queryset = User.objects.none()
    service_method = 'restore_user_account'

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise exceptions.ValidationError(
                f"User with {email} does not exist")
        if user.is_active:
            raise exceptions.ValidationError(
                "Active user can't be restored. "
                "Please reset password if you forgot it.")
        service = services.UserAccountService(user)
        service.send_restore_account_email(
            constants.RESTORE_ACCOUNT_TEMPLATE_NAME
        )
        return response.Response(status=status.HTTP_200_OK)


class InvitedCompanyUserSignUpView(RestoreAccountView):
    """
    View for finishing registration of new company user.

    post:
        Send user_id, token and passwords for finishing registration.\n
        Only for company users.
        Example request data:
            {
                "user": 1
                "token": "stringtoken",
                "new_password": "password",
                "new_password_confirm": "password",
            }
        Errors:
            Passwords don't match.
            Passwords are not valid.
        """

    serializer_class = serializers.InvitedCompanyUserSignUpSerializer
    service_method = 'activate_invited_company_user'


class UserDetailView(auth_views.UserDetailsView):
    serializer_class = serializers.UserUpdateDetailSerializer


class PasswordChangeView(auth_views.PasswordChangeView):
    serializer_class = serializers.UserPasswordChangeSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)  # noqa
        msg = constants.USER_PASSWORD_CHANGE_SUCCESS_MESSAGE
        response.data['detail'] = msg
        return response


class SetPasswordView(auth_views.PasswordChangeView):
    serializer_class = serializers.UserPasswordSetSerializer
    permission_classes = (
        drf_permissions.IsAuthenticated,
        permissions.JobSeekerSetPasswordWithoutOldPasswordPermission,
    )

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)  # noqa
        msg = constants.USER_PASSWORD_SET_SUCCESS_MESSAGE
        response.data['detail'] = msg
        return response


class AllPermissionsView(generics.ListAPIView):

    permission_classes = (drf_permissions.IsAuthenticated,)
    serializer_class = serializers.PermissionSerializer
    pagination_class = None

    def get_queryset(self):
        return models.Permission.objects.order_by('id')


class AllUserPermissionView(AllPermissionsView):

    def get_queryset(self):
        return utils.get_all_user_permissions_qs(
            self.request.user).order_by('id')


class CustomSocialLoginView(ra_views.SocialLoginView):
    """Base view for sign up job seekers with social accounts."""

    def post(self, request, *args, **kwargs):
        self.serializer = self.get_serializer(data=self.request.data)  # noqa
        self.serializer.is_valid(raise_exception=True)
        self.create_job_seeker()

        self.login()
        return self.get_response()  # noqa

    def create_job_seeker(self):
        self.user = self.serializer.validated_data['user']  # noqa
        if not utils.is_job_seeker(self.user):
            services.create_job_seeker(self.user, is_password_set=False)


class FacebookLoginView(CustomSocialLoginView):
    adapter_class = fb_views.FacebookOAuth2Adapter


class GoogleLoginView(CustomSocialLoginView):
    adapter_class = google_views.GoogleOAuth2Adapter
