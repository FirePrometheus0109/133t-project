import http
from unittest import mock

import pytest
from django.utils import timezone

from job_seeker import constants
from tests import api_requests
from tests import utils
from tests import validators
from tests.api.job_seeker import expected


class TestJobExperienceApi:

    def test_add_job_experience(
            self, job_seeker, job_seeker_client,
            job_experience_data):
        resp = api_requests.add_job_experience(
            job_seeker_client, job_seeker.id, job_experience_data)
        assert resp.status_code == http.HTTPStatus.CREATED
        assert resp.json() == expected.EXPECTED_JOB_EXPERIENCE

    def test_get_list_job_experience(
            self, job_seeker, job_seeker_client, job_experience):
        resp = api_requests.get_job_experience(
            job_seeker_client,
            job_seeker.id)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['results']
        assert resp.json()['count'] == 1

    def test_get_job_experience(
            self, job_seeker, job_seeker_client, job_experience):
        resp = api_requests.get_job_experience_details(
            job_seeker_client,
            job_seeker.id,
            job_experience['id'])
        assert resp.status_code == http.HTTPStatus.OK

    def test_update_job_experience(
            self, job_seeker, job_seeker_client,
            job_experience_data, job_experience):
        data = job_experience_data.copy()
        data['job_title'] = 'new job title'
        resp = api_requests.update_job_experience(
            job_seeker_client,
            job_seeker.id,
            job_experience['id'],
            data)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['job_title'] == data['job_title']

    def test_cant_update_owner_job_experience(
            self, job_seeker, job_seeker_2, job_seeker_client,
            job_experience_data, job_experience):
        data = job_experience_data.copy()
        data['owner'] = job_seeker_2.id
        resp = api_requests.update_job_experience(
            job_seeker_client,
            job_seeker.id,
            job_experience['id'],
            data)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['owner'] != data['owner']

    def test_job_seeker_can_add_more_than_one_current_job(
            self, job_seeker, job_seeker_client, job_experience_data):
        for _ in range(2):
            resp = api_requests.add_job_experience(
                job_seeker_client,
                job_seeker.id,
                job_experience_data)
            assert resp.status_code == http.HTTPStatus.CREATED


class TestJobExperienceValidate:

    @pytest.mark.parametrize(('field',), (
        ('company',), ('job_title',), ('date_from',)
    ))
    def test_add_job_experience_required_fields_errors(
            self, job_seeker, job_seeker_client,
            field, job_experience_data):
        data = job_experience_data.copy()
        data.pop(field)
        resp = api_requests.add_job_experience(
            job_seeker_client, job_seeker.id, data)
        assert resp.status_code == http.HTTPStatus.BAD_REQUEST

    def test_add_job_experience_max_10_entries(
            self, job_seeker, job_seeker_client,
            job_experience_data):
        for _ in range(10):
            resp = api_requests.add_job_experience(
                job_seeker_client, job_seeker.id, job_experience_data)
            assert resp.status_code == http.HTTPStatus.CREATED

        resp = api_requests.add_job_experience(
            job_seeker_client, job_seeker.id, job_experience_data)
        emsg = constants.MAXIMUM_OF_JOB_EXPERIENCE_ERROR
        validators.validate_error_message(resp, emsg)

    @pytest.mark.parametrize(
        ('invalid_data', 'current_date', 'field', 'emsg'), (
            (
                {
                    'date_from': str(utils.date(2018, 1, 1)),
                    'date_to': str(utils.date(2016, 1, 1)),
                },
                utils.date(2017, 1, 1),
                'date_from',
                constants.DATES_FROM_FUTURE_ERROR
            ),
            (
                {
                    'date_from': str(utils.date(2016, 1, 1)),
                    'date_to': str(utils.date(2018, 1, 1)),
                },
                utils.date(2017, 1, 1),
                'date_to',
                constants.DATES_FROM_FUTURE_ERROR
            ),
            (
                {
                    'date_from': str(utils.date(2018, 1, 1)),
                    'date_to': str(utils.date(2017, 1, 1)),
                },
                utils.date(2018, 9, 1),
                '',
                constants.DATE_FROM_GREATER_DATE_TO_ERROR
            ),
        )
    )
    def test_add_job_experience_invalid_date_experince(
            self, job_seeker, job_seeker_client, job_experience_data,
            invalid_data, current_date, field, emsg):
        data = job_experience_data.copy()
        data.update(invalid_data)
        mockname = 'django.utils.timezone.now'
        with mock.patch(mockname, new=lambda: current_date):
            resp = api_requests.add_job_experience(
                job_seeker_client,
                job_seeker.id,
                data)
            if field:
                validators.validate_error_message(resp, emsg, field)
            else:
                validators.validate_error_message(resp, emsg)

    def test_add_job_experience_is_current_and_date_to(
            self, job_seeker, job_seeker_client, job_experience_data):
        data = job_experience_data.copy()
        data['date_to'] = str(timezone.now())
        resp = api_requests.add_job_experience(
            job_seeker_client,
            job_seeker.id,
            data)
        emsg = constants.DATE_TO_AND_IS_CURRENT_ERROR
        validators.validate_error_message(resp, emsg)

    def test_add_job_experience_not_is_current_and_no_date_to(
            self, job_seeker, job_seeker_client, job_experience_data):
        data = job_experience_data.copy()
        data['is_current'] = False
        resp = api_requests.add_job_experience(
            job_seeker_client,
            job_seeker.id,
            data)
        emsg = constants.NO_DATE_TO_AND_NOT_IS_CURRENT_ERROR
        validators.validate_error_message(resp, emsg)

    def test_max_length_job_experience_description(
            self, job_seeker, job_seeker_client, job_experience_data):
        data = job_experience_data.copy()
        data['description'] = ''.join(['a' for _ in range(4001)])
        resp = api_requests.add_job_experience(
            job_seeker_client,
            job_seeker.id,
            data)
        assert resp.status_code == http.HTTPStatus.BAD_REQUEST
        assert resp.json()['field_errors']['description']


class TestJobExperiencePermissions:

    @pytest.mark.parametrize(('client', 'status'), (
        (
            'anonym_client',
            http.HTTPStatus.UNAUTHORIZED,
        ),
        (
            'job_seeker_client',
            http.HTTPStatus.CREATED,
        ),
        (
            'company_user_client',
            http.HTTPStatus.FORBIDDEN,
        ),
        (
            'job_seeker_2_client',
            http.HTTPStatus.FORBIDDEN,
        )
    ))
    def test_create_job_experience(
            self, request, client, status, job_experience_data, job_seeker):
        client = request.getfixturevalue(client)
        resp = api_requests.add_job_experience(
            client,
            job_seeker.id,
            job_experience_data)
        assert resp.status_code == status

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
            http.HTTPStatus.OK,
        ),
        (
            'job_seeker_2_client',
            http.HTTPStatus.FORBIDDEN,
        )
    ))
    def test_get_job_experience_details(
            self, request, client, status, job_seeker, job_experience):
        client = request.getfixturevalue(client)
        resp = api_requests.get_job_experience_details(
            client,
            job_seeker.id,
            job_experience['id'])
        assert resp.status_code == status

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
        (
            'job_seeker_2_client',
            http.HTTPStatus.FORBIDDEN,
        )
    ))
    def test_update_job_permissions(
            self, request, client, status,
            job_seeker, job_experience, job_experience_data):
        client = request.getfixturevalue(client)
        resp = api_requests.update_job_experience(
            client,
            job_seeker.id,
            job_experience['id'],
            job_experience_data)
        assert resp.status_code == status

    @pytest.mark.parametrize(('client', 'status'), (
        (
            'anonym_client',
            http.HTTPStatus.UNAUTHORIZED,
        ),
        (
            'job_seeker_client',
            http.HTTPStatus.NO_CONTENT,
        ),
        (
            'company_user_client',
            http.HTTPStatus.FORBIDDEN,
        ),
        (
            'job_seeker_2_client',
            http.HTTPStatus.FORBIDDEN,
        )
    ))
    def test_delete_job_experience(
            self, request, client, status, job_seeker, job_experience):
        client = request.getfixturevalue(client)
        resp = api_requests.delete_job_experience(
            client,
            job_seeker.id,
            job_experience['id'])
        assert resp.status_code == status

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
            http.HTTPStatus.OK,
        ),
        (
            'job_seeker_2_client',
            http.HTTPStatus.FORBIDDEN,
        )
    ))
    def test_get_list_job_experience(
            self, request, client, status, job_seeker):
        client = request.getfixturevalue(client)
        resp = api_requests.get_job_experience(client, job_seeker.id)
        assert resp.status_code == status
