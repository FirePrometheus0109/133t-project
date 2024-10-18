import copy
import datetime
import http
from unittest import mock

import pytest
from django.utils import timezone

from event import constants
from tests import api_requests
from tests import validators


class TestEventValidate:

    def test_create_event_not_valid_job_status(
            self, company_user_client, job_closed, event_base_data):
        data = copy.deepcopy(event_base_data)
        data['job'] = job_closed['id']
        resp = api_requests.create_event(company_user_client, data)
        emsg = constants.INVALID_JOB_FOR_EVENT.format(job_closed['title'])
        validators.validate_error_message(resp, emsg, 'job')

    def test_create_event_candidate_is_not_valid_for_event_for_certain_job(
            self, company_user_client, event_base_data, candidate_one, job1):
        data = copy.deepcopy(event_base_data)
        data['candidates'] = [candidate_one['job_seeker']['user']['id']]
        data['job'] = job1['id']
        resp = api_requests.create_event(company_user_client, data)
        user = candidate_one['job_seeker']['user']
        user_name = ' '.join([user['first_name'], user['last_name']])
        emsg = constants.INVALID_CANDIDATE_FOR_EVENT_ERROR.format(user_name)
        validators.validate_error_message(resp, emsg)

    def test_create_event_max_count_candidates(
            self, company_user_client, event_data, settings):
        max_count = 0
        settings.MAX_COUNT_OF_CANDIDATES_FOR_EVENT = max_count
        resp = api_requests.create_event(company_user_client, event_data)
        emsg = constants.MAX_COUNT_OF_CANDIDATES_FOR_EVENT_ERROR.format(
            max_count)
        validators.validate_error_message(resp, emsg, 'candidates')

    def test_create_event_colleagues_is_not_valid(
            self, company_user_client, event_data, new_company_user):
        data = copy.deepcopy(event_data)
        # TODO (i.bogretsov) change key to user_id
        data['colleagues'] = [new_company_user['user']]
        resp = api_requests.create_event(company_user_client, data)
        emsgs = [
            constants.INVALID_COLLEAGUE_FOR_EVENT_ERROR.format(
                new_company_user['full_name']),
            constants.ATTENDEES_LIST_SHOULD_CONTAIN_EVENT_OWNER_ERROR
        ]
        validators.validate_error_message(resp, emsgs)

    def test_create_event_max_count_colleagues(
            self, company_user_client, event_base_data, settings):
        max_count = 0
        settings.MAX_COUNT_OF_COLLEAGUES_FOR_EVENT = max_count
        resp = api_requests.create_event(company_user_client, event_base_data)
        emsg = constants.MAX_COUNT_OF_COLLEAGUES_FOR_EVENT_ERROR.format(
            max_count)
        validators.validate_error_message(resp, emsg, 'colleagues')

    @pytest.mark.parametrize(('field', 'value'), (
        (
            'address',
            '',
        ),
        (
            'address',
            None,
        ),
        (
            'address',
            'pop',
        ),
        (
            'country',
            None
        ),
        (
            'city',
            None
        ),
        (
            'zip',
            None
        ),
        (
            'country',
            'pop'
        ),
        (
            'city',
            'pop'
        ),
        (
            'zip',
            'pop'
        )
    ))
    def test_create_event_location_field_all_required(
            self, company_user_client, event_base_data, field, value):
        data = copy.deepcopy(event_base_data)
        data['location'][field] = value
        if value == 'pop':
            data['location'].pop(field)
        resp = api_requests.create_event(company_user_client, data)
        assert resp.status_code == http.HTTPStatus.BAD_REQUEST
        assert 'location' in resp.json()['field_errors']

    @pytest.mark.parametrize(('field', 'value', 'error'), (
        (
            'time_from',
            str(datetime.datetime(2019, 1, 1, 1, 59)),
            constants.INVALID_EVENT_TIME_ERROR,
        ),
        (
            'time_to',
            str(datetime.datetime(2019, 1, 1, 1, 59)),
            constants.INVALID_EVENT_TIME_ERROR,
        )
    ))
    def test_create_event_invalid_datetime(
            self, company_user_client, event_base_data, field, value, error):
        data = copy.deepcopy(event_base_data)
        data[field] = value
        mockname = 'event.validators.validate_event_from_to_time'
        with mock.patch(mockname, return_value=None):
            resp = api_requests.create_event(company_user_client, data)
            validators.validate_error_message(resp, error, field)

    def test_create_event_time_from_great_than_time_to(
            self, company_user_client, event_data):
        data = copy.deepcopy(event_data)
        data['time_from'], data['time_to'] = data['time_to'], data['time_from']
        resp = api_requests.create_event(company_user_client, data)
        emsg = constants.INVALID_TIME_FROM_TIME_TO_ERROR
        validators.validate_error_message(resp, emsg)

    def test_event_timezone_does_not_equal_timezone_time_from_time_to(
            self, company_user_client, event_data, tz_london):
        data = copy.deepcopy(event_data)
        data['timezone'] = tz_london
        resp = api_requests.create_event(company_user_client, data)
        emsg = constants.TIMEZONE_OFFSET_DOES_NOT_EQUAL_TIME_TZ_OFFSET
        validators.validate_error_message(resp, emsg)

    @pytest.mark.parametrize(('param', 'value', 'emsg'), (
        (
            'day',
            '',
            constants.LIST_EVENTS_QUERY_PARAMS_DAY_OR_MONTH_ERROR
        ),
        (
            'month',
            '',
            constants.LIST_EVENTS_QUERY_PARAMS_DAY_OR_MONTH_ERROR
        ),
        (
            'tz',
            '',
            constants.TIMEZONE_IS_REQUIRED_ERROR
        ),
    ))
    def test_validate_required_fields_for_list_events(
            self, company_user_client, param, value, emsg):
        query_params = {param: value}
        resp = api_requests.get_events(
            company_user_client,
            query_params=query_params
        )
        validators.validate_error_message(resp, emsg)

    def test_create_event_fails_if_event_owner_not_in_attendees_list(
            self, company_user_client, event_data):
        data = copy.deepcopy(event_data)
        data['colleagues'] = []
        resp = api_requests.create_event(company_user_client, data)
        emsg = constants.ATTENDEES_LIST_SHOULD_CONTAIN_EVENT_OWNER_ERROR
        validators.validate_error_message(resp, emsg)

    def test_update_event_fails_if_event_owner_not_in_attendees_list(
            self, company_user_client, event_data, event):
        data = copy.deepcopy(event_data)
        data['colleagues'] = []
        resp = api_requests.update_event(
            company_user_client, event['id'], data)
        emsg = constants.ATTENDEES_LIST_SHOULD_CONTAIN_EVENT_OWNER_ERROR
        validators.validate_error_message(resp, emsg)


class TestEvent:

    def test_create_event(self, company_user_client, event_data, mailoutbox):
        resp = api_requests.create_event(company_user_client, event_data)
        assert resp.status_code == http.HTTPStatus.CREATED
        assert resp.json()['time_from'] == event_data['time_from']
        assert resp.json()['time_to'] == event_data['time_to']
        assert len(mailoutbox) == 1

    @pytest.mark.parametrize(('fixture', 'count'), (
        (
            'event_interview',
            1
        ),
        (
            'event_screening',
            0
        )
    ))
    def test_filter_events_by_type(
            self, event, company_user_client, request, fixture, count):
        event_type = request.getfixturevalue(fixture)
        query_params = {
            'type': event_type['id']
        }
        resp = api_requests.get_events(
            company_user_client,
            query_params=query_params
        )
        assert resp.status_code == http.HTTPStatus.OK
        assert len(resp.json()) == count

    @pytest.mark.parametrize(('query_params', 'count'), (
        # TODO (i.bogretsov) add more tests for filter by day or month
        (
            {
                'day': str(timezone.now().date()),
            },
            1
        ),
        (
            {
                'day': str(timezone.now().date() + datetime.timedelta(days=1))
            },
            0
        ),
        (
            {
                'month': str(timezone.now().date())
            },
            1
        ),
        (
            {
                'month': str(
                    timezone.now().date() + datetime.timedelta(days=40)
                )
            },
            0
        ),
    ))
    def test_filter_events_by_date(
            self, event, company_user_client, query_params, count, tz_london):
        query_params['tz'] = tz_london
        resp = api_requests.get_events(
            company_user_client,
            query_params=query_params
        )
        assert resp.status_code == http.HTTPStatus.OK
        assert len(resp.json()) == count

    @pytest.mark.parametrize(('fixture', 'count'), (
        (
            'company_user_client',
            1
        ),
        (
            'company_user_2_client',
            0
        )
    ))
    def test_filter_events_by_owner(self, event, request, fixture, count):
        client = request.getfixturevalue(fixture)
        query_params = {
            'is_owner': 'true'
        }
        resp = api_requests.get_events(client, query_params=query_params)
        assert resp.status_code == http.HTTPStatus.OK
        assert len(resp.json()) == count

    def test_update_event_subject_read_only(
            self, company_user_client, event, event_data):
        data = copy.deepcopy(event_data)
        data['subject'] = 'new subject'
        resp = api_requests.update_event(
            company_user_client,
            event['id'],
            data
        )
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['subject'] == event['subject']

    def test_update_event_description(
            self, company_user_client, event, event_data):
        data = copy.deepcopy(event_data)
        data['description'] = 'new description'
        resp = api_requests.update_event(
            company_user_client,
            event['id'],
            data
        )
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['description'] == data['description']

    def test_update_location(
            self, company_user_client, event,
            event_data, candidate, city_ashville, zip_ashville):
        data = copy.deepcopy(event_data)
        data['location']['city'] = city_ashville.id
        data['location']['zip'] = zip_ashville.id
        data['location']['address'] = 'new address'
        resp = api_requests.update_event(
            company_user_client,
            event['id'],
            data
        )
        assert resp.status_code == http.HTTPStatus.OK
        loca_act = resp.json()['location']
        assert loca_act['address'] == data['location']['address']
        assert loca_act['city']['name'] == city_ashville.name
        assert loca_act['zip']['code'] == zip_ashville.code

    def test_add_one_more_candidate(
            self, company_user_client, event,
            event_data, candidate_one, candidate_two, mailoutbox):
        mailoutbox.clear()
        data = copy.deepcopy(event_data)
        data['candidates'].append(candidate_two['job_seeker']['user']['id'])
        resp = api_requests.update_event(
            company_user_client,
            event['id'],
            data
        )
        assert resp.status_code == http.HTTPStatus.OK
        assert len(resp.json()['candidates']) == len(data['candidates'])
        assert len(mailoutbox) == 1

    def test_add_one_new_candidate_and_drop_one_old(
            self, event_two_candidates, company_user_client,
            event_base_data, candidate_one, candidate_three, mailoutbox):
        mailoutbox.clear()
        data = copy.deepcopy(event_base_data)
        data['job'] = candidate_one['job']['id']
        data['candidates'] = [
            candidate_one['job_seeker']['user']['id'],
            candidate_three['job_seeker']['user']['id']
        ]
        resp = api_requests.update_event(
            company_user_client,
            event_two_candidates['id'],
            data
        )
        assert resp.status_code == http.HTTPStatus.OK
        act_candidates_ids = set(
            i['user']['id'] for i in resp.json()['candidates']
        )
        assert act_candidates_ids == set(data['candidates'])
        assert len(mailoutbox) == 2

    def test_rejected_candidate_automaticaly_deleted_from_attendees(
            self, company_user_client, cand_status_rejected,
            event_two_candidates, candidate_one, candidate_two,
            mailoutbox):
        mailoutbox.clear()
        data = {'status': cand_status_rejected['id']}
        resp = api_requests.update_candidate_status(
            company_user_client,
            candidate_one['id'],
            data
        )
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['id'] == data['status']
        assert len(mailoutbox) == 1
        resp = api_requests.get_event_details(
            company_user_client,
            event_two_candidates['id']
        )
        assert resp.status_code == http.HTTPStatus.OK
        assert len(resp.json()['candidates']) == 1
        assert (resp.json()['candidates'][0]['user']['id'] ==
                candidate_two['job_seeker']['user']['id'])


class TestEventPermission:

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
    def test_get_events(self, request, client, status):
        client = request.getfixturevalue(client)
        resp = api_requests.get_events(client)
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
            http.HTTPStatus.CREATED
        ),
    ))
    def test_create_event(
            self, request, client, status, event_base_data, candidate):
        data = copy.deepcopy(event_base_data)
        data['candidates'] = [candidate['job_seeker']['user']['id']]
        data['job'] = candidate['job']['id']
        client = request.getfixturevalue(client)
        resp = api_requests.create_event(client, data)
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
            http.HTTPStatus.OK
        ),
    ))
    def test_get_event_details(self, request, client, status, event):
        client = request.getfixturevalue(client)
        resp = api_requests.get_event_details(client, event['id'])
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
        ),
    ))
    def test_delete_event(self, request, client, status, event):
        client = request.getfixturevalue(client)
        resp = api_requests.delete_event(client, event['id'])
        assert resp.status_code == status

    # TODO (i.bogretsov) add more tests for permisions
