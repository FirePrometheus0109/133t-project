import http

import pytest

from tests import api_requests


class TestCompanyEnumList:

    @pytest.mark.parametrize(('query_params', 'n_companies'), (
        (
            {},
            2
        ),
        (
            {'search': 'first'},
            1
        ),
        (
            {'search': 'fi'},
            1
        ),
        (
            {'search': 'sec'},
            1
        ),
        (
            {'search': 'com'},
            2
        ),
        (
            {'search': 'noresult'},
            0
        ),
    ))
    def test_list_company_enums(
            self, job_seeker_client, companies_list,
            query_params, n_companies):
        resp = api_requests.get_enums_companies(
            job_seeker_client,
            query_params=query_params)
        assert resp.status_code == http.HTTPStatus.OK
        assert len(resp.json()) == n_companies
