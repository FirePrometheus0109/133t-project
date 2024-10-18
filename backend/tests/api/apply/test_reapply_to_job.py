import datetime
import http
from unittest import mock

import pytest
from django.conf import settings
from django.utils import timezone

from apply import constants
from leet import enums
from tests import api_requests
from tests import validators


class TestReApplyToJob:

    @pytest.mark.parametrize(('client', 'status'), (
        (
            'anonym_client',
            http.HTTPStatus.UNAUTHORIZED,
        ),
        (
            'job_seeker_client',
            http.HTTPStatus.OK,
        ),
        (
            'company_user_client',
            http.HTTPStatus.FORBIDDEN,
        ),
    ))
    def test_reapply_permissions(
            self, request, client, status, apply, job1):
        client = request.getfixturevalue(client)
        resp = api_requests.reapply_for_job(client, job1['id'])
        assert resp.status_code == status

    def test_reapply_apply_does_not_exist(self, job_seeker_client, job1):
        resp = api_requests.reapply_for_job(job_seeker_client, job1['id'])
        assert resp.status_code == http.HTTPStatus.NOT_FOUND

    @pytest.mark.parametrize(('candidate_fixture',), (
        (
            'candidate',
        ),
        (
            'candidate_a_apply',
        )
    ))
    def test_reapply_success(
            self, request, job_seeker_client, candidate_fixture):
        candidate = request.getfixturevalue(candidate_fixture)
        mockname = 'django.utils.timezone.now'
        mock_value = timezone.now() + datetime.timedelta(days=1)
        with mock.patch(mockname, new=lambda: mock_value):
            resp = api_requests.reapply_for_job(
                job_seeker_client,
                candidate['job']['id'])
            assert resp.status_code == http.HTTPStatus.OK
            applied_at = resp.json()['applied_at']
            exp = mock_value.strftime(settings.DEFAULT_SERVER_DATETIME_FORMAT)
            assert applied_at == exp

    def test_not_active_job_for_reapply(
            self, job_seeker_client, company_user_client,
            apply, job1, job_base_data):
        job_base_data['status'] = enums.JobStatusEnum.DRAFT.name
        resp = api_requests.update_job(
            company_user_client,
            job1['id'],
            job_base_data)
        assert resp.status_code == http.HTTPStatus.OK
        resp = api_requests.reapply_for_job(job_seeker_client, job1['id'])
        validators.validate_error_message(
            resp,
            constants.IMPOSSIBLE_TO_APPLY_FOR_NOT_ACTIVE_JOB_ERROR)

    def test_does_not_reapply_for_the_job_need_no_matching(
            self, job_seeker_client, company_user_client,
            apply, job1, job_base_data):
        job_base_data['is_cover_letter_required'] = True
        resp = api_requests.update_job(
            company_user_client,
            job1['id'],
            job_base_data)
        assert resp.status_code == http.HTTPStatus.OK
        resp = api_requests.reapply_for_job(
            job_seeker_client,
            job1['id'])
        validators.validate_error_message(
            resp,
            constants.COVER_LETTER_IS_REQUIRED_FOR_APPLY)

    @pytest.mark.parametrize(
        ('candidate_fixture', 'n_candidates'), (
            (
                'candidate',
                1
            ),
            (
                'candidate_a_apply',
                1
            ),
            (
                'rejected_candidate',
                2
            ),
            (
                'candidate_a_apply_rejected',
                2
            ),
        )
    )
    def test_reapply_to_the_job_candidate_count_candidates(
            self, request, job_seeker_client, candidate_fixture,
            company_user_client, n_candidates):
        candidate = request.getfixturevalue(candidate_fixture)
        resp = api_requests.reapply_for_job(
            job_seeker_client,
            candidate['job']['id'])
        assert resp.status_code == http.HTTPStatus.OK
        # check count candidates
        resp = api_requests.get_candidates(company_user_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == n_candidates

    def test_can_not_reaaply_to_job_in_autoapply_list_if_skills_dont_match(
            self, candidate_a_apply, job_seeker_client, job_seeker):
        job_seeker.skills.clear()
        resp = api_requests.reapply_for_job(
            job_seeker_client,
            candidate_a_apply['job']['id'])
        validators.validate_error_message(
            resp,
            constants.REQUIRED_SKILLS_MATCH_ERROR)
