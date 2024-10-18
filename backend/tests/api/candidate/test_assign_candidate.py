import http

import pytest

from candidate import constants
from candidate import models
from job import models as job_models
from leet import enums
from tests import api_requests
from tests import validators
from tests.api.candidate import expected


class TestAssignCandidateToJobPermissions:

    @pytest.mark.parametrize(('client', 'status'), (
        (
            'anonym_client',
            http.HTTPStatus.UNAUTHORIZED
        ),
        (
            'job_seeker_client',
            http.HTTPStatus.FORBIDDEN
        ),
        (
            'company_2_user_client',
            http.HTTPStatus.FORBIDDEN
        ),
        (
            'company_user_client',
            http.HTTPStatus.CREATED
        ),
    ))
    def test_assign_candidate(
            self, request, client, status, job, job_seeker, apply):
        client = request.getfixturevalue(client)
        data = {
            'jobs': [job['id']],
            'job_seekers': [job_seeker.id]
        }
        resp = api_requests.assign_candidate_to_job(client, data)
        assert resp.status_code == status


class TestAssignCandidateToJob:

    def test_assign_candidate_to_jobs_success(
            self, company_user_client, company_jobs, company_user,
            job_seeker, purchased_job_seekers):
        data = {
            'jobs': [j['id'] for j in company_jobs],
            'job_seekers': [job_seeker.id]
        }
        resp = api_requests.assign_candidate_to_job(company_user_client, data)
        assert resp.status_code == http.HTTPStatus.CREATED
        exp = expected.EXPECTED_ONE_CANDIDATE_ASSIGNED_TO_JOBS
        assert resp.json() == exp
        workflow_steps = models.WorkflowStep.objects.all()
        for workflow_step in workflow_steps:
            assert workflow_step.owner == company_user

    def test_assign_candidate_to_job_already_assigned(
            self, company_user_client, assigned_candidates,
            job1, job2, job3, job_seeker):
        data = {
            'jobs': [j['id'] for j in (job1, job2, job3)],
            'job_seekers': [job_seeker.id]
        }
        resp = api_requests.assign_candidate_to_job(company_user_client, data)
        assert resp.status_code == http.HTTPStatus.CREATED
        exp = expected.EXPECTED_ONE_CANDIDATE_ALREADY_ASSIGNED_TO_JOBS
        assert resp.json() == exp

    def test_assign_two_candidates_one_is_already_assigned_on_some(
            self, company_user_client, assigned_candidates,
            job, company_jobs, job_seeker, job_seeker_2):
        jobs = company_jobs + (job,)
        data = {
            'jobs': [j['id'] for j in jobs],
            'job_seekers': [job_seeker.id, job_seeker_2.id]
        }
        resp = api_requests.assign_candidate_to_job(company_user_client, data)
        assert resp.status_code == http.HTTPStatus.CREATED
        exp = expected.EXPECTED_TWO_CANDIDATES_ON_MANY_JOBS
        assert resp.json() == exp

    def test_applied_job_seeker_is_already_candidate(
            self, company_user_client, job1, job_seeker, apply):
        data = {
            'jobs': [job1['id']],
            'job_seekers': [job_seeker.id]
        }
        resp = api_requests.assign_candidate_to_job(company_user_client, data)
        assert resp.status_code == http.HTTPStatus.CREATED
        assert resp.json() == expected.EXPECTED_APPLIED_CANDIDATE_TO_JOB

    def test_assign_rejected_candidate(
            self, company_user_client, rejected_candidate, job1, job_seeker):
        data = {
            'jobs': [job1['id']],
            'job_seekers': [job_seeker.id]
        }
        resp = api_requests.assign_candidate_to_job(company_user_client, data)
        assert resp.status_code == http.HTTPStatus.CREATED
        assert resp.json() == expected.EXPECTED_REJECTED_CANDIDATE_TO_JOB

    def test_assign_rejected_reapplied_candidate(
            self, company_user_client, job_seeker_client,
            rejected_candidate, job1, job_seeker):
        resp = api_requests.reapply_for_job(
            job_seeker_client,
            rejected_candidate['job']['id'])
        assert resp.status_code == http.HTTPStatus.OK
        data = {
            'jobs': [job1['id']],
            'job_seekers': [job_seeker.id]
        }
        resp = api_requests.assign_candidate_to_job(company_user_client, data)
        assert resp.status_code == http.HTTPStatus.CREATED
        assert resp.json() == expected.EXPECTED_APPLIED_CANDIDATE_TO_JOB


class TestAssignCandidateToJobValidate:

    def test_assign_candidates_max_count_jobs(
            self, company_user_client, job, many_jobs, job_seeker):
        jobs = many_jobs + [job]
        data = {
            'jobs': [j['id'] for j in jobs],
            'job_seekers': [job_seeker.id]
        }
        resp = api_requests.assign_candidate_to_job(company_user_client, data)
        emsg = constants.MAX_COUNT_OF_JOBS_ERROR
        validators.validate_error_message(resp, emsg, 'jobs')

    def test_assign_candidates_max_count_job_seekers(
            self, company_user_client, job, many_job_seekers, job_seeker):
        job_seekers = many_job_seekers + [job_seeker]
        data = {
            'jobs': [job['id']],
            'job_seekers': [js.id for js in job_seekers]
        }
        resp = api_requests.assign_candidate_to_job(company_user_client, data)
        emsg = constants.MAX_COUNT_OF_JOB_SEEKERS_ERROR
        validators.validate_error_message(resp, emsg, 'job_seekers')

    def test_assign_candidates_not_valid_job_status(
            self, company_user_client, job_draft,
            job_seeker, purchased_job_seekers):
        data = {
            'jobs': [job_draft['id']],
            'job_seekers': [job_seeker.id]
        }
        resp = api_requests.assign_candidate_to_job(company_user_client, data)
        emsg = constants.NOT_VALID_JOB_STATUS_FOR_ASSIGNING.format(
            job_draft['title'],
            job_draft['status'])
        validators.validate_error_message(resp, emsg, 'jobs')

    def test_assign_candidate_not_valid_job_seeker(
            self, company_user_client, job, job_seeker):
        data = {
            'jobs': [job['id']],
            'job_seekers': [job_seeker.id]
        }
        resp = api_requests.assign_candidate_to_job(company_user_client, data)
        emsg = constants.NOT_VALID_JOB_SEEKER_FOR_ASSIGNING.format(
            job_seeker.user.first_name,
            job_seeker.user.last_name)
        validators.validate_error_message(resp, emsg, 'job_seekers')

    def test_assign_candidate_not_valid_job_seeker_apply_need_review(
            self, company_user_client, job4,
            job_seeker, autoapply_need_review):
        data = {
            'jobs': [job4['id']],
            'job_seekers': [job_seeker.id]
        }
        job_models.Job.objects.exclude(id=job4['id']).delete()  # workaround
        resp = api_requests.assign_candidate_to_job(company_user_client, data)
        emsg = constants.NOT_VALID_JOB_SEEKER_FOR_ASSIGNING.format(
            job_seeker.user.first_name,
            job_seeker.user.last_name)
        validators.validate_error_message(resp, emsg, 'job_seekers')
