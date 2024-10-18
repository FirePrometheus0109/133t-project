import datetime
import http
from unittest import mock

import pytest

from candidate import filters
from leet import enums
from tests import api_requests
from tests.api.candidate import constants
from tests.api.candidate import expected


class TestCandidateStats:

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
            'company_user_client',
            http.HTTPStatus.OK
        ),
    ))
    def test_candidate_workflow_steps_stats_permissions(
            self, request, client, status):
        client = request.getfixturevalue(client)
        resp = api_requests.get_candidates_workflow_stats(client)
        assert resp.status_code == status

    def test_get_candidate_stats_one_step(
            self, company_user_client, candidate):
        resp = api_requests.get_candidates_workflow_stats(company_user_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert (resp.json() ==
                expected.EXPECTED_CANDIDATE_WORKFLOW_STEPS_ONLY_APPLIED)

    def test_get_candidate_stats_completed_workflow(
            self, company_user_client, candidate_completed):
        resp = api_requests.get_candidates_workflow_stats(company_user_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert (resp.json() ==
                expected.EXPECTED_CANDIDATE_COMPLETED_WORKFLOW)

    def test_get_candidate_stats_completed_workflow_rejected_in_the_end(
            self, company_user_client, candidate_completed_rejected):
        resp = api_requests.get_candidates_workflow_stats(company_user_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert (resp.json() ==
                expected.EXPECTED_CANDIDATE_COMPLETED_WORKFLOW_REJECTED)

    def test_get_candidate_stats_step_back(
            self, company_user_client, candidate_completed,
            cand_status_screened):
        resp = api_requests.update_candidate_status(
            company_user_client,
            candidate_completed['id'],
            {'status': cand_status_screened['id']})
        assert resp.status_code == http.HTTPStatus.OK

        resp = api_requests.get_candidates_workflow_stats(company_user_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert (resp.json() ==
                expected.EXPECTED_CANDIDATE_COMPLETED_WORKFLOW_RETURNED_SCREENED)

    def test_get_candidate_stats_applied_rejected(
            self, company_user_client, candidate, cand_status_rejected):
        resp = api_requests.update_candidate_status(
            company_user_client,
            candidate['id'],
            {'status': cand_status_rejected['id']})

        resp = api_requests.get_candidates_workflow_stats(company_user_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert (resp.json() == expected.EXPECTED_CANDIDATE_APPLIED_REJECTED)

    def test_get_candidate_stats_screened_rejected_screened(
            self, company_user_client, candidate,
            cand_status_rejected, cand_status_screened):
        resp = api_requests.update_candidate_status(
            company_user_client,
            candidate['id'],
            {'status': cand_status_screened['id']})
        assert resp.status_code == http.HTTPStatus.OK
        resp = api_requests.update_candidate_status(
            company_user_client,
            candidate['id'],
            {'status': cand_status_rejected['id']})
        assert resp.status_code == http.HTTPStatus.OK
        resp = api_requests.restore_candidate(
            company_user_client,
            candidate['id'])
        assert resp.status_code == http.HTTPStatus.OK

        resp = api_requests.get_candidates_workflow_stats(company_user_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert (resp.json() ==
                expected.EXPECTED_CANDIDATE_SCREENED_REJECTED_SCREENED)

    def test_get_candidate_stats_applied_after_assign(
            self, company_user_client, job_seeker_client,
            job_seeker, assigned_candidate, job1):
        resp = api_requests.apply_to_job(
            job_seeker_client,
            {'job': job1['id']})
        assert resp.status_code == http.HTTPStatus.CREATED

        resp = api_requests.get_candidates_workflow_stats(company_user_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert (resp.json() ==
                expected.EXPECTED_CANDIDATE_WORKFLOW_STEPS_ONLY_APPLIED)

    def test_get_candidate_stats_reapplied_after_reject(
            self, company_user_client, job_seeker_client,
            candidate_completed_rejected):
        resp = api_requests.reapply_for_job(
            job_seeker_client,
            candidate_completed_rejected['job']['id'])
        assert resp.status_code == http.HTTPStatus.OK
        resp = api_requests.get_candidates_workflow_stats(company_user_client)
        assert resp.status_code == http.HTTPStatus.OK
        exp = expected.EXPECTED_CANDIDATE_COMPLETED_REJECTED_WORKFLOW_REAPPLY
        assert resp.json() == exp

    @pytest.mark.parametrize(('query_params', 'expec'), (
        (
            None,
            expected.CANDIDATE_WORKFLOW_STATS_ALL,
        ),
        (
            {'created_at':
                enums.WorkflowStepsCompanyStatFilters.TWO_WEEKS.name},
            expected.CANDIDATE_WORKFLOW_STATS_PAST_TWO_WEEKS,
        ),
        (
            {'created_at':
                enums.WorkflowStepsCompanyStatFilters.THIRTY_DAYS.name},
            expected.CANDIDATE_WORKFLOW_STATS_PAST_THIRTY_DAYS,
        ),
        (
            {'created_at':
                enums.WorkflowStepsCompanyStatFilters.SIXTY_DAYS.name},
            expected.CANDIDATE_WORKFLOW_STATS_PAST_SIXTY_DAYS,
        ),
    ))
    def test_get_candidates_workflow_stats_filter(
            self, company_user_client, query_params, expec,
            candidate_workflow_steps):
        num_days = (filters.ENUM_NUM_DAYS_MAP
                    [enums.WorkflowStepsCompanyStatFilters.TWO_WEEKS.name])
        mock_date = constants.FROM_DATE + datetime.timedelta(days=num_days)
        with mock.patch('django.utils.timezone.now', new=lambda: mock_date):
            resp = api_requests.get_candidates_workflow_stats(
                company_user_client, query_params)
            assert resp.status_code == http.HTTPStatus.OK
            assert resp.json() == expec

    def test_get_candidates_workflow_stats_filter_invalid_filter_value(
            self, company_user_client, candidate_workflow_steps):
        query_params = {'created_at': 'GIMMEEVERYTHINGUGOT'}
        resp = api_requests.get_candidates_workflow_stats(company_user_client,
                                                          query_params)
        assert resp.status_code == http.HTTPStatus.BAD_REQUEST

    def test_get_candidate_stats_hidded_all_statuses(
            self, company_user_client):
        data = {'statuses': []}
        resp = api_requests.manage_viewed_candidate_statuses(
            company_user_client, data)
        assert resp.status_code == http.HTTPStatus.OK

        resp = api_requests.get_candidates_workflow_stats(company_user_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert not resp.json()

    def test_get_candidate_states_all_statuses_hidden_exclude_rejected(
            self, company_user_client,
            candidate_completed_rejected, cand_status_rejected):
        data = {'statuses': [cand_status_rejected['id']]}
        resp = api_requests.manage_viewed_candidate_statuses(
            company_user_client, data)
        assert resp.status_code == http.HTTPStatus.OK

        n_candidates = 1
        resp = api_requests.get_candidates_workflow_stats(company_user_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert len(resp.json()) == 1
        assert resp.json()[0]['name'] == cand_status_rejected['name']
        assert resp.json()[0]['n_candidates'] == n_candidates

    def test_get_candidate_states_all_statuses_hidden_with_query_param_all(
            self, company_user_client, candidate_statuses,
            candidate_completed_rejected):
        data = {'statuses': []}
        resp = api_requests.manage_viewed_candidate_statuses(
            company_user_client, data)
        assert resp.status_code == http.HTTPStatus.OK

        n_candidates = len(candidate_statuses)
        query_params = {'all': 'true'}
        resp = api_requests.get_candidates_workflow_stats(
            company_user_client,
            query_params=query_params)
        assert resp.status_code == http.HTTPStatus.OK
        assert len(resp.json()) == n_candidates
