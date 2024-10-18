import copy
import http

import pytest
import pytz
from dateutil import parser

from leet import enums
from tests import api_requests
from tests.api.log import expected


class TestLogs:

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
        )
    ))
    def test_get_logs_permissions(self, request, client, status):
        client = request.getfixturevalue(client)
        resp = api_requests.get_company_logs(client)
        assert resp.status_code == status

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
            http.HTTPStatus.NO_CONTENT
        )
    ))
    def test_delete_permissions(self, request, client, status, log):
        client = request.getfixturevalue(client)
        resp = api_requests.delete_log(client, log['id'])
        assert resp.status_code == status

    @pytest.mark.parametrize(('fixture', 'exp_logs', 'is_job'), (
        (
            'purchased_job_seeker',
            expected.EXPECTED_LOGS_AFTER_PURCHASE_PROFILE,
            False
        ),
        (
            'assigned_candidate',
            expected.EXPECTED_LOGS_AFTER_ASSIGN_CANDIDATE,
            False
        ),
        (
            'apply',
            expected.EXPECTED_LOGS_AFTER_APPLY,
            False
        ),
        (
            'started_autoapply',
            expected.EXPECTED_LOGS_AFTER_AUTOAPPLY,
            False
        ),
        (
            'reapplied_candidate',
            expected.EXPECTED_LOGS_AFTER_REAPPLY,
            False
        ),
        (
            'rejected_candidate',
            expected.EXPECTED_LOGS_AFTER_CHANGED_WORKFLOW,
            False
        ),
        (
            'candidate_good_rate',
            expected.EXPECTED_LOGS_AFTER_CHANGING_RATE,
            False
        ),
        (
            'candidate_no_rate',
            expected.EXPECTED_LOGS_AFTER_REMOVING_RATE,
            False
        ),
        (
            'job',
            expected.EXPECTED_LOGS_AFTER_CREATING_JOB,
            True
        ),
        (
            'deleted_job',
            expected.EXPECTED_LOGS_AFTER_DELETING_JOB,
            True
        ),
        (
            'saved_job_seeker',
            expected.EXPECTED_LOGS_AFTER_SAVING_OF_JOB_SEEKER,
            False
        ),
    ))
    def test_get_logs_after_some_action(
            self, request, company_user_client,
            js_logs_query_params, job_logs_query_params,
            fixture, exp_logs, is_job):
        request.getfixturevalue(fixture)
        params = job_logs_query_params if is_job else js_logs_query_params
        resp = api_requests.get_company_logs(
            company_user_client,
            query_params=params)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['results'] == exp_logs

    def test_get_logs_after_event_creation(
            self, company_user_client, js_logs_query_params, event, tz_new_york):
        params = js_logs_query_params
        resp = api_requests.get_company_logs(
            company_user_client,
            query_params=params)
        assert resp.status_code == http.HTTPStatus.OK
        result = resp.json()['results'][0]
        tz = pytz.timezone(tz_new_york)
        assert result == expected.EXPECTED_LOGS_AFTER_EVENT_CREATION
        event_time_from = parser.parse(event['time_from']).astimezone(tz)
        expected_message = ('scheduled Interview with Candidate for '
                            '{} in title.'.format(event_time_from))
        assert result['message'] == expected_message

    def test_get_logs_after_created_job_seeker_comment(
            self, company_user_client, job_seeker, js_logs_query_params):
        data = {
            'title': 'what',
            'comment': 'ever',
            'source': job_seeker.id
        }
        resp = api_requests.create_job_seeker_comment(
            company_user_client,
            data)
        assert resp.status_code == http.HTTPStatus.CREATED
        resp = api_requests.get_company_logs(
            company_user_client,
            query_params=js_logs_query_params)
        exp = expected.EXPECTED_LOGS_AFTER_ADDING_COMMENT_JS
        assert resp.json()['results'] == exp

    def test_get_logs_after_edit_job_seeker_comment(
            self, company_user_client, job_seeker, js_logs_query_params):
        data = {
            'title': 'what',
            'comment': 'ever',
            'source': job_seeker.id
        }
        resp = api_requests.create_job_seeker_comment(
            company_user_client,
            data)
        assert resp.status_code == http.HTTPStatus.CREATED
        data = {
            'title': 'what',
            'comment': 'everbeen',
            'source': job_seeker.id
        }
        resp = api_requests.update_job_seeker_comment(
            company_user_client,
            resp.json()['id'],
            data)
        assert resp.status_code == http.HTTPStatus.OK
        resp = api_requests.get_company_logs(
            company_user_client,
            query_params=js_logs_query_params)
        exp = expected.EXPECTED_LOGS_AFTER_EDIT_COMMENT_JS
        assert resp.json()['results'] == exp

    def test_get_logs_after_delete_job_seeker_comment(
            self, company_user_client, job_seeker, js_logs_query_params):
        data = {
            'title': 'what',
            'comment': 'ever',
            'source': job_seeker.id
        }
        resp = api_requests.create_job_seeker_comment(
            company_user_client,
            data)
        assert resp.status_code == http.HTTPStatus.CREATED
        resp = api_requests.delete_job_seeker_comment(
            company_user_client,
            resp.json()['id'])
        assert resp.status_code == http.HTTPStatus.NO_CONTENT
        resp = api_requests.delete_job_seeker_comment
        resp = api_requests.get_company_logs(
            company_user_client,
            query_params=js_logs_query_params)
        exp = expected.EXPECTED_LOGS_AFTER_DELETE_COMMENT_JS
        assert resp.json()['results'] == exp

    def test_delete_log(self, company_user_client, log, js_logs_query_params):
        resp = api_requests.delete_log(company_user_client, log['id'])
        assert resp.status_code == http.HTTPStatus.NO_CONTENT
        resp = api_requests.get_company_logs(
            company_user_client,
            query_params=js_logs_query_params)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == 0
        assert not resp.json()['results']

    def test_logs_invalid_object_id(
            self, company_user_client, log, js_logs_query_params):
        query_params = js_logs_query_params.copy()
        query_params['object_id'] = 999999
        resp = api_requests.get_company_logs(
            company_user_client,
            query_params=query_params)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == 0

    def test_get_job_logs_after_changing_only_status(
            self, company_user_client, job,
            job_base_data, job_logs_query_params):
        data = copy.deepcopy(job_base_data)
        data['status'] = enums.JobStatusEnum.DRAFT.name
        resp = api_requests.update_job(
            company_user_client,
            job['id'],
            data)
        assert resp.status_code == http.HTTPStatus.OK
        resp = api_requests.get_company_logs(
            company_user_client,
            job_logs_query_params)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == 2
        exp = expected.EXPECTED_LOGS_AFTER_CHANGING_JOB_STATUS
        assert resp.json()['results'] == exp

    @pytest.mark.parametrize(('field', 'value'), (
        (
            'required_skills',
            [],
        ),
        (
            'optional_skills',
            [],
        ),
        (
            'title',
            'new',
        ),
        (
            'location',
            {},
        ),
        (
            'industry',
            0,
        ),
    ))
    def test_get_job_logs_after_changing_attrs(
            self, company_user_client, job, field, value,
            industry_construction, city_new_york, country_usa,
            job_base_data, job_logs_query_params):
        data = copy.deepcopy(job_base_data)
        # default job's fixture city is ashville
        loca_value = {'city': city_new_york.id, 'country': country_usa.id}
        # default job's fixture industry is industry_manufacturing
        industry_value = industry_construction.id
        if field == 'location':
            data[field] = loca_value
        elif field == 'industry':
            data[field] = industry_value
        else:
            data[field] = value
        resp = api_requests.update_job(
            company_user_client,
            job['id'],
            data)
        assert resp.status_code == http.HTTPStatus.OK
        resp = api_requests.get_company_logs(
            company_user_client,
            job_logs_query_params)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == 2
        exp = expected.EXPECTED_LOGS_AFTER_EDITING_JOB
        assert resp.json()['results'] == exp

    def test_get_job_logs_nothing_is_changed(
            self, company_user_client, job,
            job_base_data, job_logs_query_params):
        resp = api_requests.update_job(
            company_user_client,
            job['id'],
            job_base_data)
        assert resp.status_code == http.HTTPStatus.OK
        resp = api_requests.get_company_logs(
            company_user_client,
            job_logs_query_params)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == 1
        exp = expected.EXPECTED_LOGS_AFTER_CREATING_JOB
        assert resp.json()['results'] == exp
