import http

import faker
import pytest
from django.forms.models import model_to_dict

from company import models
from geo import constants
from permission import constants as perm_constants
from tests import api_requests
from tests import utils
from tests import validators
from tests.api.company import expected

fake = faker.Faker()

EXPECTED_COMPANY_DETAIL_FIELDS = {
    'id',
    'name',
    'description',
    'phone',
    'fax',
    'website',
    'email',
    'address',
    'industry',
    'photo',
}


def validate_company(actual_dict, expected_dict):   # noqa
    company_flat_fields = ['name', 'description', 'phone', 'fax',
                           'website', 'email']
    for field in company_flat_fields:
        assert actual_dict[field] == expected_dict[field]
    address_flat_fields = ['address', 'zip']
    for field in address_flat_fields:
        assert actual_dict['address'][field] == expected_dict['address'][field]
    assert (
        actual_dict['address']['country']['id'] ==
        expected_dict['address']['country'])
    assert (
        actual_dict['address']['city']['id'] ==
        expected_dict['address']['city'])
    assert (
        actual_dict['industry']['id'] ==
        expected_dict['industry']
    )


class TestCompanyApiCommon:

    @pytest.mark.parametrize(('update_method',), (
        (
            api_requests.update_company,
        ),
        (
            api_requests.partial_update_company,
        ),
    ))
    def test_anonymous_cant_update_patch_company(
            self, anonym_client, company, update_method):
        resp = update_method(
            anonym_client,
            company.id,
            {})
        assert resp.status_code == http.HTTPStatus.UNAUTHORIZED

    def test_job_seeker_cant_get_company_via_private_url(
            self, job_seeker_client, company):
        resp = api_requests.get_company(job_seeker_client, company.id)
        assert resp.status_code == http.HTTPStatus.FORBIDDEN

    def test_job_seeker_cant_update_company(
            self, job_seeker_client, company):
        resp = api_requests.update_company(job_seeker_client, company.id,
                                           data={})
        assert resp.status_code == http.HTTPStatus.FORBIDDEN

    def test_update_company_not_company_user(
            self, company_2_user_client, company):
        resp = api_requests.partial_update_company(
            company_2_user_client,
            company.id,
            data={})
        assert resp.status_code == http.HTTPStatus.FORBIDDEN

    def test_update_company_success(
            self, company_user_client, company):
        company_info = utils.generate_random_company_info()
        resp = api_requests.update_company(
            company_user_client,
            company.id,
            company_info)
        assert resp.status_code == http.HTTPStatus.OK
        company = models.Company.objects.get(id=company.id)
        validate_company(self._company_object_to_dict(company), company_info)

    @staticmethod
    def _company_object_to_dict(company):
        company_dict = model_to_dict(company)
        address_dict = model_to_dict(company.address)
        country_dict = model_to_dict(company.address.country)
        city_dict = model_to_dict(company.address.city)
        industry_dict = model_to_dict(company.industry)
        address_dict.update(
            {'country': country_dict, 'city': city_dict}
        )
        company_dict.update({'address': address_dict})
        company_dict.update({'industry': industry_dict})
        return company_dict

    @pytest.mark.parametrize(('field', 'value'), (
        (
            'name',
            fake.company(),
        ),
        (
            'description',
            fake.text(),
        ),
        (
            'phone',
            fake.phone_number(),
        ),
        (
            'fax',
            fake.msisdn()
        ),
        (
            'website',
            fake.url()
        ),
        (
            'email',
            fake.email()
        )
    ))
    def test_partial_update_company(
            self, company_user_client, company, field, value):
        data = {field: value}
        resp = api_requests.partial_update_company(
            company_user_client,
            company.id,
            data)
        assert resp.status_code == http.HTTPStatus.OK
        company = models.Company.objects.get(id=company.id)
        assert getattr(company, field) == value

    def test_partial_update_company_address(
            self, company_user_client, company):
        data = {'address': fake.address()}
        resp = api_requests.partial_update_company(
            company_user_client,
            company.id,
            {'address': data})
        assert resp.status_code == http.HTTPStatus.OK
        company = models.Company.objects.get(id=company.id)
        assert getattr(company.address, 'address') == data['address']

    def test_partial_update_company_address_country(
            self, company_user_client, company, country_usa):
        data = {'country': country_usa.id}
        resp = api_requests.partial_update_company(
            company_user_client,
            company.id,
            {'address': data})
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['address']['country']['id'] == country_usa.id

    def test_partial_update_city_and_zip(
            self, company_user_client, company, city_ashville, zip_ashville):
        resp = api_requests.partial_update_company(
            company_user_client,
            company.id,
            {'address': {'city': city_ashville.id, 'zip': zip_ashville.id}})
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['address']['city']['id'] == city_ashville.id

    def test_partial_update_industry(
            self, company_user_client, company, industry_manufacturing):
        resp = api_requests.partial_update_company(
            company_user_client,
            company.id,
            {'industry': industry_manufacturing.id})
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['industry']['id'] == industry_manufacturing.id

    def test_partial_update_zip_zip_fails_when_doesnt_belong_to_the_city(
            self, company_user_client, company, zip_new_york, city_ashville):
        data = {
            'address': {
                'zip': zip_new_york.id,
                'city': city_ashville.id
            }
        }
        resp = api_requests.partial_update_company(
            company_user_client,
            company.id,
            data)
        emsg = constants.ZIP_SHOULD_BELONG_TO_THE_CITY
        validators.validate_error_message(resp, emsg, ['address', 'zip'])

    def test_update_company_description_max_length(
            self, company_user_client, company):
        description = ''.join('a' for _ in range(4001))
        data = {'description': description}
        resp = api_requests.partial_update_company(
            company_user_client,
            company.id,
            data)
        assert resp.status_code == http.HTTPStatus.BAD_REQUEST
        assert resp.json()['field_errors']['description']

    @pytest.mark.parametrize(('field',), (
        ('phone',), ('fax',)
    ))
    def test_update_invalid_length_phone_and_fax(
            self, company_user_client, company, field):
        value = ''.join('1' for _ in range(33))
        data = {field: value}
        resp = api_requests.partial_update_company(
            company_user_client,
            company.id,
            data)
        assert resp.status_code == http.HTTPStatus.BAD_REQUEST
        assert resp.json()['field_errors'][field]

    @pytest.mark.parametrize(('api_request',), (
        (
            api_requests.partial_update_company,
        ),
        (
            api_requests.update_company,
        ),
    ))
    def test_update_company_draft_address(
            self, company_draft_client, company_draft, api_request,
            country_usa, city_ashville, zip_ashville):
        data = {
            'name': 'draft company',
            'address': {
                'address': 'address',
                'country': country_usa.id,
                'city': city_ashville.id,
                'zip': zip_ashville.id
            }
        }
        resp = api_request(company_draft_client, company_draft.id, data)
        exp = expected.EXPECTED_ADDRESS_DATA_DRAFT_COMPANY
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['address'] == exp


class TestCompanyApiList:

    def test_list_success(
            self, anonym_client, companies_list,
            job, company_2_job):
        resp = api_requests.get_companies(anonym_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == len(companies_list)


class TestPublicCompanyApiRetrieve:

    def test_get_returns_appropriate_fields(
            self, anonym_client, company):
        resp = api_requests.get_public_company(
            anonym_client, company.id)
        assert resp.status_code == http.HTTPStatus.OK
        assert set(resp.json().keys()) == EXPECTED_COMPANY_DETAIL_FIELDS


class TestUpdateCompanyPhotoAPI:

    def test_update_company_photo_success(
            self, mock_send_email_confirm, company_user_client,
            fake_photo, company):
        data = {'photo': fake_photo}
        resp = api_requests.upload_company_photo(
            company_user_client,
            company.id,
            data)
        assert resp.status_code == http.HTTPStatus.OK
        assert 'photo' in resp.json()
        assert resp.json()['photo'] is not None

    def test_delete_company_photo_success(
            self, company_user_client, company_with_photo):
        data = {"photo": None}
        resp = api_requests.delete_company_photo(
            company_user_client,
            company_with_photo.id,
            data)
        assert resp.status_code == http.HTTPStatus.OK
        assert 'photo' in resp.json()
        assert not resp.json()['photo']

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
            'company_2_user_client',
            http.HTTPStatus.FORBIDDEN
        ),
    ))
    def test_update_not_own_company_photo_fails_or_not_company_user(
            self, request, client, mock_send_email_confirm,
            fake_photo, status, company):
        client = request.getfixturevalue(client)
        data = {'photo': fake_photo}
        resp = api_requests.upload_company_photo(
            client,
            company.id,
            data)
        assert resp.status_code == status

    def test_update_company_photo_fails_without_permissions(
            self, company_user_client, company_user_2_client,
            active_company_user, permissions_groups, company,
            invited_company_user_data):
        data = invited_company_user_data.copy()
        data['permissions_groups'] = [
            perm_group['id'] for perm_group in permissions_groups
            if perm_group['name'] != perm_constants.EDIT_COMPANY_PROFILE_GROUP
        ]
        resp = api_requests.edit_company_user(
            company_user_client,
            active_company_user['id'],
            data)
        assert resp.status_code == http.HTTPStatus.OK
        resp = api_requests.upload_company_photo(
            company_user_2_client,
            company.id,
            data)
        assert resp.status_code == http.HTTPStatus.FORBIDDEN


class TestBannedCompaniesInCompanyList:

    def test_banned_companies_not_in_public_company_list(
            self, anonym_client, company):
        resp = api_requests.get_companies(anonym_client)
        assert resp.json()['count'] == 1

        utils.ban_entity(company)
        resp = api_requests.get_companies(anonym_client)
        assert resp.json()['count'] == 0
