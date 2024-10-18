import datetime
import http
from unittest import mock

import pytest
from django.conf import settings
from django.utils import timezone

from leet import enums
from tests import api_requests
from tests import validators
from tests import utils


class TestFilters:

    @pytest.mark.parametrize(('query_params', 'count'), (
        (
            {},
            6
        ),
        (
            {
                'position_type': [enums.PositionTypesEnum.CONTRACT.name]
            },
            2
        ),
        (
            {
                'position_type': [enums.PositionTypesEnum.TEMPORARY.name]
            },
            2
        ),
        (
            {
                'position_type': [
                    enums.PositionTypesEnum.CONTRACT.name,
                    enums.PositionTypesEnum.FULL_TIME.name
                ]
            },
            3
        ),
        (
            {
                'position_type': [
                    enums.PositionTypesEnum.CONTRACT.name,
                ],
                'travel': enums.JSTravelOpportunitiesEnum.WILLING_TO_TRAVEL.name
            },
            1
        ),
        (
            {
                'experience': enums.ExperienceEnum.MORE_THAN_10.name,
            },
            4
        ),
        (
            {
                'clearance': [
                    enums.ClearanceTypesEnum.CONFIDENTIAL.name
                ]
            },
            1
        ),
        (
            {
                'clearance': [
                    enums.ClearanceTypesEnum.CONFIDENTIAL.name,
                    enums.ClearanceTypesEnum.PUBLIC_TRUST.name,
                ]
            },
            4
        ),
        (
            {
                'education': enums.EducationTypesEnum.HIGH_SCHOOL.name,
            },
            2
        ),
    ))
    def test_list_job_seekers_filters(
            self, company_user_client, job_seekers, query_params, count):
        resp = api_requests.get_job_seekers(
            company_user_client,
            query_params=query_params)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == count

    @pytest.mark.parametrize(('skill_fixture', 'count'), (
        (
            'document_management_software_skill',  # there are no job_seekers with this skill
            0
        ),
        (
            'spreadsheet_software_skill',
            4
        )
    ))
    def test_list_job_seekers_filter_by_skill(
            self, request, company_user_client,
            job_seekers, skill_fixture, count):
        skill = request.getfixturevalue(skill_fixture)
        query_params = {'skills': [skill.id]}
        resp = api_requests.get_job_seekers(
            company_user_client,
            query_params=query_params)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == count

    @pytest.mark.parametrize(('query_params', 'count'), (
        (
            {
                'profile_updated_within_days': enums.LastUpdatedWithingDays.FIVE_DAYS.value
            },
            1,
        ),
        (
            {
                'profile_updated_within_days': enums.LastUpdatedWithingDays.TEN_DAYS.value
            },
            1,
        ),
        (
            {
                'profile_updated_within_days': enums.LastUpdatedWithingDays.FIFTEEN_DAYS.value
            },
            2,
        )
    ))
    def test_list_job_seekers_filter_by_last_updated_date(
            self, company_user_client, job_seeker_client,
            job_seeker, job_seeker_2, query_params, count,
            project_management_software_skill):
        modified_at = timezone.now() + datetime.timedelta(days=11)
        with mock.patch.object(timezone, 'now', new=lambda: modified_at):
            data = {
                'user': {
                    'last_name': 'new last name'
                },
            }
            resp = api_requests.partial_update_job_seeker(
                job_seeker_client,
                job_seeker.id,
                data)
            assert resp.status_code == http.HTTPStatus.OK
        today = timezone.now() + datetime.timedelta(days=13)
        with mock.patch.object(timezone, 'now', new=lambda: today):
            resp = api_requests.get_job_seekers(
                company_user_client,
                query_params=query_params)
            assert resp.status_code == http.HTTPStatus.OK
            assert resp.json()['count'] == count

    @pytest.mark.parametrize(('query_params', 'count'), (
        (
            {'search': 'rob roberto mike'},
            3
        ),
        (
            {'search': 'roberto'},
            2,
        ),
        (
            {'search': 'noname'},
            2,
        ),
        (
            {'search': 'noname roberto'},
            3,
        ),
        (
            {'search': 'noname-robertomo'},
            0,
        ),
        (
            {'search': 'noname, roberto'},
            3,
        ),
        (
            {'search': 'noname , roberto'},
            3,
        ),
        (
            {'search': 'noname, roberto'},
            3,
        ),
        (
            {'search': 'roberto    asd'},
            2,
        ),
        (
            {'search': 'roberto abc mike'},
            3,
        ),
        (
            {'search': 'roberto abc mike study'},
            4,
        ),
        (
            {'search': ', noname; lolol, 10001; testetst trash'},
            5,
        ),
        (
            {'search': 'title; spreadsheet '},
            5
        ),
    ))
    @pytest.mark.skipif(
        'postgres' not in settings.DATABASES['default']['ENGINE'],
        reason='sqlite does not support postgres full text search')
    def test_job_seekers_by_full_text_search(
            self, job_seeker, job_experience, company_user_client,
            education, certification, job_seekers, query_params, count):
        resp = api_requests.get_job_seekers(
            company_user_client,
            query_params=query_params)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == count

    @pytest.mark.parametrize(('is_current', 'count'), ((True, 1), (False, 0)))
    @pytest.mark.skipif(
        'postgres' not in settings.DATABASES['default']['ENGINE'],
        reason='sqlite does not support postgres full text search')
    def test_get_job_seekers_full_text_search_job_title_only_in_current_jobs(
            self, job_seeker, job_seeker_client,
            company_user_client, job_experience_data,
            is_current, count):
        data = job_experience_data.copy()
        if not is_current:
            data['date_to'] = str(timezone.now())
            data['is_current'] = is_current
        resp = api_requests.add_job_experience(
            job_seeker_client,
            job_seeker.id,
            data)
        assert resp.status_code == http.HTTPStatus.CREATED

        query_params = {'search': resp.json()['job_title']}
        resp = api_requests.get_job_seekers(
            company_user_client,
            query_params=query_params)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == count

    @pytest.mark.skipif(
        'postgres' not in settings.DATABASES['default']['ENGINE'],
        reason='sqlite does not support postgres full text search')
    def test_search_job_seeker_by_location(
            self, city_new_york, zip_new_york, country_usa, city_ashville,
            zip_ashville, state_iowa, job_seeker, job_experience,
            company_user_client, education, certification, job_seekers):
        query_params = {
            'location': [
                zip_ashville.code,
                city_new_york.name,
                state_iowa.abbreviation
            ]
        }
        resp = api_requests.get_job_seekers(
            company_user_client,
            query_params=query_params)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == 7
        expected_job_seeker_ids_order = [
            job_seekers[0].id,
            job_seekers[1].id,
            job_seeker.id,
            job_seekers[5].id,
            job_seekers[2].id,
            job_seekers[3].id,
            job_seekers[4].id,
        ]
        actual_job_seeker_ids_order = [
            js['id'] for js in resp.json()['results']
        ]
        assert expected_job_seeker_ids_order == actual_job_seeker_ids_order

    @pytest.mark.skipif(
        'postgres' not in settings.DATABASES['default']['ENGINE'],
        reason='sqlite does not support postgres full text search')
    def test_searh_job_seeker_by_location_no_location(
            self, city_new_york, zip_new_york, country_usa, city_ashville,
            zip_ashville, state_iowa, job_seeker, job_experience,
            company_user_client, education, certification, job_seekers):
        query_params = {
            'location': [
                '11111',  # there are no job seekers with certain zip code
                state_iowa.abbreviation
            ]
        }
        resp = api_requests.get_job_seekers(
            company_user_client,
            query_params=query_params)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == 1

    @pytest.mark.parametrize(('client', 'count'), (
        ('company_user_client', 1), ('company_user_2_client', 0)
    ))
    def test_get_list_saved_job_seekers(
            self, request, client, count, saved_job_seeker):
        client = request.getfixturevalue(client)
        query_params = {
            'saved': True
        }
        resp = api_requests.get_job_seekers(client, query_params=query_params)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == count

    @pytest.mark.parametrize(('query_params',), (
        (
            {
                'saved': True
            },
        ),
        (
            {
                'saved': 1
            },
        ),
        (
            {
                'saved': 'true'
            },
        ),
        (
            {
                'saved': 'True'
            },
        ),
    ))
    def test_get_list_saved_job_seekers_valid_params(
            self, company_user_client, saved_job_seeker,
            query_params, job_seeker_2):
        resp = api_requests.get_job_seekers(
            company_user_client,
            query_params=query_params)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == 1
        assert resp.json()['results'][0]['saved_at']

    @pytest.mark.parametrize(('client', 'count'), (
        ('company_user_client', 2), ('company_2_user_client', 0)
    ))
    def test_get_list_puchased_job_seekers(
            self, request, client, count, purchased_job_seekers):
        client = request.getfixturevalue(client)
        query_params = {
            'purchased': True
        }
        resp = api_requests.get_job_seekers(client, query_params=query_params)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == count

    def test_get_list_purchased_job_seekers_ordering_by_modified(
            self, company_user_client,
            purchased_job_seekers, job_seeker_2):
        mockname = 'django.utils.timezone.now'
        with mock.patch(mockname, new=lambda: utils.date(2018, 11, 11)):
            job_seeker_2.salary_max = 10000
            job_seeker_2.save()
        query_params = {
            'purchased': True,
            'ordering': 'modified_at'
        }
        resp = api_requests.get_job_seekers(
            company_user_client,
            query_params=query_params)
        assert resp.status_code == http.HTTPStatus.OK
        validators.validate_ordering(
            resp.json()['results'],
            '-modified_at',
            'modified_at')

    @pytest.mark.skipif(
        'postgres' not in settings.DATABASES['default']['ENGINE'],
        reason='sqlite does not support postgres full text search')
    def test_default_ordering_is_by_rank(self, company_user_client, job_seekers):
        query_params = {'search': 'packman'}
        resp = api_requests.get_job_seekers(
            company_user_client,
            query_params=query_params)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == 2
        assert resp.json()['results'][0]['id'] == job_seekers[-1].id
        assert resp.json()['results'][1]['id'] == job_seekers[0].id
