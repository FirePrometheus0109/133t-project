import http

import pytest
from django.contrib.auth import models

from letter_template import constants
from permission import constants as perm_constants
from tests import api_requests
from tests import validators


class TestLetterTemplatePermissions:

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
    def test_get_list_letter_templates(
            self, request, client, status):
        client = request.getfixturevalue(client)
        resp = api_requests.get_letter_templates_list(client)
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
    def test_create_letter_template(
            self, request, client, status, letter_template_data):
        client = request.getfixturevalue(client)
        resp = api_requests.create_letter_template(
            client,
            letter_template_data)
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
    def test_get_details_letter_template(
            self, request, client, status, letter_template):
        client = request.getfixturevalue(client)
        resp = api_requests.get_letter_template_details(
            client,
            letter_template['id'])
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
    def test_update_letter_template(
            self, request, client, status,
            letter_template_data, letter_template):
        client = request.getfixturevalue(client)
        resp = api_requests.update_letter_template(
            client,
            letter_template['id'],
            letter_template_data)
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
    def test_delete_letter_template(
            self, request, client, status, letter_template):
        client = request.getfixturevalue(client)
        resp = api_requests.delete_letter_template(
            client,
            letter_template['id'])
        assert resp.status_code == status

    def test_cu_without_manage_letter_templates_group_cant_view_templates(
            self, company_user, company_user_client, letter_template):
        letter_template_group = models.Group.objects.get_by_natural_key(
            perm_constants.MANAGE_LETTER_TEMPLATE_GROUP
        )
        company_user.user.groups.remove(letter_template_group)

        resp = api_requests.get_letter_templates_list(company_user_client)
        assert resp.status_code == http.HTTPStatus.FORBIDDEN

        resp = api_requests.get_letter_template_details(
            company_user_client, letter_template['id']
        )
        assert resp.status_code == http.HTTPStatus.FORBIDDEN


class TestLetterTemplateValidate:

    def test_create_letter_template_max_count(
            self, company_user_client, settings,
            letter_template, letter_template_data):
        data = letter_template_data.copy()
        data['name'] = 'max count'
        settings.MAX_COUNT_OF_LETTER_TEMPLATES_FOR_COMPANY = 1
        resp = api_requests.create_letter_template(company_user_client, data)
        emsg = constants.MAXIMUM_OF_LETTER_TEMPLATES_ERROR
        validators.validate_error_message(resp, emsg)

    def test_create_letter_template_name_exists(
            self, company_user_client, letter_template, letter_template_data):
        resp = api_requests.create_letter_template(
            company_user_client,
            letter_template_data
        )
        emsg = constants.LETTER_TEMPLATE_NAME_NOT_UNIQUE_ERROR
        validators.validate_error_message(resp, emsg, 'name')

    def test_update_letter_template_name_exists(
            self, company_user_client,
            letter_template, letter_template_2,
            letter_template_data):
        data = letter_template_data.copy()
        data['name'] = letter_template_2['name']
        resp = api_requests.update_letter_template(
            company_user_client,
            letter_template['id'],
            data
        )
        emsg = constants.LETTER_TEMPLATE_NAME_NOT_UNIQUE_ERROR
        validators.validate_error_message(resp, emsg, 'name')


class TestLetterTemplate:

    @pytest.mark.parametrize(('query_params', 'count'), (
        (
            {
                'search': 'name'
            },
            2
        ),
        (
            {
                'search': 'nomatch'
            },
            0
        ),
        (
            {
                'search': 'second'
            },
            1
        )
    ))
    def test_search_by_name(
            self, company_user_client, query_params,
            letter_template, letter_template_2, count):
        resp = api_requests.get_letter_templates_list(
            company_user_client,
            query_params=query_params
        )
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == count

    @pytest.mark.parametrize(('order_by', 'fields'), (
        (
            'name',
            ['name']
        ),
        (
            '-modified_at',
            ['modified_at']
        ),
    ))
    def test_ordering(
            self, company_user_client, order_by, fields,
            letter_template, mock_tomorrow, letter_template_2):
        resp = api_requests.get_letter_templates_list(
            company_user_client,
            query_params={'ordering': order_by}
        )
        assert resp.status_code == http.HTTPStatus.OK
        validators.validate_ordering(resp.json()['results'], order_by, fields)

    def test_create_lt_with_event_type_other_lt_with_same_event_type_exists(
            self, company_user_client, letter_template,
            letter_template_data, event_interview):
        data = letter_template_data.copy()
        data['event_type'] = event_interview['id']
        data['name'] = 'new'
        resp = api_requests.create_letter_template(company_user_client, data)
        assert resp.status_code == http.HTTPStatus.CREATED
        assert resp.json()['event_type']['name'] == event_interview['name']
        # check letter template which had event_type
        resp = api_requests.get_letter_template_details(
            company_user_client,
            letter_template['id']
        )
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['event_type'] is None

    def test_update_lt_add_event_type_other_lt_with_same_event_type_exists(
            self, company_user_client, letter_template, letter_template_2,
            letter_template_data, event_interview):
        data = letter_template_data.copy()
        data['event_type'] = event_interview['id']
        data['name'] = letter_template_2['name']
        resp = api_requests.update_letter_template(
            company_user_client,
            letter_template_2['id'],
            data
        )
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['event_type']['name'] == event_interview['name']
        # check letter template which had event_type
        resp = api_requests.get_letter_template_details(
            company_user_client,
            letter_template['id']
        )
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['event_type'] is None

    def test_letter_template_other_company_does_not_see_letter_template(
            self, company_2_user_client, letter_template):
        resp = api_requests.get_letter_templates_list(company_2_user_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == 0
