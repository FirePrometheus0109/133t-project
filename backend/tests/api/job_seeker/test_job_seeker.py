import http
import random

import pytest
from django.conf import settings

from job import constants as job_constants
from job_seeker import constants
from leet import constants as base_constants
from leet import enums
from tests import api_requests
from tests import constants as test_constants
from tests import validators
from tests.api.job_seeker import expected


class TestJobSeeker:

    def test_job_seeker_update_photo(
            self, job_seeker_client, fake_photo,
            job_seeker):
        data = {"photo": fake_photo}
        resp = api_requests.upload_photo(
            job_seeker_client,
            job_seeker.id,
            data)
        assert resp.status_code == http.HTTPStatus.OK
        assert 'photo' in resp.json()
        assert resp.json()['photo'] is not None

    def test_job_seeker_delete_photo(
            self, job_seeker_client, fake_photo,
            job_seeker_with_photo):
        data = {"photo": None}
        resp = api_requests.delete_photo(
            job_seeker_client,
            job_seeker_with_photo.id,
            data)
        assert resp.status_code == http.HTTPStatus.OK
        assert 'photo' in resp.json()
        assert not resp.json()['photo']

    @pytest.mark.parametrize(('field', 'value'), (
        ('position_type', random.choice(list(enums.PositionTypesEnum)).name),
        ('education', random.choice(list(enums.EducationTypesEnum)).name),
        ('clearance', random.choice(list(enums.ClearanceTypesEnum)).name),
        ('experience', random.choice(list(enums.ExperienceEnum)).name),
        ('benefits', random.choice(list(enums.BenefitsEnum)).name),
        ('travel', random.choice(list(enums.JSTravelOpportunitiesEnum)).name),
        ('salary_public', False),
        ('salary_min', 200),
        ('salary_max', 1000),
        ('about', 'Some text'),
        ('phone', '1-541-754-3010'),
    ))
    def test_patch_flat_fields_success(
            self, job_seeker_client, job_seeker, field, value):
        data = {field: value}
        resp = api_requests.partial_update_job_seeker(
            job_seeker_client,
            job_seeker.id,
            data)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()[field] == value

    def test_update_job_seeker_email_success(
            self, job_seeker_client, anonym_client, job_seeker):
        new_email = 'newuseremail@mail.com'
        resp = api_requests.partial_update_job_seeker(
            job_seeker_client,
            job_seeker.id,
            {'user': {'email': new_email}})
        assert resp.status_code == http.HTTPStatus.OK
        login_data = {
            'email': new_email,
            'password': test_constants.DEFAULT_PASSWORD
        }
        resp = api_requests.login(anonym_client, login_data)
        assert resp.status_code == http.HTTPStatus.OK

    def test_salary_is_hidden_for_other_users_if_not_salary_public(
            self, job_seeker_client, company_user_client,
            job_seeker):
        data = {
            'salary_public': False
        }
        resp = api_requests.partial_update_job_seeker(
            job_seeker_client,
            job_seeker.id,
            data)
        assert resp.status_code == http.HTTPStatus.OK
        assert not resp.json()['salary_public']
        assert 'salary_max' in resp.json()
        assert 'salary_min' in resp.json()

        resp = api_requests.get_job_seeker_details(
            company_user_client,
            job_seeker.id)
        assert resp.status_code == http.HTTPStatus.OK
        assert 'salary_max' not in resp.json()
        assert 'salary_min' not in resp.json()

    @pytest.mark.parametrize(('current_is_public', ), (
            (True,),
            (False,)
    ))
    def test_change_is_public_profile_success(
            self, current_is_public, job_seeker, job_seeker_client):
        job_seeker.is_public = current_is_public
        job_seeker.save()
        resp = api_requests.partial_update_job_seeker(
            job_seeker_client,
            job_seeker.id,
            {'is_public': not current_is_public})
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['is_public'] is not current_is_public

    def test_share_profile_success(
            self, job_seeker, job_seeker_client):
        resp = api_requests.partial_update_job_seeker(
            job_seeker_client,
            job_seeker.id,
            {'is_shared': True})
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['is_shared']
        assert resp.json()['guid']

    def test_unshare_profile_success(
            self, shared_job_seeker, job_seeker_client):
        resp = api_requests.partial_update_job_seeker(
            job_seeker_client,
            shared_job_seeker.id,
            {'is_shared': False})
        assert resp.status_code == http.HTTPStatus.OK
        assert not resp.json()['is_shared']
        assert not resp.json().get('guid')

    @pytest.mark.parametrize(('attr',), (
        ('position_type',),
        ('education',),
    ))
    def test_publish_profile_gets_hidden_after_removing_of_profile_attrs(
            self, attr, job_seeker, job_seeker_client):
        resp = api_requests.partial_update_job_seeker(
            job_seeker_client,
            job_seeker.id,
            {attr: ''})
        assert resp.status_code == http.HTTPStatus.OK
        assert not resp.json()['is_public']

    def test_publish_profile_gets_hidden_after_updating_of_skills(
            self, job_seeker, job_seeker_client,
            electronic_mail_software_skill,
            document_management_software_skill):
        resp = api_requests.partial_update_job_seeker(
            job_seeker_client,
            job_seeker.id,
            {'skills': [electronic_mail_software_skill.id,
                        document_management_software_skill.id]})
        assert resp.status_code == http.HTTPStatus.OK
        assert not resp.json()['is_public']

    def test_job_seeker_completion_one_hundred_percents_if_all_completed(
            self, job_seeker_client, education, job_experience, job_seeker):
        resp = api_requests.get_job_seeker_details(
            job_seeker_client,
            job_seeker.id)
        assert resp.status_code == http.HTTPStatus.OK
        profile_completion = resp.json()['profile_completion']
        assert profile_completion['total_complete'] == 100
        assert not profile_completion['need_complete']

    @pytest.mark.parametrize(
        ('education_fixtures', 'percents', 'len_need_complete'), (
            (
                ('education',),
                100,
                0,
            ),
            (
                ('certification',),
                100,
                0,
            ),
            (
                ('education', 'certification'),
                100,
                0,
            ),
            (
                (),
                90,
                1
            )
        ))
    def test_job_seeker_completion_educations_section(
            self, request, job_seeker_client,
            job_experience, job_seeker,
            education_fixtures, percents, len_need_complete):
        for f in education_fixtures:
            request.getfixturevalue(f)
        resp = api_requests.get_job_seeker_details(
            job_seeker_client,
            job_seeker.id)
        assert resp.status_code == http.HTTPStatus.OK
        profile_completion = resp.json()['profile_completion']
        assert profile_completion['total_complete'] == percents
        assert len(profile_completion['need_complete']) == len_need_complete

    @pytest.mark.parametrize(('data', 'exp_field_name'), (
        (
            {
                'user': {
                    'first_name': ''
                },
            },
            'First name'
        ),
        (
            {
                'user': {
                    'last_name': ''
                },
            },
            'Last name'
        ),
        (
            {
                'user': {
                    'first_name': '',
                    'last_name': ''
                },
            },
            'First name, Last name'
        ),
        (
            {
                'address': {
                    'city': None,
                }
            },
            'City',
        ),
        (
            {
                'address': {
                    'zip': None,
                },
            },
            'Zip',
        ),
        (
            {
                'address': {
                    'country': None,
                },
            },
            'Country',
        ),
        (
            {
                'address': {
                    'city': None,
                    'zip': None,
                },
            },
            'City, Zip',
        ),
        (
            {
                'address': {
                    'city': None,
                    'country': None,
                },
            },
            'Country, City',
        ),
        (
            {
                'address': {
                    'zip': None,
                    'country': None,
                },
            },
            'Country, Zip',
        ),
        (
            {
                'address': {
                    'zip': None,
                    'country': None,
                    'city': None
                },
            },
            'Country, City, Zip',
        ),
    ))
    def test_job_seeker_profile_completion_no_complex_field(
            self, job_seeker, data, exp_field_name,
            job_seeker_client, job_experience, education):
        resp = api_requests.partial_update_job_seeker(
            job_seeker_client,
            job_seeker.id,
            data)
        assert resp.status_code == http.HTTPStatus.OK
        profile_completion = resp.json()['profile_completion']
        assert profile_completion['total_complete'] == 90
        assert len(profile_completion['need_complete']) == 1
        assert (profile_completion['need_complete'][0]['field'] ==
                exp_field_name)

    def test_get_list_job_seekers_only_public_profiles(
            self, company_user_client, job_seeker):
        job_seeker.is_public = False
        job_seeker.save()
        resp = api_requests.get_job_seekers(company_user_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == 0

    def test_job_seeker_can_update_email(
            self, job_seeker_client, job_seeker):
        data = {
            'user': {
                'email': 'newuniqueemail@email.com'
            }
        }
        resp = api_requests.partial_update_job_seeker(
            job_seeker_client,
            job_seeker.id,
            data)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['user']['email'] == data['user']['email']

    def test_list_job_seekers_saved_js_has_saved_at_date(
            self, company_user_client, saved_job_seeker):
        resp = api_requests.get_job_seekers(company_user_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == 1
        assert resp.json()['results'][0]['saved_at']

    def test_add_industries_to_profile(
            self, job_seeker_client, job_seeker, industries):
        industries = industries['results'][:constants.MAX_COUNT_OF_INDUSTRIES]
        data = {'industries': [i['id'] for i in industries]}
        resp = api_requests.partial_update_job_seeker(
            job_seeker_client,
            job_seeker.id,
            data
        )
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['industries'] == industries

    def test_get_job_seekers_details(self, job_seeker_client, job_seeker):
        resp = api_requests.get_job_seeker_details(
            job_seeker_client,
            job_seeker.id
        )
        assert resp.status_code == http.HTTPStatus.OK
        assert (resp.json() ==
                expected.EXPECTED_JS_PROFILE_DETAILS_FOR_OWNER)

    @pytest.mark.parametrize(('field',), (
        ('industries',), ('skills',)
    ))
    def test_delete_many_to_many_fields(
            self, job_seeker_client, job_seeker, field):
        data = {field: []}
        resp = api_requests.partial_update_job_seeker(
            job_seeker_client,
            job_seeker.id,
            data
        )
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()[field] == data[field]


class TestJobSeekerValidate:

    def test_patch_salary_max_fail_if_it_less_than_salary_min(
            self, job_seeker_client, job_seeker, job_seeker_info):
        salary_max = job_seeker_info['salary_min'] - 1
        data = {
            'salary_max': salary_max,
            'salary_min': job_seeker_info['salary_min']
        }
        resp = api_requests.partial_update_job_seeker(
            job_seeker_client,
            job_seeker.id,
            data)
        emsg = constants.MIN_SALARY_SHOULD_NOT_BE_GREATER_THAN_MAX
        validators.validate_error_message(resp, emsg)

    @pytest.mark.parametrize(('attr', 'value',), (
            ('first_name', ''),
            ('last_name', ''),
            ('email', ''),
    ))
    def test_publish_profile_fails_if_user_attrs_missing(
            self, attr, value, job_seeker, job_seeker_client):
        job_seeker.is_public = False
        job_seeker.save()
        setattr(job_seeker.user, attr, value)
        job_seeker.user.save()
        resp = api_requests.partial_update_job_seeker(
            job_seeker_client,
            job_seeker.id,
            {'is_public': True})
        emsg = constants.PROFILE_CANT_BE_PUBLIC_ERROR
        validators.validate_error_message(resp, emsg)

    @pytest.mark.parametrize(('attr', 'value',), (
            ('address', None),
            ('position_type', ''),
            ('education', ''),
    ))
    def test_publish_profile_fails_if_profile_attrs_missing(
            self, attr, value, job_seeker, job_seeker_client):
        job_seeker.is_public = False
        setattr(job_seeker, attr, value)
        job_seeker.save()
        resp = api_requests.partial_update_job_seeker(
            job_seeker_client,
            job_seeker.id,
            {'is_public': True})
        emsg = constants.PROFILE_CANT_BE_PUBLIC_ERROR
        validators.validate_error_message(resp, emsg)

    def test_publish_profile_fails_if_skills_missing(
            self, job_seeker, job_seeker_client,
            electronic_mail_software_skill,
            document_management_software_skill):
        job_seeker.is_public = False
        job_seeker.save()
        job_seeker.skills.clear()
        job_seeker.skills.add(
            electronic_mail_software_skill,
            document_management_software_skill)
        resp = api_requests.partial_update_job_seeker(
            job_seeker_client,
            job_seeker.id,
            {'is_public': True})
        emsg = constants.PROFILE_CANT_BE_PUBLIC_ERROR
        validators.validate_error_message(resp, emsg)

    @pytest.mark.parametrize(('field',), (
        ('salary_max',), ('salary_min',)
    ))
    def test_create_salary_more_than_max_salary(
            self, company_user_client, job_base_data, field):
        job_base_data[field] = settings.MAX_SALARY + 1
        resp = api_requests.create_job(company_user_client, job_base_data)
        emsg = job_constants.MAX_SALARY_VALUE_ERROR
        validators.validate_error_message(resp, emsg, field)

    def test_job_seeker_update_email_email_already_exists(
            self, job_seeker, job_seeker_2, job_seeker_client):
        data = {
            'user': {
                'email': job_seeker_2.user.email
            }
        }
        resp = api_requests.partial_update_job_seeker(
            job_seeker_client,
            job_seeker.id,
            data)
        assert resp.status_code == http.HTTPStatus.BAD_REQUEST
        assert (resp.json()['field_errors']['user']['email'][0] ==
                base_constants.USER_WITH_CERTAIN_EMAIL_EXISTS)

    def test_job_seeker_can_save_about_field_max_length(
            self, job_seeker_client, job_seeker):
        data = {'about': ''.join(['a' for _ in range(2001)])}
        resp = api_requests.partial_update_job_seeker(
            job_seeker_client,
            job_seeker.id,
            data)
        assert resp.status_code == http.HTTPStatus.BAD_REQUEST
        assert resp.json()['field_errors']['about']

    def test_job_seeker_update_phone_validation_fail(
            self, job_seeker, job_seeker_client):
        data = {'phone': '1-243-invalid-phone'}
        resp = api_requests.partial_update_job_seeker(
            job_seeker_client,
            job_seeker.id,
            data)
        emsg = constants.INVALID_PHONE_NUMBER_ERROR
        validators.validate_error_message(resp, emsg, 'phone')

    def test_update_job_seeker_profile_max_count_of_industries(
            self, job_seeker_client, job_seeker, industries):
        industries = (industries['results']
                      [:constants.MAX_COUNT_OF_INDUSTRIES + 1])
        data = {
            'industries': [i['id'] for i in industries]
        }
        resp = api_requests.partial_update_job_seeker(
            job_seeker_client,
            job_seeker.id,
            data)
        emsg = constants.MAXIMUM_OF_INDUSTRIES_ERROR
        validators.validate_error_message(resp, emsg, 'industries')


class TestJobSeekerApiPermissions:

    @pytest.mark.parametrize(('client', 'status'), (
        (
            'anonym_client',
            http.HTTPStatus.UNAUTHORIZED,
        ),
        (
            'job_seeker_client',
            http.HTTPStatus.FORBIDDEN,
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
    def test_get_list_job_seekers(self, request, client, status, job_seeker):
        client = request.getfixturevalue(client)
        resp = api_requests.get_job_seekers(client)
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
    def test_get_job_seeker_details(
            self, request, client, status, job_seeker):
        client = request.getfixturevalue(client)
        resp = api_requests.get_job_seeker_details(client, job_seeker.id)
        assert resp.status_code == status

    @pytest.mark.parametrize(('client', 'status'), (
        (
            'anonym_client',
            http.HTTPStatus.UNAUTHORIZED,
        ),
        (
            'job_seeker_client',
            http.HTTPStatus.FORBIDDEN,
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
    def test_delete_profile(
            self, request, client, status, job_seeker):
        client = request.getfixturevalue(client)
        resp = api_requests.delete_job_seeker_profile(client, job_seeker.id)
        assert resp.status_code == status

    def test_patch_not_own_photo_fails(
            self, mock_send_email_confirm, fake_photo,
            job_seeker_2_client, job_seeker):
        data = {'photo': fake_photo}
        resp = api_requests.upload_photo(
            job_seeker_2_client,
            job_seeker.id,
            data)
        assert resp.status_code == http.HTTPStatus.FORBIDDEN

    def test_company_user_get_job_seeker_list_success(
            self, company_user_client):
        resp = api_requests.get_job_seekers(
            company_user_client)
        assert resp.status_code == http.HTTPStatus.OK

    def test_company_user_get_public_job_seeker_success(
            self, company_user_client, job_seeker):
        resp = api_requests.get_job_seeker_details(
            company_user_client,
            job_seeker.id)
        assert resp.status_code == http.HTTPStatus.OK

    def test_company_user_get_hidden_profile_fails(
            self, company_user_client, job_seeker_hidden):
        resp = api_requests.get_job_seeker_details(
            company_user_client,
            job_seeker_hidden.id)
        emsg = constants.PROFILE_IS_HIDDEN_ERROR
        validators.validate_error_message(
            resp, emsg, error_code=http.HTTPStatus.FORBIDDEN)

    def test_company_user_get_hidden_profile_success_if_user_was_applied(
            self, company_user_client, apply, job_seeker_hidden):
        resp = api_requests.get_job_seeker_details(
            company_user_client,
            job_seeker_hidden.id)
        assert resp.status_code == http.HTTPStatus.OK

    @pytest.mark.parametrize(('api_request',), (
        (
            api_requests.update_job_seeker,
        ),
        (
            api_requests.partial_update_job_seeker,
        ),
    ))
    def test_unauthenticated_user_cant_update_profile(
            self, anonym_client, job_seeker, api_request):
        resp = api_request(anonym_client, job_seeker.id, {})
        assert resp.status_code == http.HTTPStatus.UNAUTHORIZED
