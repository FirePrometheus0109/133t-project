import http

import pytest

from tests import api_requests
from tests import constants
from tests import utils
from tests.api.job import expected


class TestExportJobListCsv:

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
            http.HTTPStatus.OK),
        )
    )
    def test_get_csv(self, request, client, status, job1):
        client = request.getfixturevalue(client)
        query_params = {'jobs': job1['id']}
        resp = api_requests.export_job_list_csv(client, query_params)
        assert resp.status_code == status

    def test_get_csv_data(self, company_user_client, job1):
        data = {'jobs': [job1['id']]}
        resp = api_requests.export_job_list_csv(company_user_client, data)
        assert resp.status_code == http.HTTPStatus.OK
        assert (resp._headers.get('content-type')[1]
                == constants.CSV_EXPECTED_CONTENT_TYPE)

        headers, body = utils.get_csv_response_data(resp)
        job_row = body.pop(0)

        assert set(headers) == expected.CSV_EXPECTED_HEADERS

        assert job1['title'] in job_row
        assert job1['industry']['name'] in job_row
        assert job1['position_type'] in job_row
        assert job1['description'] in job_row
        assert job1['status'] in job_row
        assert job1['education'] in job_row
        print(job_row)
        assert str(job1['clearance']) in job_row
        assert job1['experience'] in job_row
        assert str(job1['salary_min']) in job_row
        assert str(job1['salary_max']) in job_row
        assert str(job1['salary_negotiable']) in job_row
        assert job1['benefits'] in job_row
        assert job1['travel'] in job_row
        assert job1['publish_date'] in job_row
        assert job1['owner']['name'] in job_row
        assert job1['location']['country']['name'] in job_row
        assert job1['location']['city']['state']['name'] in job_row
        assert job1['location']['city']['name'] in job_row
        assert job1['location']['zip'].get('code', '') in job_row

        job1_rs = ','.join(s['name'] for s in job1['required_skills'])
        job1_os = ','.join(s['name'] for s in job1['optional_skills'])

        assert job1_rs in job_row
        assert job1_os in job_row

    def test_get_multiple_jobs_csv(self, company_user_client, company_jobs):
        job_ids = [j['id'] for j in company_jobs]
        data = {'jobs': job_ids}
        resp = api_requests.export_job_list_csv(company_user_client, data)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp._headers.get('content-type')[
                   1] == constants.CSV_EXPECTED_CONTENT_TYPE
