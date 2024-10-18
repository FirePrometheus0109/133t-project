import http
import json

import pytest
from django import urls
from tests import api_requests
from tests import constants as test_constants

from company import constants
from leet import constants as leet_constants
from leet import enums
from permission import constants as perms_constants
from subscription import constants as subscription_constants
from tests import validators

class TestCompanyUsers:

    def test_create_company_user(
            self, company_user_client, company_user,
            invited_company_user_data, mailoutbox):
        mailoutbox.clear()
        resp = api_requests.create_company_user(
            company_user_client,
            invited_company_user_data)
        assert resp.status_code == http.HTTPStatus.CREATED
        assert (resp.json()['detail'] ==
                constants.COMPANY_USER_CREATE_SUCCESS_MESSAGE)
        assert len(mailoutbox) == 1

    def test_list_of_company_users(
            self, company_user_client, new_company_user):
        resp = api_requests.get_company_users(company_user_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == 2
        results = resp.json()['results']
        # TODO (i.bogretsov) add correct ordering validator
        assert results[0]['status'] == enums.CompanyUserStatusEnum.NEW.name
        assert results[1]['status'] == enums.CompanyUserStatusEnum.ACTIVE.name

    def test_company_user_has_status_active_after_activating(
            self, company_user_client, active_company_user):
        resp = api_requests.get_company_users(company_user_client)
        assert resp.status_code == http.HTTPStatus.OK
        for i in resp.json()['results']:
            assert i['status'] == enums.CompanyUserStatusEnum.ACTIVE.name

    def test_get_company_user(self, company_user_client, active_company_user):
        resp = api_requests.get_company_user(
            company_user_client,
            active_company_user['id'])
        assert resp.status_code == http.HTTPStatus.OK

    @pytest.mark.parametrize(('field', 'value'), (
        (
            'last_name',
            'new_last_name',
        ),
        (
            'first_name',
            'new_first_name',
        )
    ))
    def test_edit_company_user_safe_fields(
            self, company_user_client, company_user,
            field, value, invited_company_user_data):
        data = invited_company_user_data.copy()
        data[field] = value
        resp = api_requests.edit_company_user(
            company_user_client,
            company_user.id,
            data)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['user'][field] == value

    def test_disable_company_user(
            self, company_user_client,
            active_company_user, invited_company_user_data):
        data = invited_company_user_data.copy()
        data['status'] = enums.CompanyUserStatusEnum.DISABLED.name
        resp = api_requests.edit_company_user(
            company_user_client,
            active_company_user['id'],
            data)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['status'] == data['status']

    def test_change_permissions_for_company_user(
            self, company_user_client, active_company_user,
            permissions_groups, invited_company_user_data):
        data = invited_company_user_data.copy()
        data['permissions_groups'] = [permissions_groups[0]['id']]
        resp = api_requests.edit_company_user(
            company_user_client,
            active_company_user['id'],
            data)
        assert resp.status_code == http.HTTPStatus.OK
        actual_perms_groups = resp.json()['permissions_groups']
        assert len(actual_perms_groups) == 1
        group_name = actual_perms_groups[0]['permissions'][0]['name']
        assert group_name == permissions_groups[0]['name']

    def test_disabled_user_include_in_company_users_list(
            self, company_user_client, disabled_company_user):
        resp = api_requests.get_company_users(company_user_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == 2
        assert (
            resp.json()['results'][-1]['status'] ==
            enums.CompanyUserStatusEnum.DISABLED.name)

    def test_delete_company_user(
            self, company_user_client,
            active_company_user, anonym_client):
        resp = api_requests.delete_company_user(
            company_user_client,
            active_company_user['id'])
        assert resp.status_code == http.HTTPStatus.NO_CONTENT

        # check list of company users
        resp = api_requests.get_company_users(company_user_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == 1

        # check company user account
        resp = api_requests.get_company_user(
            company_user_client,
            active_company_user['id'])
        assert resp.status_code == http.HTTPStatus.NOT_FOUND

        # check login
        creds = {
            'email': active_company_user['user']['email'],
            'password': test_constants.DEFAULT_PASSWORD
        }
        resp = api_requests.login(anonym_client, creds)
        assert resp.status_code == http.HTTPStatus.BAD_REQUEST

    def test_patch_not_allowed(self, company_user_client, active_company_user):
        resp = company_user_client.patch(
            urls.reverse(
                'company:api_v1:company-user-detail',
                kwargs={'pk': active_company_user['id']}),
            data=json.dumps({}),
            content_type='application/json')
        assert resp.status_code == http.HTTPStatus.METHOD_NOT_ALLOWED

    def test_restore_company_user(
            self, company_user_client, deleted_company_user,
            invited_company_user_data, permissions_groups, mailoutbox):
        mailoutbox.clear()
        data = invited_company_user_data.copy()
        data['permissions_groups'] = [permissions_groups[0]['id']]

        resp = api_requests.restore_company_user(company_user_client, data)
        assert resp.status_code == http.HTTPStatus.OK
        assert len(mailoutbox) == 1
        assert 'restore' in mailoutbox[0].message().as_string()

        resp = api_requests.get_company_user(
            company_user_client,
            deleted_company_user['id'])
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['status'] == enums.CompanyUserStatusEnum.NEW.name
        perms_groups = resp.json()['permissions_groups']
        assert len(perms_groups) == 1
        group_id = perms_groups[0]['permissions'][0]['id']
        assert group_id == data['permissions_groups'][0]


class TestCompanyUsersValidate:

    def test_create_company_users_max_count(
            self, company_user_client, invited_company_user_data):
        for i in range(9):
            data = invited_company_user_data.copy()
            data['email'] += str(i)
            resp = api_requests.create_company_user(
                company_user_client,
                data)
            assert resp.status_code == http.HTTPStatus.CREATED
        resp = api_requests.create_company_user(
            company_user_client,
            invited_company_user_data)
        emsg = subscription_constants.PLAN_NUMBER_OF_USERS_EXCEEDED_ERROR.format(10)
        validators.validate_error_message(resp, emsg)

    def test_create_company_user_with_email_exists(
            self, company_user_client, invited_company_user_data):
        data = invited_company_user_data.copy()
        data['email'] = test_constants.COMPANY_USER_EMAIL
        resp = api_requests.create_company_user(
            company_user_client,
            data)
        emsg = leet_constants.USER_WITH_CERTAIN_EMAIL_EXISTS
        validators.validate_error_message(resp, emsg, 'email')

    def test_create_company_user_invalid_email(
            self, company_user_client, invited_company_user_data):
        data = invited_company_user_data.copy()
        data['email'] = 'invalid'
        resp = api_requests.create_company_user(
            company_user_client,
            data)
        assert resp.status_code == http.HTTPStatus.BAD_REQUEST

    @pytest.mark.parametrize(('field',), (
        (
            'first_name',
        ),
        (
            'last_name',
        ),
        (
            'email',
        ),
        (
            'permissions_groups',
        )
    ))
    def test_create_company_user_no_required_fields(
            self, company_user_client, field, invited_company_user_data):
        data = invited_company_user_data.copy()
        data.pop(field)
        resp = api_requests.create_company_user(
            company_user_client,
            data)
        assert resp.status_code == http.HTTPStatus.BAD_REQUEST

    def test_update_status_user_is_owner(
            self, company_user_client,
            company_user, invited_company_user_data):
        data = invited_company_user_data.copy()
        data['status'] = enums.CompanyUserStatusEnum.DISABLED.name
        resp = api_requests.edit_company_user(
            company_user_client,
            company_user.id,
            data)
        emsg = constants.USER_CAN_NOT_UPDATE_HIS_STATUS_ERROR
        validators.validate_error_message(resp, emsg, 'status')

    @pytest.mark.parametrize(('groups_names', 'expected'), (
        (
            [perms_constants.MANAGE_COMPANY_USERS_GROUP],
            [perms_constants.MANAGE_SUBSCRIPTION_PLAN_GROUP],
        ),
        (
            [perms_constants.MANAGE_SUBSCRIPTION_PLAN_GROUP],
            [perms_constants.MANAGE_COMPANY_USERS_GROUP],
        ),
        (
            [],
            [
                perms_constants.MANAGE_SUBSCRIPTION_PLAN_GROUP,
                perms_constants.MANAGE_COMPANY_USERS_GROUP,
            ],
        )
    ))
    def test_update_permissions_groups_no_users_with_group_in_company(
            self, company_user_client, company_user,
            permissions_groups, groups_names,
            invited_company_user_data, expected):
        groups_ids = [
            g['id'] for g in permissions_groups
            if g['name'] in groups_names
        ]
        data = invited_company_user_data.copy()
        data['permissions_groups'] = groups_ids
        resp = api_requests.edit_company_user(
            company_user_client,
            company_user.id,
            data)
        assert resp.status_code == http.HTTPStatus.BAD_REQUEST
        errors = sorted(resp.json()['field_errors']['permissions_groups'])
        groups_names = sorted(expected)
        for gname, error in zip(groups_names, errors):
            assert gname in error

    def test_update_status_for_new_company_user(
            self, company_user_client, new_company_user,
            invited_company_user_data):
        data = invited_company_user_data.copy()
        data['status'] = enums.CompanyUserStatusEnum.ACTIVE.name
        resp = api_requests.edit_company_user(
            company_user_client,
            new_company_user['id'],
            data)
        emsg = constants.CAN_NOT_UPDATE_STATUS_FOR_NEW_USER_ERROR
        validators.validate_error_message(resp, emsg, 'status')

    def test_not_valid_choice_for_changing_user_status(
            self, company_user_client, active_company_user,
            invited_company_user_data):
        data = invited_company_user_data.copy()
        data['status'] = enums.CompanyUserStatusEnum.NEW.name
        resp = api_requests.edit_company_user(
            company_user_client,
            active_company_user['id'],
            data)
        assert resp.status_code == http.HTTPStatus.BAD_REQUEST

    def test_activate_disabled_company_user_max_count_of_users(
            self, company_user_client, disabled_company_user,
            invited_company_user_data):
        for i in range(9):
            data = invited_company_user_data.copy()
            data['email'] = str(i) + data['email']
            resp = api_requests.create_company_user(
                company_user_client,
                data)
            assert resp.status_code == http.HTTPStatus.CREATED

        data = invited_company_user_data.copy()
        data['status'] = enums.CompanyUserStatusEnum.ACTIVE.name
        resp = api_requests.edit_company_user(
            company_user_client,
            disabled_company_user['id'],
            data)
        emsg = subscription_constants.PLAN_NUMBER_OF_USERS_EXCEEDED_ERROR.format(10)
        validators.validate_error_message(resp, emsg, 'status')

    def test_delete_company_user_his_account(
            self, company_user_client, company_user):
        resp = api_requests.delete_company_user(
            company_user_client,
            company_user.id)
        emsg = constants.CAN_NOT_DELETE_OWN_ACCOUNT
        validators.validate_error_message(resp, emsg)

    def test_create_company_user_deleted_user_exists_with_certain_email(
            self, company_user_client,
            active_company_user, invited_company_user_data):
        resp = api_requests.delete_company_user(
            company_user_client,
            active_company_user['id'])
        assert resp.status_code == http.HTTPStatus.NO_CONTENT
        resp = api_requests.create_company_user(
            company_user_client,
            invited_company_user_data)
        emsg = constants.COMPANY_USER_WITH_CERTAIN_EMAIL_EXISTS
        validators.validate_error_message(resp, emsg, 'email')

    def test_restore_company_user_is_not_deleted(
            self, company_user_client,
            active_company_user, invited_company_user_data):
        resp = api_requests.restore_company_user(
            company_user_client,
            invited_company_user_data)
        emsg = constants.NO_DELETED_COMPANY_USERS_ERROR
        validators.validate_error_message(resp, emsg, 'email')


class TestCompanyAdminCRUDLPermissions:

    @pytest.mark.parametrize(('client', 'status'), (
        (
            'anonym_client',
            http.HTTPStatus.UNAUTHORIZED
        ),
        (
            'company_user_client',
            http.HTTPStatus.OK
        ),
        (
            'job_seeker_client',
            http.HTTPStatus.FORBIDDEN
        )
    ))
    def test_get_list_company_users(
            self, request, client, status):
        client = request.getfixturevalue(client)
        resp = api_requests.get_company_users(client)
        assert resp.status_code == status

    @pytest.mark.parametrize(('client', 'status'), (
        (
            'anonym_client',
            http.HTTPStatus.UNAUTHORIZED
        ),
        (
            'company_user_client',
            http.HTTPStatus.CREATED
        ),
        (
            'job_seeker_client',
            http.HTTPStatus.FORBIDDEN
        )
    ))
    def test_create_company_user(
            self, request, client,
            status, invited_company_user_data):
        client = request.getfixturevalue(client)
        resp = api_requests.create_company_user(
            client,
            invited_company_user_data)
        assert resp.status_code == status

    @pytest.mark.parametrize(('client', 'status'), (
        (
            'anonym_client',
            http.HTTPStatus.UNAUTHORIZED
        ),
        (
            'company_user_client',
            http.HTTPStatus.OK
        ),
        (
            'job_seeker_client',
            http.HTTPStatus.FORBIDDEN
        )
    ))
    def test_get_company_user(
            self, request, client, status, company_user):
        client = request.getfixturevalue(client)
        resp = api_requests.get_company_user(client, company_user.id)
        assert resp.status_code == status

    @pytest.mark.parametrize(('client', 'status'), (
        (
            'anonym_client',
            http.HTTPStatus.UNAUTHORIZED
        ),
        (
            'company_user_client',
            http.HTTPStatus.OK
        ),
        (
            'job_seeker_client',
            http.HTTPStatus.FORBIDDEN
        )
    ))
    def test_edit_company_user(
            self, request, client, status, company_user,
            invited_company_user_data):
        client = request.getfixturevalue(client)
        data = invited_company_user_data.copy()
        data['last_name'] = 'test'
        resp = api_requests.edit_company_user(client, company_user.id, data)
        assert resp.status_code == status

    @pytest.mark.parametrize(('client', 'status'), (
        (
            'anonym_client',
            http.HTTPStatus.UNAUTHORIZED
        ),
        (
            'company_user_client',
            http.HTTPStatus.NO_CONTENT
        ),
        (
            'job_seeker_client',
            http.HTTPStatus.FORBIDDEN
        )
    ))
    def test_delete_company_user(
            self, request, client, status, active_company_user):
        client = request.getfixturevalue(client)
        resp = api_requests.delete_company_user(
            client, active_company_user['id'])
        assert resp.status_code == status

    @pytest.mark.parametrize(('client', 'status'), (
        (
            'anonym_client',
            http.HTTPStatus.UNAUTHORIZED
        ),
        (
            'company_user_client',
            http.HTTPStatus.OK
        ),
        (
            'job_seeker_client',
            http.HTTPStatus.FORBIDDEN
        )
    ))
    def test_restore_company_user(
            self, request, client, status,
            deleted_company_user, invited_company_user_data):
        client = request.getfixturevalue(client)
        resp = api_requests.restore_company_user(
            client,
            invited_company_user_data)
        assert resp.status_code == status
