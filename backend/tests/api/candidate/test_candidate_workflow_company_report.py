import datetime
import http

import pytest
from tests import api_requests
from tests.api.candidate import constants
from tests.api.candidate import expected

from candidate import constants as candidate_constants


class TestCompanyReport:

    @pytest.mark.parametrize(('query_params', 'matched_data'), (
        (
            {
                'from_date': constants.FROM_DATE,
                'to_date': constants.FROM_DATE + datetime.timedelta(
                    weeks=10),
                'basis': candidate_constants.TIME_BASIS_DAY,
            },
            expected.COMPANY_REPORT_ALL_DATE,
        ),
        (
            {
                'from_date': constants.FROM_DATE,
                'to_date': constants.FROM_DATE + datetime.timedelta(days=5),
                'basis': candidate_constants.TIME_BASIS_DAY,
            },
            expected.COMPANY_REPORT_5_DAYS,
        ),
        (
            {
                'from_date': constants.FROM_DATE,
                'to_date': constants.FROM_DATE + datetime.timedelta(weeks=4),
                'basis': candidate_constants.TIME_BASIS_WEEK,
            },
            expected.COMPANY_REPORT_4_WEEK,
        ),
        (
            {
                'from_date': constants.FROM_DATE,
                'to_date': constants.FROM_DATE + datetime.timedelta(weeks=8),
                'basis': candidate_constants.TIME_BASIS_MONTH,
            },
            expected.COMPANY_REPORT_8_WEEKS_MONTH_BASIS,
        ),
        (
            {
                'from_date': constants.FROM_DATE - datetime.timedelta(days=15),
                'to_date': constants.FROM_DATE - datetime.timedelta(days=10),
                'basis': candidate_constants.TIME_BASIS_DAY,
            },
            expected.COMPANY_REPORT_EMPTY,
        ),
    ))
    def test_company_report_match_example(
            self, company_user_client, company, query_params, matched_data,
            company_candidates_workflow_stats):
        resp = api_requests.company_report(
            company_user_client,
            company.id,
            query_params['from_date'],
            query_params['to_date'],
            query_params['basis'])
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json() == matched_data

    @pytest.mark.parametrize(('client', 'status'), (
        (
            'company_user_client',
            http.HTTPStatus.OK
        ),
        (
            'company_user_client_without_subscription',
            http.HTTPStatus.FORBIDDEN
        ),
        (
            'company_2_user_client',
            http.HTTPStatus.FORBIDDEN
        ),
        (
            'company_2_user_client_without_subscription',
            http.HTTPStatus.FORBIDDEN
        ),
        (
            'company_user_2_client',
            http.HTTPStatus.OK
        ),
        (
            'job_seeker_client',
            http.HTTPStatus.FORBIDDEN
        ),
        (
            'anonym_client',
            http.HTTPStatus.UNAUTHORIZED
        ),
    ))
    def test_company_report_permissions(self, request, client, status,
                                        company):
        client = request.getfixturevalue(client)
        resp = api_requests.company_report(
            client,
            company.id,
            constants.FROM_DATE,
            constants.TO_DATE,
            candidate_constants.TIME_BASIS_DAY)
        assert resp.status_code == status

    @pytest.mark.parametrize(('basis_value', 'status'), (
        (
            candidate_constants.TIME_BASIS_DAY,
            http.HTTPStatus.OK
        ),
        (
            candidate_constants.TIME_BASIS_MONTH,
            http.HTTPStatus.OK
        ),
        (
            candidate_constants.TIME_BASIS_WEEK,
            http.HTTPStatus.OK
        ),
        (
            'year',
            http.HTTPStatus.BAD_REQUEST
        ),
        (
            'more_strange_value',
            http.HTTPStatus.BAD_REQUEST
        ),
        (
            '12849214qwoeioqwem7418294',
            http.HTTPStatus.BAD_REQUEST
        ),
    ))
    def test_company_report_basis(self, company_user_client, company,
                                  basis_value, status):
        resp = api_requests.company_report(
            company_user_client,
            company.id,
            constants.FROM_DATE,
            constants.TO_DATE,
            basis_value)
        assert resp.status_code == status
