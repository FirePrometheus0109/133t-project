import copy
import http

import pytest

from job.models import Job
from tests import api_requests


@pytest.fixture
def job_seeker_autoapply2(job_seeker_client, autoapply_base_data):
    data = autoapply_base_data.copy()
    data['title'] = 'My autoapply2'
    data['stopped_jobs'] = []
    data['deleted_jobs'] = []
    data['query_params'] = ''
    resp = api_requests.save_autoapply(
        job_seeker_client, data)
    assert resp.status_code == http.HTTPStatus.CREATED
    return resp.json()


@pytest.fixture
def job_seeker_2_autoapply(job_seeker_2_client, autoapply_base_data):
    resp = api_requests.save_autoapply(
        job_seeker_2_client, autoapply_base_data)
    assert resp.status_code == http.HTTPStatus.CREATED
    return resp.json()


@pytest.fixture
def job_seeker_autoapplies(
        job_seeker_client, job, job1, job2, job3, autoapply_base_data):
    n_jobs = (3, 4, 25, 30)
    jobs = (job, job1, job2, job3)
    for n, job in zip(n_jobs, jobs):
        data = copy.deepcopy(autoapply_base_data)
        data['title'] = '{}{}'.format(n, autoapply_base_data['title'])
        data['number'] = n
        resp = api_requests.save_autoapply(job_seeker_client, data)
        assert resp.status_code == http.HTTPStatus.CREATED
        Job.objects.get(id=job['id']).applies.all().delete()  # workaround
        resp = api_requests.start_autoapply(
            job_seeker_client,
            resp.json()['id'],
            data={
                'applied_jobs': [job['id']]
            }
        )
        assert resp.status_code == http.HTTPStatus.OK
