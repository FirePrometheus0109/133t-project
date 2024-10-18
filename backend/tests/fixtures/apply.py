import http

import pytest

from leet import enums
from job import models as job_models
from tests import api_requests


@pytest.fixture
def autoapply_base_data(job, city_ashville):
    query_params = 'title=Comp&city_id={}'.format(city_ashville.id)
    return {
        'title': 'My autoapply',
        'query_params': query_params,
        'stopped_jobs': [],
        'deleted_jobs': [],
        'number': 3
    }


@pytest.fixture
def job_seeker_autoapply(job_seeker_client, autoapply_base_data):
    resp = api_requests.save_autoapply(
        job_seeker_client, autoapply_base_data)
    assert resp.status_code == http.HTTPStatus.CREATED
    return resp.json()


@pytest.fixture
def job_seeker_autoapply_for_one_job(job_seeker_client, autoapply_base_data):
    data = autoapply_base_data.copy()
    data['number'] = 1
    resp = api_requests.save_autoapply(
        job_seeker_client, data)
    assert resp.status_code == http.HTTPStatus.CREATED
    return resp.json()


@pytest.fixture
def started_autoapply(
        job_seeker_client, job_seeker_autoapply, job):
    resp = api_requests.start_autoapply(
        job_seeker_client, job_seeker_autoapply['id'],
        data={
            'applied_jobs': [
                job['id']
            ]
        })
    assert resp.status_code == http.HTTPStatus.OK
    return resp.json()


@pytest.fixture
def apply(job_seeker_client, job1, cover_letter):
    data = {'job': job1['id']}
    resp = api_requests.apply_to_job(job_seeker_client, data=data)
    assert resp.status_code == http.HTTPStatus.CREATED
    assert resp.json()['status'] == enums.ApplyStatusEnum.APPLIED.name
    return resp.json()


@pytest.fixture
def apply_for_company_2_job(job_seeker_client, company_2_job):
    resp = api_requests.apply_to_job(
        job_seeker_client,
        data={'job': company_2_job['id']})
    assert resp.status_code == http.HTTPStatus.CREATED
    assert resp.json()['status'] == enums.ApplyStatusEnum.APPLIED.name
    return resp.json()


@pytest.fixture
def apply_with_questionnaire(
        job_seeker_client, job_with_questions, answers_base_data):
    resp = api_requests.create_answers_to_questions(
        job_seeker_client,
        job_with_questions['id'],
        answers_base_data)
    assert resp.status_code == http.HTTPStatus.CREATED
    resp = api_requests.apply_to_job(
        job_seeker_client,
        data={'job': job_with_questions['id']})
    assert resp.status_code == http.HTTPStatus.CREATED
    assert resp.json()['status'] == enums.ApplyStatusEnum.APPLIED.name


@pytest.fixture
def autoapply_need_review(job_seeker_client, job_seeker_autoapply, job4):
    resp = api_requests.start_autoapply(
        job_seeker_client, job_seeker_autoapply['id'],
        data={
            'applied_jobs': [
                job4['id']
            ]
        })
    assert resp.status_code == http.HTTPStatus.OK
    return resp.json()
