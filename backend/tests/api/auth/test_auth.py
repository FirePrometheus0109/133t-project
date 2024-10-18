import http
import re

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model, models

from auth import constants as auth_constants
from leet import enums
from permission.utils import get_all_user_permissions_qs
from tests import api_requests
from tests import constants
from tests import utils
from tests import validators
from tests.api.auth import constants as ta_constants

SUCCESSFUL_LOGOUT = 'Successfully logged out.'
NEW_PASSWORD = 'n3w_aWe$ome_Passw0rd'
USER = get_user_model()


class TestUserAuthApi:

    def test_user_sign_up_email_not_valid_length(
            self, anonym_client, user_data):
        prefix = '@gmail.com'
        user_data['email'] = ''.join('a' for i in range(256 - len(prefix) + 1))
        user_data['email'] += prefix
        resp = api_requests.signup(anonym_client, user_data)
        emsg = auth_constants.MAX_LENGTH_OF_EMAIL_ADDRESS_ERROR.format(
            settings.MAX_EMAIL_LENGTH)
        validators.validate_error_message(resp, emsg, 'email')

    def test_user_isnt_created_with_incorrect_password(
            self, anonym_client, user_data, mailoutbox):
        user_data['password1'] = 'wrong'
        user_data['password2'] = 'wrong'
        resp = api_requests.signup(anonym_client, user_data)
        assert resp.status_code == http.HTTPStatus.BAD_REQUEST
        assert mailoutbox == []

    def test_user_isnt_passwords_dont_match(
            self, anonym_client, user_data, mailoutbox):
        user_data['password2'] = 'Othervalidpass2'
        resp = api_requests.signup(anonym_client, user_data)
        assert resp.status_code == http.HTTPStatus.BAD_REQUEST
        assert mailoutbox == []

    def test_user_isnt_created_with_incorrect_email(
            self, anonym_client, user_data, mailoutbox):
        user_data['email'] = 'wrong'
        resp = api_requests.signup(anonym_client, user_data)
        assert resp.status_code == http.HTTPStatus.BAD_REQUEST
        assert mailoutbox == []

    def test_user_sign_up_success(
            self, anonym_client, user_data, mailoutbox):
        assert mailoutbox == []
        resp = api_requests.signup(anonym_client, user_data)
        assert resp.status_code == http.HTTPStatus.CREATED
        assert len(mailoutbox) == 1
        user = USER.objects.get(email=user_data['email'])
        user_groups = user.groups.all()
        group = models.Group.objects.get(
            name=enums.AuthGroupsEnum.JOB_SEEKER.value)
        assert group in user_groups

    def test_user_login_success(self, anonym_client, verified_user_creds):
        resp = api_requests.login(anonym_client, verified_user_creds)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['token']

    def test_user_login_success_email_is_not_case_sensitive(
            self, anonym_client, verified_user_creds):
        data = verified_user_creds.copy()
        data['email'] = data['email'].capitalize()
        resp = api_requests.login(anonym_client, data)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['token']

    def test_user_fails_if_email_unverified(self, anonym_client, user_data):
        resp = api_requests.signup(anonym_client, user_data)
        assert resp.status_code == http.HTTPStatus.CREATED
        creds = {
            'email': user_data['email'],
            'password': user_data['password1']
        }
        resp = api_requests.login(anonym_client, creds)
        assert resp.status_code == http.HTTPStatus.BAD_REQUEST

    def test_user_login_invalid_pswd(self, anonym_client, verified_user_creds):
        creds = verified_user_creds.copy()
        creds['password'] = 'wrong'
        resp = api_requests.login(anonym_client, creds)
        assert resp.status_code == http.HTTPStatus.BAD_REQUEST

    def test_user_logout_success(self, anonym_client, verified_user_creds):
        resp = api_requests.login(anonym_client, verified_user_creds)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['token']

        resp = api_requests.logout(anonym_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['detail'] == SUCCESSFUL_LOGOUT

    def test_disabled_company_user_can_not_login(
            self, anonym_client, disabled_company_user):
        creds = {
            'email': disabled_company_user['user']['email'],
            'password': constants.DEFAULT_PASSWORD
        }
        resp = api_requests.login(anonym_client, creds)
        validators.validate_error_message(
            resp,
            auth_constants.DISABLED_COMPANY_USER_LOGIN_ERROR)


class TestResendRestoreUserApi:

    def test_resend_restore_account_email(self, anonym_client, mailoutbox, job_seeker):
        mailoutbox.clear()
        data = {'email': job_seeker.user.email}
        job_seeker.user.is_active = False
        job_seeker.user.save()
        resp = api_requests.resend_restore_account(anonym_client, data)
        assert resp.status_code == http.HTTPStatus.OK
        assert mailoutbox[0].subject == '[leet.teamcity.com]: Account Restore'
        assert mailoutbox[0].to == [job_seeker.user.email]

    def test_resend_restore_account_email_active_user(self, anonym_client, mailoutbox, job_seeker):
        mailoutbox.clear()
        data = {'email': job_seeker.user.email}
        resp = api_requests.resend_restore_account(anonym_client, data)
        emsg = "Active user can't be restored. Please reset password if you forgot it."
        validators.validate_error_message(resp, emsg)

    def test_resend_restore_account_email_bad_email(self, anonym_client, mailoutbox):
        data = {'email': 'bad@email.com'}
        resp = api_requests.resend_restore_account(anonym_client, data)
        validators.validate_error_message(
            resp, 'User with bad@email.com does not exist')

    def test_resend_restore_account_email_no_email(self, anonym_client, mailoutbox):
        data = {}
        resp = api_requests.resend_restore_account(anonym_client, data)
        validators.validate_error_message(
            resp, 'This field is required.', field='email')

class TestCompanyUserAuthApi:

    def test_company_user_user_created_with_appropriate_group(
            self, anonym_client, company_user_data, mailoutbox):
        assert mailoutbox == []
        resp = api_requests.signup_company_user(
            anonym_client, company_user_data)
        assert resp.status_code == http.HTTPStatus.CREATED
        assert len(mailoutbox) == 1

        group = models.Group.objects.get(
            name=enums.AuthGroupsEnum.COMPANY_USER.value)
        user = USER.objects.get(email=company_user_data['email'])
        assert group in user.groups.all()


class TestCurrentAuthenticatedUserApi:

    def test_get_current_authenticated_user(self, job_seeker_client,
                                            verified_user_creds):
        user_data = api_requests.get_current_user(job_seeker_client).json()
        expected_fields = ['first_name', 'last_name', 'email']
        for field in expected_fields:
            assert field in user_data

    def test_update_current_authenticated_user(self, job_seeker_client,
                                               verified_user_creds):
        current_user_resp = api_requests.get_current_user(job_seeker_client)
        assert current_user_resp.status_code == http.HTTPStatus.OK
        current_user_data = current_user_resp.json()

        data = {'first_name': 'foo', 'last_name': 'bar'}
        assert current_user_data.get('first_name') != data['first_name']
        assert current_user_data.get('last_name') != data['last_name']

        update_current_user_resp = api_requests.update_current_user(
            job_seeker_client, data=data)
        updated_user_data = update_current_user_resp.json()
        assert update_current_user_resp.status_code == http.HTTPStatus.OK
        assert updated_user_data.get('first_name') == data['first_name']
        assert updated_user_data.get('last_name') == data['last_name']

    def test_user_cant_update_user_email(
            self, verified_user_creds, job_seeker_client, job_seeker):
        data = {'email': 'good@email.ll'}
        assert job_seeker.user.email != data['email']

        update_current_user_resp = api_requests.update_current_user(
            job_seeker_client, data=data)
        updated_user_data = update_current_user_resp.json()
        assert update_current_user_resp.status_code == http.HTTPStatus.OK
        assert updated_user_data.get('email') != data['email']

    def test_obtain_only_authenticated_user_data(self, anonym_client):
        current_user_resp = api_requests.get_current_user(anonym_client)
        assert current_user_resp.status_code == http.HTTPStatus.UNAUTHORIZED


class TestChangeUserPassword:

    def test_change_user_valid_password(
            self, job_seeker_client, job_seeker, anonym_client):
        creds = {
            'email': job_seeker.user.email,
            'password': constants.DEFAULT_PASSWORD
        }
        data = {
            'old_password': constants.DEFAULT_PASSWORD,
            'new_password': NEW_PASSWORD
        }
        resp = api_requests.update_user_password(job_seeker_client, data)
        assert resp.status_code == http.HTTPStatus.OK

        login_invalid_creds = api_requests.login(anonym_client,
                                                 creds)
        assert login_invalid_creds.status_code == http.HTTPStatus.BAD_REQUEST

        creds.update({'password': NEW_PASSWORD})
        login_valid_creds = api_requests.login(anonym_client,
                                               creds)
        assert login_valid_creds.status_code == http.HTTPStatus.OK

    def test_change_user_wrong_old_password(self, job_seeker_client,
                                            verified_user_creds):
        data = {'old_password': 'wrong', 'new_password': NEW_PASSWORD}
        resp = api_requests.update_user_password(job_seeker_client, data)
        assert resp.status_code == http.HTTPStatus.BAD_REQUEST

    def test_change_user_password_invalid_format(self, job_seeker_client,
                                                 verified_user_creds):
        data = {
            'old_password': constants.DEFAULT_PASSWORD,
            'new_password': 'invalid'
        }
        resp = api_requests.update_user_password(job_seeker_client, data)
        assert resp.status_code == http.HTTPStatus.BAD_REQUEST


class TestResetUserPassword:
    def test_reset_password_success(self, anonym_client,
                            verified_user_creds, mailoutbox):
        mailoutbox.clear()
        resp = api_requests.reset_user_password(
            anonym_client, data={'email': verified_user_creds['email']}
        )
        assert resp.status_code == http.HTTPStatus.OK
        assert len(mailoutbox) == 1
        new_password = '1Password123'
        token, uid = utils.find_account_link_in_email(mailoutbox[0])
        data = {
            'new_password': new_password,
            'new_password_confirm': new_password,
            'token': token,
            'uid': uid
        }
        resp = api_requests.reset_user_password_confirm(
            anonym_client, data)
        assert resp.status_code == http.HTTPStatus.OK

        login_data = {
            'email': verified_user_creds['email'],
            'password': new_password
        }
        resp = api_requests.login(anonym_client, login_data)
        assert resp.status_code == http.HTTPStatus.OK

    def test_reset_password_fails_when_invalid_token(
            self, anonym_client, verified_user_creds, mailoutbox):
        mailoutbox.clear()
        resp = api_requests.reset_user_password(
            anonym_client, data={'email': verified_user_creds['email']}
        )
        assert resp.status_code == http.HTTPStatus.OK
        assert len(mailoutbox) == 1
        new_password = '1Password123'
        _, uid = utils.find_account_link_in_email(mailoutbox[0])
        data = {
            'new_password': new_password,
            'new_password_confirm': new_password,
            'token': 'invalid_token',
            'uid': uid
        }
        resp = api_requests.reset_user_password_confirm(
            anonym_client, data)
        assert resp.status_code == http.HTTPStatus.BAD_REQUEST
        emsg = 'Invalid value'
        validators.validate_error_message(resp, emsg, 'token')

    def test_reset_user_password__email_length(self, anonym_client):
        resp = api_requests.reset_user_password(
            anonym_client,
            data={'email': ta_constants.VALID_EMAIL_256_CHARACTERS})

        assert resp.status_code == http.HTTPStatus.OK


class TestJobSeekerDeleteRestoreAccountApi:

    def test_job_seeker_delete_success(
            self, job_seeker_client, job_seeker, mailoutbox):
        mailoutbox.clear()
        resp = api_requests.delete_account(
            job_seeker_client,
            data={'text': 'Bla-bla-bla'}
        )
        assert resp.status_code == http.HTTPStatus.OK
        user = USER.objects.get(email=job_seeker.user.email)
        job_seeker.refresh_from_db()
        assert not user.is_active
        assert job_seeker.is_deleted
        assert len(mailoutbox) == 1

    def test_job_seeker_cant_login_when_account_is_deleted(
            self, job_seeker_client, job_seeker, anonym_client, mailoutbox):
        resp = api_requests.delete_account(
            job_seeker_client,
            data={'text': 'Bla-bla-bla'}
        )
        assert resp.status_code == http.HTTPStatus.OK
        mailoutbox.clear()
        resp = api_requests.login(
            anonym_client,
            data={
                'email': job_seeker.user.email,
                'password': constants.DEFAULT_PASSWORD
            }
        )
        emsg = auth_constants.LOGIN_JOB_SEEKER_DELETED_ACCOUNT_ERROR.format(
            job_seeker.user.email)
        validators.validate_error_message(resp, emsg)
        assert len(mailoutbox) == 1

    def test_job_seeker_delete_sends_link(
            self, job_seeker_client, job_seeker, mailoutbox):
        mailoutbox.clear()
        resp = api_requests.delete_account(
            job_seeker_client,
            data={'text': 'Bla-bla-bla'}
        )
        assert resp.status_code == http.HTTPStatus.OK
        mail_content = mailoutbox[0].body
        search = re.search('<a href="(.+)">', mail_content)
        assert search

    def test_job_seeker_restore_account_success(
            self, job_seeker_client, job_seeker, mailoutbox, anonym_client):
        mailoutbox.clear()
        resp = api_requests.delete_account(
            job_seeker_client,
            data={'text': 'Bla-bla-bla'}
        )
        assert resp.status_code == http.HTTPStatus.OK
        token, user_id = utils.find_account_link_in_email(mailoutbox[0])
        resp = api_requests.restore_account(
            anonym_client,
            data={
                'token': token,
                'user': user_id,
                'new_password': NEW_PASSWORD
            }
        )
        assert resp.status_code == http.HTTPStatus.OK
        resp = api_requests.login(
            anonym_client,
            data={
                'email': job_seeker.user.email,
                'password': NEW_PASSWORD
            }
        )
        assert resp.status_code == http.HTTPStatus.OK

    def test_job_seeker_cant_restore_account_with_invalid_token(
            self, job_seeker_client, job_seeker, mailoutbox, anonym_client):
        resp = api_requests.delete_account(
            job_seeker_client,
            data={'text': 'Bla-bla-bla'}
        )
        assert resp.status_code == http.HTTPStatus.OK
        resp = api_requests.restore_account(
            anonym_client,
            data={
                'token': "Invalid token",
                'user': job_seeker.user.id,
                'new_password': NEW_PASSWORD
            }
        )
        emsg = 'Invalid token.'
        validators.validate_error_message(resp, emsg)

    def test_max_length_text_other_reason(self, job_seeker_client, job_seeker):
        data = {
            'text': ''.join(['a' for _ in range(2001)])
            }
        resp = api_requests.delete_account(job_seeker_client, data=data)
        assert resp.status_code == http.HTTPStatus.BAD_REQUEST
        assert resp.json()['field_errors']['text']


class TestInvitedCompanyUserSignUp:

    def test_sign_up_invited_company_user(
            self, anonym_client, new_company_user):
        data = new_company_user
        resp = api_requests.signup_invited_company_user(
            anonym_client,
            data)
        assert resp.status_code == http.HTTPStatus.OK
        data = {
            'password': constants.DEFAULT_PASSWORD,
            'email': new_company_user['email']
        }
        resp = api_requests.login(anonym_client, data)
        assert resp.status_code == http.HTTPStatus.OK

    def test_sign_up_invited_company_user_passwords_dont_match(
            self, anonym_client, new_company_user):
        data = new_company_user.copy()
        data['new_password'] = NEW_PASSWORD
        resp = api_requests.signup_invited_company_user(anonym_client, data)
        emsg = auth_constants.PASSWORDS_DONT_MATCH_ERROR
        validators.validate_error_message(resp, emsg)

    def test_restore_deleted_company_user_account(
            self, anonym_client, company_user_client,
            deleted_company_user, mailoutbox, invited_company_user_data):
        mailoutbox.clear()
        resp = api_requests.restore_company_user(
            company_user_client,
            invited_company_user_data)
        assert resp.status_code == http.HTTPStatus.OK
        token, user_id = utils.find_account_link_in_email(mailoutbox[0])
        data = {
            'email': invited_company_user_data['email'],
            'token': token,
            'user': user_id,
            'new_password': constants.DEFAULT_PASSWORD,
            'new_password_confirm': constants.DEFAULT_PASSWORD
        }
        resp = api_requests.signup_invited_company_user(
            anonym_client,
            data)
        assert resp.status_code == http.HTTPStatus.OK
        mailoutbox.clear()
        data = {
            'password': constants.DEFAULT_PASSWORD,
            'email': invited_company_user_data['email']
        }
        resp = api_requests.login(anonym_client, data)
        assert len(mailoutbox) == 0
        assert resp.status_code == http.HTTPStatus.OK


class TestAllPermissions:

    @pytest.mark.parametrize(('client',), (
        (
            'company_user_client',
        ),
        (
            'job_seeker_client',
        )
    ))
    def test_get_all_permissions(self, request, client):
        client = request.getfixturevalue(client)
        resp = api_requests.get_all_permissions(client)
        assert resp.status_code == http.HTTPStatus.OK
        assert len(resp.json()) == models.Permission.objects.count()

    @pytest.mark.parametrize(('client', 'user'), (
        (
            'company_user_client',
            'company_user'
        ),
        (
            'job_seeker_client',
            'job_seeker'
        )
    ))
    def test_get_all_user_permissions(self, request, client, user):
        client = request.getfixturevalue(client)
        user = request.getfixturevalue(user)
        resp = api_requests.get_all_user_permissions(client)
        assert resp.status_code == http.HTTPStatus.OK
        assert len(resp.json()) == get_all_user_permissions_qs(user.user).count()

    @pytest.mark.parametrize(('api_request',), (
        (
            api_requests.get_all_permissions,
        ),
        (
            api_requests.get_all_user_permissions,
        )
    ))
    def test_unauthorized_user_can_not_see_permissions(
            self, api_request, anonym_client):
        resp = api_request(anonym_client)
        assert resp.status_code == http.HTTPStatus.UNAUTHORIZED


class TestLoginToBannedAccount:

    @pytest.mark.parametrize(('user_obj',), (
        (
            'job_seeker',
        ),
        (
            'company_user',
        ),
    ))
    def test_banned_user_cant_login(
            self, request, anonym_client, user_obj):
        user_obj = request.getfixturevalue(user_obj)
        creds = {
            'email': user_obj.user.email,
            'password': constants.DEFAULT_PASSWORD
        }
        # make sure we can actually login with this creds
        resp = api_requests.login(anonym_client, creds)
        assert resp.status_code == http.HTTPStatus.OK
        utils.ban_entity(user_obj)

        resp = api_requests.login(anonym_client, creds)
        emsg = auth_constants.USER_BANNED_ERROR
        validators.validate_error_message(resp, emsg)

    def test_company_user_cant_login_if_company_is_banned(
            self, company_user, anonym_client):
        assert company_user.ban_status != enums.BanStatusEnum.BANNED
        utils.ban_entity(company_user.company)
        creds = {
            'email': company_user.user.email,
            'password': constants.DEFAULT_PASSWORD
        }
        resp = api_requests.login(anonym_client, creds)
        emsg = auth_constants.COMPANY_BANNED_ERROR
        validators.validate_error_message(resp, emsg)


class TestSetPasswordForSocialLoginUsers:

    @pytest.mark.parametrize(('client', 'email'), (
            (
                    'google_login_client',
                    ta_constants.GOOGLE_EMAIL
            ),
            (
                    'fb_login_client',
                    ta_constants.FB_EMAIL
            ),
    ))
    def test_set_password_for_social_logined_user_success(
            self, request, client, email, anonym_client):
        client = request.getfixturevalue(client)
        resp = api_requests.set_user_password(
            client,
            data={
                'new_password': constants.DEFAULT_PASSWORD,
                'new_password_confirm': constants.DEFAULT_PASSWORD
            }
        )
        assert resp.status_code == http.HTTPStatus.OK
        assert (resp.json()['detail']
                == auth_constants.USER_PASSWORD_SET_SUCCESS_MESSAGE)

        creds = {
            'email': email,
            'password': constants.DEFAULT_PASSWORD
        }
        resp = api_requests.login(anonym_client, creds)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['user']['job_seeker']['is_password_set'] is True
        # test set_password endpoint isn't available anymore
        resp = api_requests.set_user_password(client, data={})
        assert resp.status_code == http.HTTPStatus.FORBIDDEN
