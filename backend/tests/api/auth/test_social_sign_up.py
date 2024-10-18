import http

import pytest
from auth import constants
from tests import api_requests
from tests import validators


class TestSocialAuth:

    @pytest.mark.parametrize(('mock_resp', 'api_request'), (
        (
            'mock_facebook_response',
            api_requests.sign_up_facebook
        ),
        (
            'mock_google_response',
            api_requests.sign_up_google
        ),
    ))
    def test_sign_up_with_social_apps(
            self, request, mock_social_resp_errors,
            mock_resp, api_request, anonym_client, social_apps):
        request.getfixturevalue(mock_resp)
        data = {
            'access_token': 'mysecrettoken'
        }
        resp = api_request(anonym_client, data)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['user']['job_seeker'] is not None
        assert resp.json()['user']['job_seeker']['is_password_set'] is False
        assert resp.json()['user']['company'] is None

    @pytest.mark.parametrize(('user_fixture', 'mock_resp', 'api_request'), (
        (
            'user_with_fb_email',
            'mock_facebook_response',
            api_requests.sign_up_facebook
        ),
        (
            'user_with_google_email',
            'mock_google_response',
            api_requests.sign_up_google
        ),
    ))
    def test_connect_social_account_to_existing_success(
            self, request, mock_social_resp_errors,
            mock_resp, user_fixture, api_request, anonym_client, social_apps):
        request.getfixturevalue(mock_resp)
        request.getfixturevalue(user_fixture)
        data = {
            'access_token': 'mysecrettoken'
        }
        resp = api_request(anonym_client, data)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['user']['job_seeker'] is not None
        assert resp.json()['user']['company'] is None

    @pytest.mark.parametrize(('user_fixture', 'mock_resp', 'api_request'), (
            (
                    'company_user_with_fb_email',
                    'mock_facebook_response',
                    api_requests.sign_up_facebook
            ),
            (
                    'company_user_with_google_email',
                    'mock_google_response',
                    api_requests.sign_up_google
            ),
    ))
    def test_connect_social_account_to_company_user_fails(
            self, request, mock_social_resp_errors,
            mock_resp, user_fixture, api_request, anonym_client, social_apps):
        request.getfixturevalue(mock_resp)
        request.getfixturevalue(user_fixture)
        data = {
            'access_token': 'mysecrettoken'
        }
        resp = api_request(anonym_client, data)
        validators.validate_error_message(
            resp, constants.SOCIAL_SIGNUP_IS_NOT_ALLOWED)
