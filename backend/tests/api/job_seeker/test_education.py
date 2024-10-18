import http
from unittest import mock

import pytest

from job_seeker import constants
from tests import api_requests
from tests import utils
from tests import validators
from tests.api.job_seeker import expected


class TestEducationsApi:

    def test_add_education(
            self, job_seeker_client, job_seeker, education_data):
        resp = api_requests.add_education(
            job_seeker_client,
            job_seeker.id,
            education_data)
        assert resp.status_code == http.HTTPStatus.CREATED

    def test_update_education(
            self, job_seeker_client, job_seeker, education, education_data):
        data = education_data.copy()
        data['institution'] = 'new institution'
        resp = api_requests.update_education(
            job_seeker_client,
            job_seeker.id,
            education['id'],
            data)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['institution'] == data['institution']

    def test_get_get_job_seeker_educations(
            self, job_seeker_client, job_seeker, educations):
        resp = api_requests.get_educations(
            job_seeker_client,
            job_seeker.id)
        assert resp.status_code == http.HTTPStatus.OK
        resp_data = resp.json()['results']
        assert resp_data == expected.EXPECTED_JOB_SEEKER_EDUCATION_LIST


class TestEducationsValidation:

    def test_add_education_max_count_of_educations_and_certifications(
            self, job_seeker_client, job_seeker, education_data):
        for _ in range(constants.MAX_COUNT_OF_EDUCATION):
            resp = api_requests.add_education(
                job_seeker_client,
                job_seeker.id,
                education_data)
            assert resp.status_code == http.HTTPStatus.CREATED
        resp = api_requests.add_education(
            job_seeker_client,
            job_seeker.id,
            education_data)
        emsg = constants.MAXIMUM_OF_EDUCATION_ENTRIES_ERROR
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
    def test_add_education_invalid_dates(
            self, job_seeker, job_seeker_client, education_data,
            invalid_data, current_date, field, emsg):
        data = education_data.copy()
        data.update(invalid_data)
        mockname = 'django.utils.timezone.now'
        with mock.patch(mockname, new=lambda: current_date):
            resp = api_requests.add_education(
                job_seeker_client,
                job_seeker.id,
                data)
            if field:
                validators.validate_error_message(resp, emsg, field)
            else:
                validators.validate_error_message(resp, emsg)


class TestEducationsPermissions:

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
    def test_add_education(
            self, request, client, status, education_data, job_seeker):
        client = request.getfixturevalue(client)
        resp = api_requests.add_education(
            client,
            job_seeker.id,
            education_data)
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
            'company_user_client',
            http.HTTPStatus.FORBIDDEN,
        ),
    ))
    def test_update_education(
            self, request, client, status,
            job_seeker, education, education_data):
        client = request.getfixturevalue(client)
        resp = api_requests.update_education(
            client,
            job_seeker.id,
            education['id'],
            education_data)
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
    def test_delete_education(
            self, request, client, status, job_seeker, education):
        client = request.getfixturevalue(client)
        resp = api_requests.delete_education(
            client,
            job_seeker.id,
            education['id'])
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
    def test_get_list_education(
            self, request, client, status, job_seeker, education):
        client = request.getfixturevalue(client)
        resp = api_requests.get_educations(
            client,
            job_seeker.id)
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
    def test_get_education_details(
            self, request, client, status, job_seeker, education):
        client = request.getfixturevalue(client)
        resp = api_requests.get_education_detail(
            client,
            job_seeker.id,
            education['id'])
        assert resp.status_code == status


class TestCertificationsApi:

    def test_add_certification(
            self, job_seeker_client, job_seeker, certification_data):
        resp = api_requests.add_certification(
            job_seeker_client,
            job_seeker.id,
            certification_data)
        assert resp.status_code == http.HTTPStatus.CREATED

    def test_update_certification(
            self, job_seeker_client, job_seeker,
            certification, certification_data):
        data = certification_data.copy()
        data['institution'] = 'new institution'
        resp = api_requests.update_certification(
            job_seeker_client,
            job_seeker.id,
            certification['id'],
            data)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['institution'] == data['institution']

    def test_get_get_job_seeker_certifications(
            self, job_seeker_client, job_seeker, certifications):
        resp = api_requests.get_certifications(
            job_seeker_client,
            job_seeker.id)
        assert resp.status_code == http.HTTPStatus.OK
        resp_data = resp.json()['results']
        assert resp_data == expected.EXPECTED_JOB_SEEKER_CERTIFICATION_LIST


class TestCertificationValidation:

    def test_add_certification_max_count_of_educations_and_certifications(
            self, job_seeker_client, job_seeker, certification_data):
        for _ in range(constants.MAX_COUNT_OF_EDUCATION):
            resp = api_requests.add_certification(
                job_seeker_client,
                job_seeker.id,
                certification_data)
            assert resp.status_code == http.HTTPStatus.CREATED
        resp = api_requests.add_certification(
            job_seeker_client,
            job_seeker.id,
            certification_data)
        emsg = constants.MAXIMUM_OF_EDUCATION_ENTRIES_ERROR
        validators.validate_error_message(resp, emsg)

    def test_add_certification_gradueted_to_and_is_current(
            self, job_seeker_client, job_seeker, certification_data):
        data = certification_data.copy()
        data['is_current'] = True
        resp = api_requests.add_certification(
            job_seeker_client,
            job_seeker.id,
            data)
        emsg = constants.CERTIFICATION_IS_CURRENT_ERROR
        validators.validate_error_message(resp, emsg)

    def test_add_certification_no_gradueted_to_and_is_not_current(
            self, job_seeker_client, job_seeker, certification_data):
        data = certification_data.copy()
        data.pop('graduated')
        resp = api_requests.add_certification(
            job_seeker_client,
            job_seeker.id,
            data)
        emsg = constants.CERTIFICATION_IS_NOT_CURRENT_ERROR
        validators.validate_error_message(resp, emsg)

    def test_add_certification_licence_number_to_and_is_current(
            self, job_seeker_client, job_seeker, certification_data):
        data = certification_data.copy()
        data.pop('graduated')
        data['is_current'] = True
        resp = api_requests.add_certification(
            job_seeker_client,
            job_seeker.id,
            data)
        emsg = constants.CERTIFICATION_IS_CURRENT_ERROR
        validators.validate_error_message(resp, emsg)

    def test_add_certification_no_licence_number_to_and_is_not_current(
            self, job_seeker_client, job_seeker, certification_data):
        data = certification_data.copy()
        data.pop('licence_number')
        resp = api_requests.add_certification(
            job_seeker_client,
            job_seeker.id,
            data)
        emsg = constants.CERTIFICATION_IS_NOT_CURRENT_ERROR
        validators.validate_error_message(resp, emsg)


class TestCertificationsPermissions:

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
    def test_add_certification(
            self, request, client, status, certification_data, job_seeker):
        client = request.getfixturevalue(client)
        resp = api_requests.add_certification(
            client,
            job_seeker.id,
            certification_data)
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
            'company_user_client',
            http.HTTPStatus.FORBIDDEN,
        ),
    ))
    def test_update_certification(
            self, request, client, status,
            job_seeker, certification, certification_data):
        client = request.getfixturevalue(client)
        resp = api_requests.update_certification(
            client,
            job_seeker.id,
            certification['id'],
            certification_data)
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
    def test_delete_certification(
            self, request, client, status, job_seeker, certification):
        client = request.getfixturevalue(client)
        resp = api_requests.delete_certification(
            client,
            job_seeker.id,
            certification['id'])
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
    def test_get_list_certification(
            self, request, client, status, job_seeker, certification):
        client = request.getfixturevalue(client)
        resp = api_requests.get_certifications(
            client,
            job_seeker.id)
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
    def test_get_certification_details(
            self, request, client, status, job_seeker, certification):
        client = request.getfixturevalue(client)
        resp = api_requests.get_certification_detail(
            client,
            job_seeker.id,
            certification['id'])
        assert resp.status_code == status
