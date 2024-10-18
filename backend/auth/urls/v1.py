from django import urls
from rest_auth import views as ra_views
from rest_auth.registration import views as reg_views
from rest_framework_jwt import views as jwt_views

from auth import views

app_name = 'api_v1_auth'

urlpatterns = (
    urls.path(
        'api-token-verify/',
        jwt_views.verify_jwt_token
    ),
    urls.path(
        'api-token-refresh/',
        jwt_views.refresh_jwt_token
    ),
    urls.path(
        'login/',
        ra_views.LoginView.as_view(),
        name='login'
    ),
    urls.path(
        'logout/',
        ra_views.LogoutView.as_view(),
        name='logout'
    ),
    urls.path(
        'company-signup/',
        views.CompanyUserSignUpView.as_view(),
        name='company_signup'
    ),
    urls.path(
        'job-seeker-signup/',
        views.JobSeekerSignUpView.as_view(),

        name='job_seeker_signup'
    ),
    urls.path(
        'verify-email/',
        reg_views.VerifyEmailView.as_view(),

        name='account_email_verification_sent'
    ),
    urls.path(
        'user/',
        views.UserDetailView.as_view(),
        name='user'
    ),
    urls.path(
        'password/change/',
        views.PasswordChangeView.as_view(),

        name='password-change'
    ),
    urls.path(
        'password-reset/',
        ra_views.PasswordResetView.as_view(),
        name='password-reset'
    ),
    urls.path(
        'set-password/',
        views.SetPasswordView.as_view(),
        name='set-password'
    ),
    urls.path(
        'password-reset-confirm/',
        ra_views.PasswordResetConfirmView.as_view(),
        name='password-reset-confirm'),
    urls.path(
        'delete-account/',
        views.DeleteAccountView.as_view(),
        name='delete-account'
    ),
    urls.path(
        'restore-account/',
        views.RestoreAccountView.as_view(),
        name='restore-account'
    ),
    urls.path(
        'resend-restore-account-email/',
        views.ResendRestoreAccountEmailView.as_view(),
        name='resend-restore-account-email'
    ),
    urls.path(
        'invited-company-user-sign-up/',
        views.InvitedCompanyUserSignUpView.as_view(),
        name='invited-company-user-sign-up'
    ),
    urls.path(
        'permissions/',
        views.AllUserPermissionView.as_view(),
        name='permissions'
    ),
    urls.path(
        'all-permissions/',
        views.AllPermissionsView.as_view(),
        name='all-permissions'
    ),
    urls.path(
        'facebook/login/',
        views.FacebookLoginView.as_view(),
        name='fb-login'
    ),
    urls.path(
        'google/login/',
        views.GoogleLoginView.as_view(),
        name='google-login'
    ),
)
