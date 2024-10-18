import datetime
import http
from unittest import mock

import pytest
from django.conf import settings
from django.utils import timezone

from leet import constants as base_constants
from tests import api_requests
from tests import utils
from tests import validators


def assign_candidate(client, data, date):
    mockname = 'django.utils.timezone.now'
    with mock.patch(mockname, new=lambda: date):
        resp = api_requests.assign_candidate_to_job(client, data)
        assert resp.status_code == http.HTTPStatus.CREATED


class TestCandidatesListApi:

    def test_assigned_job_seeker_in_candidates_list(
            self, company_user_client, assigned_candidates):
        resp = api_requests.get_candidates(company_user_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == 6

    def test_applied_job_seeker_in_candidates_list(
            self, company_user_client, apply):
        resp = api_requests.get_candidates(company_user_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == 1
        assert resp.json()['results'][0]['is_disqualified_for_skills']

    @pytest.mark.parametrize(('candidate_apply', 'expected_value'), (
            ('apply', False),
            ('apply_with_questionnaire', False),
            ('apply_with_disqualifying_questionnaire', True),
    ))
    def test_applied_job_seeker_is_disqualified_for_questionnaire_expected(
            self, request, company_user_client,
            candidate_apply, expected_value):
        request.getfixturevalue(candidate_apply)
        resp = api_requests.get_candidates(company_user_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == 1
        data = resp.json()['results'][0]
        assert data['is_disqualified_for_questionnaire'] is expected_value

    @pytest.mark.parametrize(('candidate_apply', 'expected_value'), (
            ('apply', True),
            ('apply_with_questionnaire', False),
    ))
    def test_applied_job_seeker_is_disqualified_for_skills_expected(
            self, request, company_user_client,
            candidate_apply, expected_value):
        # apply_with_questionnaire has fixture job
        # which has all candidate skills
        request.getfixturevalue(candidate_apply)
        resp = api_requests.get_candidates(company_user_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == 1
        data = resp.json()['results'][0]
        assert data['is_disqualified_for_skills'] is expected_value

    def test_candidate_applied_after_assignment(
            self, assigned_candidate, company_user_client,
            job_seeker_client, job1):
        resp = api_requests.get_candidates(company_user_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == 1
        data = resp.json()['results'][0]
        assert data['is_applied_after_assignment'] is False
        resp = api_requests.apply_to_job(
            job_seeker_client,
            data={'job': job1['id']}
        )
        assert resp.status_code == http.HTTPStatus.CREATED
        resp = api_requests.get_candidates(company_user_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == 1
        data = resp.json()['results'][0]
        assert data['is_applied_after_assignment']

    @pytest.mark.usefixtures('candidates')
    def test_search_candidate_by_skill(
            self, company_user_client, job1, job_seeker):
        resp = api_requests.get_candidates(
            company_user_client, {'search': 'Operating system'})
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == 1
        data = resp.json()['results'][0]
        assert data['job']['id'] == job1['id']
        assert data['job_seeker']['id'] == job_seeker.id

    @pytest.mark.usefixtures('candidates')
    @pytest.mark.parametrize(
        ('location_fixture', 'location_field', 'exp_js_fixture'),
        (
            ('city_new_york', 'name', 'job_seeker'),
            ('city_ashville', 'name', 'job_seeker_2'),
            ('state_new_york', 'abbreviation', 'job_seeker'),
            ('state_alabama', 'abbreviation', 'job_seeker_2')
        )
    )
    def test_search_candidates_by_location(
            self, company_user_client, job1, request,
            location_fixture, location_field, exp_js_fixture):
        location = request.getfixturevalue(location_fixture)
        job_seeker = request.getfixturevalue(exp_js_fixture)
        resp = api_requests.get_candidates(
            company_user_client,
            query_params={
                'location': getattr(location, location_field)
            })
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == 1
        data = resp.json()['results'][0]
        assert data['job']['id'] == job1['id']
        assert data['job_seeker']['id'] == job_seeker.id

    def test_get_list_candidates_previous_date_exists(
            self, company_user_client, reapplied_candidate,
            mock_tomorrow, mock_yesterday):
        resp = api_requests.get_candidates(company_user_client)
        assert resp.status_code == http.HTTPStatus.OK
        candidate = resp.json()['results'][0]
        exp = mock_tomorrow.strftime(settings.DEFAULT_SERVER_DATETIME_FORMAT)
        assert candidate['applied_date'] == exp
        exp = mock_yesterday.strftime(settings.DEFAULT_SERVER_DATETIME_FORMAT)
        assert candidate['previous_applied_date'] == exp

    def test_get_list_candidates_default_ordering(
            self, company_user_client, purchased_job_seekers, job):
        # default orediring by 'applied_date' from newest to oldest
        first_date = utils.date(2018, 12, 1)
        data = {
            'jobs': [job['id']],
            'job_seekers': [purchased_job_seekers[0].id]
        }
        assign_candidate(company_user_client, data, first_date)
        second_date = utils.date(2018, 12, 2)
        data['job_seekers'] = [purchased_job_seekers[1].id]
        assign_candidate(company_user_client, data, second_date)

        resp = api_requests.get_candidates(company_user_client)
        assert resp.status_code == http.HTTPStatus.OK
        validators.validate_ordering(
            resp.json()['results'],
            '-applied_date',
            'applied_date')


class TestCandidatesListAppliedDate:
    # if mock_tomorrow first argument in test than all fixtures created
    # with mock date tomorrow.

    def test_candidates_applied_date_after_assign(
            self, mock_tomorrow, candidate, company_user_client):
        resp = api_requests.get_candidates(company_user_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == 1
        candidate = resp.json()['results'][0]
        exp_date = mock_tomorrow.strftime(
            settings.DEFAULT_SERVER_DATETIME_FORMAT)
        assert candidate['applied_date'] == exp_date

    def test_assigned_candidate_applied_date_after_apply(
            self, assigned_candidate, job_seeker_client, job1,
            company_user_client):
        mock_next_week = timezone.now() + datetime.timedelta(days=7)
        mockname = 'django.utils.timezone.now'
        data = {'job': job1['id']}
        with mock.patch(mockname, new=lambda: mock_next_week):
            resp = api_requests.apply_to_job(job_seeker_client, data)
            assert resp.status_code == http.HTTPStatus.CREATED

            resp = api_requests.get_candidates(company_user_client)
            assert resp.status_code == http.HTTPStatus.OK
            assert resp.json()['count'] == 1
            candidate = resp.json()['results'][0]
            exp_date = mock_next_week.strftime(
                settings.DEFAULT_SERVER_DATETIME_FORMAT)
            assert candidate['applied_date'] == exp_date

    def test_assigned_candidate_applied_date_after_reapply(
            self, assigned_candidate, candidate,
            job_seeker_client, company_user_client, mock_tomorrow):
        resp = api_requests.reapply_for_job(
            job_seeker_client,
            candidate['job']['id'])
        assert resp.status_code == http.HTTPStatus.OK

        resp = api_requests.get_candidates(company_user_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == 1
        candidate = resp.json()['results'][0]
        exp_date = mock_tomorrow.strftime(
            settings.DEFAULT_SERVER_DATETIME_FORMAT)
        assert candidate['applied_date'] == exp_date

    def test_rejected_candidate_applied_date_not_updated(
            self, mock_tomorrow, rejected_candidate,
            job_seeker_client, company_user_client):
        n_candidates = 2
        mockname = 'django.utils.timezone.now'
        # rejected candidate reapplies
        mock_next_week = timezone.now() + datetime.timedelta(days=7)
        with mock.patch(mockname, new=lambda: mock_next_week):
            resp = api_requests.reapply_for_job(
                job_seeker_client,
                rejected_candidate['job']['id'])
            assert resp.status_code == http.HTTPStatus.OK

            # candidate is not rejected more, but there is an old candidate entry
            # and applied_date value of rejected entry is not equal
            # new candidate applied_date
            resp = api_requests.get_candidates(company_user_client)
            assert resp.status_code == http.HTTPStatus.OK
            assert resp.json()['count'] == n_candidates

        rejected_candidate = next(
            i for i in resp.json()['results']
            if i['status']['name'] == base_constants.CANDIDATE_STATUS_REJECTED)
        applied_candidate = next(
            i for i in resp.json()['results']
            if i['status']['name'] == base_constants.CANDIDATE_STATUS_APPLIED)

        assert (rejected_candidate['applied_date'] !=
                applied_candidate['applied_date'])
        exp_date = mock_tomorrow.strftime(
            settings.DEFAULT_SERVER_DATETIME_FORMAT)
        assert rejected_candidate['applied_date'] == exp_date
        exp_date = mock_next_week.strftime(
            settings.DEFAULT_SERVER_DATETIME_FORMAT)
        assert applied_candidate['applied_date'] == exp_date

    def test_applied_date_rejected_assigned_applied_candidate(
            self, mock_tomorrow, mock_has_subscription,
            assigned_candidate, job_seeker_client,
            company_user_client, job1, cand_status_rejected):
        # reject assigned candidate
        data = {'status': cand_status_rejected['id']}
        resp = api_requests.update_candidate_status(
            company_user_client,
            assigned_candidate['id'],
            data)
        assert resp.status_code == http.HTTPStatus.OK
        n_candidates = 2
        mockname = 'django.utils.timezone.now'
        # rejected candidate applies
        mock_next_week = timezone.now() + datetime.timedelta(days=7)
        with mock.patch(mockname, new=lambda: mock_next_week):
            # rejected candidate applies
            data = {'job': job1['id']}
            resp = api_requests.apply_to_job(job_seeker_client, data)
            assert resp.status_code == http.HTTPStatus.CREATED

            resp = api_requests.get_candidates(company_user_client)
            assert resp.status_code == http.HTTPStatus.OK
            assert resp.json()['count'] == n_candidates

        rejected_candidate = next(
            i for i in resp.json()['results']
            if i['status']['name'] == base_constants.CANDIDATE_STATUS_REJECTED)
        applied_candidate = next(
            i for i in resp.json()['results']
            if i['status']['name'] == base_constants.CANDIDATE_STATUS_APPLIED)

        assert (rejected_candidate['applied_date'] !=
                applied_candidate['applied_date'])
        exp_date = mock_tomorrow.strftime(
            settings.DEFAULT_SERVER_DATETIME_FORMAT)
        assert rejected_candidate['applied_date'] == exp_date
        exp_date = mock_next_week.strftime(
            settings.DEFAULT_SERVER_DATETIME_FORMAT)
        assert applied_candidate['applied_date'] == exp_date
