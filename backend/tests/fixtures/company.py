import http

import pytest
from django.contrib.auth import get_user_model
from faker import Faker

from auth import services
from company import models as c_models
from leet import enums
from tests import constants, api_requests, utils
from tests.factories.address import create_address
from tests.factories.auth import create_base_user

User = get_user_model()
fake = Faker()


@pytest.fixture
def company_user_base_data():
    return {
        'email': constants.COMPANY_USER_EMAIL,
        'first_name': constants.COMPANY_USER_FIRST_NAME,
        'last_name': constants.COMPANY_USER_LAST_NAME,
        'password': constants.DEFAULT_PASSWORD
    }


@pytest.fixture
def company_base_data():
    return {
        'name': 'first Company',
        'description': 'description',
        'phone': fake.phone_number(),
        'fax': fake.msisdn(),
        'website': fake.url(),
        'email': utils.get_unique_company_email(),
    }


@pytest.fixture
def company_user(db, company_user_base_data, company_base_data):
    user = create_base_user(**company_user_base_data)
    company = c_models.Company.objects.create(**company_base_data)
    company.address = create_address()
    company.save()
    user = services.create_company_user(user, company, is_owner=True)
    return user.company_user


@pytest.fixture
def company_2_user(db, company_user_base_data, company_base_data):
    data = company_user_base_data.copy()
    data['email'] = '{}{}'.format('second', data['email'])
    data['first_name'] = '{}{}'.format('second', data['first_name'])
    data['last_name'] = '{}{}'.format('second', data['last_name'])
    user = create_base_user(**data)
    data = company_base_data.copy()
    data['name'] = 'second Company'
    company = c_models.Company.objects.create(**data)
    company.address = create_address()
    company.save()
    user = services.create_company_user(user, company, is_owner=True)
    return user.company_user


@pytest.fixture
def company_draft_user(db, company_user_base_data, company_base_data):
    data = company_user_base_data.copy()
    data['email'] = '{}{}'.format('draft', data['email'])
    data['first_name'] = '{}{}'.format('draft', data['first_name'])
    data['last_name'] = '{}{}'.format('draft', data['last_name'])
    user = create_base_user(**data)
    data = company_base_data.copy()
    data['name'] = 'draft Company'
    company = c_models.Company.objects.create(**data)
    user = services.create_company_user(user, company, is_owner=True)
    return user.company_user


@pytest.fixture
def permissions_groups(company_user_client):
    resp = api_requests.get_permissions_groups(company_user_client)
    assert resp.status_code == http.HTTPStatus.OK
    result_for_tests = []
    for group in resp.json():
        for i in group['permissions']:
            result_for_tests.append({
                'id': i['id'],
                'name': i['name']
            })
    return result_for_tests


@pytest.fixture
def invited_company_user_data(permissions_groups):
    return {
        'last_name': 'new' + constants.COMPANY_USER_LAST_NAME,
        'first_name': 'new' + constants.COMPANY_USER_FIRST_NAME,
        'email': 'unique@mail.com',
        'permissions_groups': [i['id'] for i in permissions_groups]
    }


@pytest.fixture
def new_company_user(
        company_user_client, invited_company_user_data, mailoutbox):
    """Return creds for finishing to sign up and company_user_id and email."""
    mailoutbox.clear()
    resp = api_requests.create_company_user(
        company_user_client,
        invited_company_user_data)
    assert resp.status_code == http.HTTPStatus.CREATED
    resp = api_requests.get_company_users(company_user_client)
    assert resp.status_code == http.HTTPStatus.OK
    company_user = next(
        i for i in resp.json()['results']
        if i['status'] == enums.CompanyUserStatusEnum.NEW.name)
    token, user_id = utils.find_account_link_in_email(mailoutbox[0])
    user_full_name = ' '.join([
        company_user['user']['first_name'],
        company_user['user']['last_name']
    ])
    return {
        'id': company_user['id'],
        'email': company_user['user']['email'],
        'full_name': user_full_name,
        'token': token,
        'user': user_id,
        'new_password': constants.DEFAULT_PASSWORD,
        'new_password_confirm': constants.DEFAULT_PASSWORD
    }


@pytest.fixture
def active_company_user(
        company_user_client, anonym_client, new_company_user):
    """Return invited company user with status 'Active'"""
    data = new_company_user
    resp = api_requests.signup_invited_company_user(
        anonym_client,
        data)
    assert resp.status_code == http.HTTPStatus.OK
    resp = api_requests.get_company_users(company_user_client)
    assert resp.status_code == http.HTTPStatus.OK
    company_user = next(
        i for i in resp.json()['results']
        if i['user']['pk'] == int(new_company_user['user']))
    return company_user


@pytest.fixture
def disabled_company_user(
        company_user_client, active_company_user,
        invited_company_user_data):
    data = invited_company_user_data.copy()
    data['status'] = enums.CompanyUserStatusEnum.DISABLED.name
    resp = api_requests.edit_company_user(
        company_user_client,
        active_company_user['id'],
        data)
    assert resp.status_code == http.HTTPStatus.OK
    return resp.json()


@pytest.fixture
def deleted_company_user(company_user_client, active_company_user):
    resp = api_requests.delete_company_user(
        company_user_client,
        active_company_user['id'])
    assert resp.status_code == http.HTTPStatus.NO_CONTENT
    return {
        'id': active_company_user['id'],
        'email': active_company_user['user']['email']
    }


@pytest.fixture
def company_draft(company_draft_user):
    return company_draft_user.company


@pytest.fixture
def company(company_user):
    return company_user.company


@pytest.fixture()
def company_with_photo(company, fake_photo, company_user_client):
    data = {'photo': fake_photo}
    resp = api_requests.upload_company_photo(
        company_user_client,
        company.id,
        data)
    assert resp.status_code == http.HTTPStatus.OK
    assert 'photo' in resp.json()
    return company


@pytest.fixture
def company_2(company_2_user):
    return company_2_user.company


@pytest.fixture
def companies_list(company, company_2):
    return [company, company_2]
