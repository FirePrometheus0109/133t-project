import copy
import http

import pytest
from django.contrib import auth
from django.core import management

from tests import api_requests
from tests import clients
from tests import constants
from tests import utils
from tests.api.auth import constants as auth_constants

USER = auth.get_user_model()


@pytest.fixture
def user_data():
    return {
        'email': 'user@mail.com',
        'first_name': 'first',
        'last_name': 'last',
        'password1': constants.DEFAULT_PASSWORD,
        'password2': constants.DEFAULT_PASSWORD,
    }


@pytest.fixture
def verifed_user(anonym_client, user_data):
    resp = api_requests.signup(anonym_client, user_data)
    assert resp.status_code == http.HTTPStatus.CREATED
    anonym_client.logout()
    user = USER.objects.get(email='user@mail.com')
    utils.verify_email(user)
    return user


@pytest.fixture
def user_with_google_email(anonym_client, user_data):
    data = copy.deepcopy(user_data)
    data['email'] = auth_constants.GOOGLE_EMAIL
    resp = api_requests.signup(anonym_client, data)
    assert resp.status_code == http.HTTPStatus.CREATED
    anonym_client.logout()
    user = USER.objects.get(email=auth_constants.GOOGLE_EMAIL)
    utils.verify_email(user)
    return user


@pytest.fixture
def user_with_fb_email(anonym_client, user_data):
    data = copy.deepcopy(user_data)
    data['email'] = auth_constants.FB_EMAIL
    resp = api_requests.signup(anonym_client, data)
    assert resp.status_code == http.HTTPStatus.CREATED
    anonym_client.logout()
    user = USER.objects.get(email=auth_constants.FB_EMAIL)
    utils.verify_email(user)
    return user


@pytest.fixture
def company_user_with_google_email(anonym_client, company_user_data):
    data = copy.deepcopy(company_user_data)
    data['email'] = auth_constants.GOOGLE_EMAIL
    resp = api_requests.signup_company_user(anonym_client, data)
    assert resp.status_code == http.HTTPStatus.CREATED
    anonym_client.logout()
    user = USER.objects.get(email=auth_constants.GOOGLE_EMAIL)
    utils.verify_email(user)
    return user


@pytest.fixture
def company_user_with_fb_email(anonym_client, company_user_data):
    data = copy.deepcopy(company_user_data)
    data['email'] = auth_constants.FB_EMAIL
    resp = api_requests.signup_company_user(anonym_client, data)
    assert resp.status_code == http.HTTPStatus.CREATED
    anonym_client.logout()
    user = USER.objects.get(email=auth_constants.FB_EMAIL)
    utils.verify_email(user)
    return user


@pytest.fixture
def verified_user_creds(verifed_user):
    return {
        'email': verifed_user.email,
        'password': constants.DEFAULT_PASSWORD
    }


@pytest.fixture
def company_user_data(user_data):
    user_data['company_name'] = constants.COMPANY_NAME
    return user_data


@pytest.fixture
def mock_social_resp_errors(mocker):
    mockname = 'requests.models.Response.raise_for_status'
    fixture = mocker.patch(mockname, return_value=None)
    return fixture()


@pytest.fixture
def mock_facebook_response(mocker):
    mockname = 'requests.models.Response.json'
    json_data = {
        "id": "104494263942517",
        "email": auth_constants.FB_EMAIL,
        "name": "Elizabeth Alcadehcababd Qinsen",
        "first_name": "Elizabeth",
        "last_name": "Qinsen"
    }
    fixture = mocker.patch(mockname, return_value=json_data)
    return fixture()


@pytest.fixture
def mock_google_response(mocker):
    mockname = 'requests.models.Response.json'
    json_data = {
        "id": "1",
        "email": auth_constants.GOOGLE_EMAIL,
        "verified_email": True,
        "name": "testname",
        "given_name": "myname",
        "family_name": "myfamilyname",
        "link": "https://plus.google.com/1",
        "picture": "picture.jpg",
        "gender": "male",
        "locale": "en"
    }
    fixture = mocker.patch(mockname, return_value=json_data)
    return fixture()


@pytest.fixture
def social_apps():
    management.call_command('set_social_appid_and_secret')


@pytest.fixture
def google_login_client(mock_google_response, social_apps, mock_social_resp_errors):
    data = {
        'access_token': 'mysecrettoken'
    }
    client = clients.GoogleLoginClient()
    client.login(**data)
    return client


@pytest.fixture
def fb_login_client(mock_facebook_response, social_apps, mock_social_resp_errors):
    data = {
        'access_token': 'mysecrettoken'
    }
    client = clients.FacebookLoginClient()
    client.login(**data)
    return client
