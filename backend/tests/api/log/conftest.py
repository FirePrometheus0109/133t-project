import http

import pytest

from tests import api_requests


@pytest.fixture
def js_logs_query_params(job_seeker):
    return {
            'ct_model': 'jobseeker',
            'object_id': job_seeker.id
        }


@pytest.fixture
def job_logs_query_params(job):
    return {
            'ct_model': 'job',
            'object_id': job['id']
        }


@pytest.fixture
def log(company_user_client, purchased_job_seeker, js_logs_query_params):
    resp = api_requests.get_company_logs(
        company_user_client,
        query_params=js_logs_query_params)
    assert resp.status_code == http.HTTPStatus.OK
    assert resp.json()['count'] == 1
    return resp.json()['results'][0]


@pytest.fixture
def deleted_job(
        company_user_client, job):
    """Deleted company job"""
    resp = api_requests.delete_job(
        company_user_client,
        job['id']
    )
    assert resp.status_code == http.HTTPStatus.NO_CONTENT
