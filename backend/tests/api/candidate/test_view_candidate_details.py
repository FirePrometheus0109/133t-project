import copy
import http

import pytest

from tests import api_requests
from tests import utils
from tests import validators
from tests.api.candidate import expected

from candidate import constants


class TestViewCandidate:

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
            http.HTTPStatus.NOT_FOUND
        ),
        (
            'company_user_client',
            http.HTTPStatus.OK
        ),
    ))
    def test_view_candidate_details_permissions(
            self, request, client, status, candidate):
        client = request.getfixturevalue(client)
        resp = api_requests.get_candidate(client, candidate['id'])
        assert resp.status_code == status

    def test_get_candidate_details(self, company_user_client, candidate):
        resp = api_requests.get_candidate(company_user_client, candidate['id'])
        assert resp.status_code == http.HTTPStatus.OK
        data = resp.json()
        # NOTE (i.bogretsov) check fields actual only for candidate
        for k, v in expected.EXPECTED_CANDIDATE_DATA.items():
            assert data[k] == v

    def test_get_candidate_details_with_cover_letter(
            self, job_seeker_client, job1, cover_letter,
            job_base_data, company_user_client):
        data = copy.deepcopy(job_base_data)
        data['title'] = job1['title']
        data['requred_skills'] = [i['id'] for i in job1['required_skills']]
        data['optional_skills'] = [i['id'] for i in job1['optional_skills']]
        data['is_cover_letter_required'] = True
        resp = api_requests.update_job(company_user_client, job1['id'], data)
        assert resp.status_code == http.HTTPStatus.OK

        data = {
            'job': job1['id'],
            'cover_letter': cover_letter['id']
        }
        resp = api_requests.apply_to_job(job_seeker_client, data)
        assert resp.status_code == http.HTTPStatus.CREATED

        resp = api_requests.get_candidates(company_user_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == 1
        candidate = resp.json()['results'][0]
        assert candidate['cover_letter'] == cover_letter

        resp = api_requests.get_candidate(company_user_client, candidate['id'])
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['cover_letter'] == cover_letter

    def test_get_banned_candidate_details_forbidden(
            self, company_user, company_user_client, company_user_candidate_1):
        utils.ban_entity(company_user_candidate_1.job_seeker)
        resp = api_requests.get_candidate(
            company_user_client,
            company_user_candidate_1.id)
        emsg = constants.CANDIDATE_BANNED_ERROR.format(
            company_user_candidate_1.job_seeker.user.get_full_name())
        validators.validate_error_message(
            resp,
            emsg,
            error_code=http.HTTPStatus.FORBIDDEN)
