import http

import pytest

from tests import api_requests


@pytest.fixture
def letter_template_data():
    return {
        'name': 'name',
        'subject': 'subject',
        'body': 'body'
    }


@pytest.fixture
def letter_template(
        company_user_client, letter_template_data,
        event_interview):
    data = letter_template_data.copy()
    data['category'] = event_interview['id']
    resp = api_requests.create_letter_template(company_user_client, data)
    assert resp.status_code == http.HTTPStatus.CREATED
    return resp.json()


@pytest.fixture
def letter_template_2(company_user_client, letter_template_data):
    data = {
        k: 'second {}'.format(v) for k, v in letter_template_data.items()
    }
    resp = api_requests.create_letter_template(company_user_client, data)
    assert resp.status_code == http.HTTPStatus.CREATED
    return resp.json()
