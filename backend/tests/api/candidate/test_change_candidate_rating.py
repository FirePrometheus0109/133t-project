import http

import pytest

from leet import enums
from tests import api_requests


class TestCandidateRating:

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
    def test_rating_candidate_permissions(
            self, request, client, status, candidate):
        client = request.getfixturevalue(client)
        data = {'rating': enums.RatingEnum.POOR.name}
        resp = api_requests.change_candidate_rating(
            client, candidate['id'], data)
        assert resp.status_code == status

    def test_update_candidate_rating(
            self, company_user_client, company_user_2_client,
            company_user, active_company_user, candidate):
        ratings = (
            enums.RatingEnum.POOR.name,
            enums.RatingEnum.GOOD.name,
            enums.RatingEnum.VERY_GOOD.name,
            enums.RatingEnum.EXCELLENT.name,
            enums.RatingEnum.NO_RATING.name,
        )
        resp = api_requests.change_candidate_rating(
            company_user_client,
            candidate['id'],
            {'rating': ratings[0]})
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['rating'] == ratings[0]
        assert resp.json()['owner'] == company_user.user.get_full_name()

        full_name = ' '.join([
            active_company_user['user']['first_name'],
            active_company_user['user']['last_name']
        ])
        for r in ratings:
            resp = api_requests.change_candidate_rating(
                company_user_2_client,
                candidate['id'],
                {'rating': r})
            assert resp.status_code == http.HTTPStatus.OK
            assert resp.json()['rating'] == r
            assert resp.json()['owner'] == full_name
