import datetime
import http
from unittest import mock

import pytest
from django.conf import settings
from django.utils import timezone

from leet import enums
from tests import api_requests
from tests import validators


def validate_jobs_list_fts_ordering(titles, results):
    for exp_title, act_resp in zip(titles, results):
        assert exp_title == act_resp['title']


class TestListJobFilters:

    def test_list_jobs_no_filters(
            self, company_user_client, jobs):
        resp = api_requests.get_job_list(
            company_user_client)
        assert resp.json()['count'] == 4

    @pytest.mark.parametrize(('status',), (
        (
            enums.JobStatusEnum.ACTIVE.name,
        ),
        (
            enums.JobStatusEnum.DELAYED.name,
        )
    ))
    def test_list_jobs_filter_by_status(
            self, company_user_client, jobs, status):
        resp = api_requests.get_job_list(
            company_user_client,
            query_params={'status': status})
        assert resp.json()['count'] == 2
        for i in resp.json()['results']:
            i['status'] == status

    def test_list_jobs_filter_by_owner_there_are_no_jobs(
            self, company_user_client, jobs):
        resp = api_requests.get_job_list(
            company_user_client,
            query_params={'owner': [999999]})
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == 0

    def test_list_jobs_filter_by_owner(
            self, company_user_client, company_user, jobs):
        resp = api_requests.get_job_list(
            company_user_client,
            query_params={'owner': [company_user.id]})
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == 4

    def test_list_jobs_filter_by_owner_many_owners(
            self, company_user_client, company_user, jobs):
        resp = api_requests.get_job_list(
            company_user_client,
            query_params={'owner': [company_user.id, 99999]})
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == 4

    @pytest.mark.parametrize(('order_by', 'fields'), (
        (
            '-created_at',
            'created_at'
        ),
        (
            'status',
            'status'
        ),
        (
            'title',
            'title'
        ),
        (
            'owner__user__first_name',
            ('owner', 'name')
        ),
        (
            '-publish_date',
            'publish_date'
        )
    ))
    def test_list_jobs_ordering(
            self, company_user_client, company_user,
            jobs, order_by, fields):
        resp = api_requests.get_job_list(
            company_user_client,
            query_params={'ordering': order_by})
        assert resp.status_code == http.HTTPStatus.OK
        validators.validate_ordering(
            resp.json()['results'], order_by, fields)

    @pytest.mark.skipif(
        'postgres' not in settings.DATABASES['default']['ENGINE'],
        reason='sqlite does not support postgres full text search')
    def test_list_jobs_search(
            self, company_user_client, company_user, jobs):
        resp = api_requests.get_job_list(
            company_user_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == 4
        resp = api_requests.get_job_list(
            company_user_client,
            query_params={'search': 'title3'})
        assert resp.json()['count'] == 1
        assert resp.json()['results'][0]['title'] == 'title3'

    @pytest.mark.parametrize(('is_deleted',), (
            (
                True,
            ),
            (
                False,
            )
    ))
    def test_list_jobs_filter_is_deleted(
            self, is_deleted, company_user_client, job,
            company_deleted_job):
        resp = api_requests.get_job_list(
            company_user_client,
            query_params={'is_deleted': is_deleted})
        assert resp.json()['count'] == 1
        assert resp.json()['results'][0]['is_deleted'] is is_deleted

    def test_ordering_by_modified_at(
            self, company_user_client, job_base_data, job):
        mock_date = timezone.now() - datetime.timedelta(days=2)
        with mock.patch.object(timezone, 'now', new=lambda: mock_date):
            resp = api_requests.create_job(company_user_client, job_base_data)
            assert resp.status_code == http.HTTPStatus.CREATED
        mock_date = timezone.now() - datetime.timedelta(days=1)
        with mock.patch.object(timezone, 'now', new=lambda: mock_date):
            data = job_base_data.copy()
            data['title'] = 'new title'
            resp = api_requests.update_job(
                company_user_client,
                job['id'],
                data)
            assert resp.status_code == http.HTTPStatus.OK
        resp = api_requests.get_job_list(
            company_user_client,
            query_params={'ordering': '-modified_at'})
        assert resp.status_code == http.HTTPStatus.OK
        validators.validate_ordering(
            resp.json()['results'], '-modified_at', 'modified_at')


class TestListJobFiltersByJobSeeker:

    @pytest.mark.parametrize(('query_params', 'jobs_count'), (
        (
            {'experience': enums.ExperienceEnum.NO_EXPERIENCE.name},
            0
        ),
        (
            {'experience': enums.ExperienceEnum.FROM_1_TO_2.name},
            1
        ),
        (
            {
                'position_type': [
                    enums.PositionTypesEnum.CONTRACT.name,
                    enums.PositionTypesEnum.FULL_TIME.name
                ]
            },
            1
        ),
        (
            {
                'position_type': [
                    enums.PositionTypesEnum.TEMPORARY.name,
                    enums.PositionTypesEnum.FULL_TIME.name
                ]
            },
            0
        ),
        (
            {
                'clearance': [
                    enums.ClearanceTypesEnum.CONFIDENTIAL.name,
                    enums.ClearanceTypesEnum.PUBLIC_TRUST.name
                ]
            },
            1
        ),
        (
            {
                'clearance': [
                    enums.ClearanceTypesEnum.SECRET.name,
                    enums.ClearanceTypesEnum.PUBLIC_TRUST.name
                ]
            },
            0
        ),
        (
            {
                'clearance': [
                    enums.ClearanceTypesEnum.CONFIDENTIAL.name,
                ],
                'position_type': [
                    enums.PositionTypesEnum.CONTRACT.name,
                ]
            },
            1
        ),
        (
            {
                'clearance': [
                    enums.ClearanceTypesEnum.PUBLIC_TRUST.name,
                ],
                'position_type': [
                    enums.PositionTypesEnum.CONTRACT.name,
                ]
            },
            0
        ),
        (
            {
                'clearance': [
                    enums.ClearanceTypesEnum.CONFIDENTIAL.name,
                ],
                'position_type': [
                    enums.PositionTypesEnum.FULL_TIME.name,
                ]
            },
            0
        ),
    ))
    def test_job_list_filters(
            self, job_seeker_client, job_for_filters,
            query_params, jobs_count):
        resp = api_requests.get_job_list(
            job_seeker_client,
            query_params=query_params)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == jobs_count

    @pytest.mark.parametrize(('skills_group_fixture', 'jobs_count'), (
        (
            'skills_group1',
            1
        ),
        (
            'skills_group2',
            0
        )
    ))
    def test_job_list_skills_filters(
            self, request, job_seeker_client,
            job_for_filters, skills_group_fixture, jobs_count):
        skills = request.getfixturevalue(skills_group_fixture)
        query_params = {
            'skills': [s.id for s in skills]
        }
        resp = api_requests.get_job_list(
            job_seeker_client,
            query_params=query_params)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == jobs_count

    @pytest.mark.parametrize((
        'companies_fixture', 'jobs_count', 'is_excluded'), (
        (
            ['company'],
            1,
            False
        ),
        (
            ['company_2'],
            0,
            False
        ),
        (
            ['company', 'company_2'],
            1,
            False
        ),
        (
            ['company'],
            0,
            True
        ),
        (
            ['company_2'],
            1,
            True
        ),
        (
            ['company', 'company_2'],
            0,
            True
        )
    ))
    def test_job_list_companies_filters(
            self, request, job_seeker_client,
            job_for_filters, companies_fixture, jobs_count, is_excluded):
        companies = [request.getfixturevalue(c) for c in companies_fixture]
        if not is_excluded:
            query_params = {
                'company': [c.id for c in companies]
            }
        else:
            query_params = {
                'excl_company': [c.id for c in companies]
            }
        resp = api_requests.get_job_list(
            job_seeker_client,
            query_params=query_params)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == jobs_count

    def test_job_list_excluded_companies_more_relevance_than_included(
            self, job_seeker_client, company, job_for_filters):
        query_params = {
            'company': [company.id],
            'excl_company': [company.id]
        }
        resp = api_requests.get_job_list(
            job_seeker_client,
            query_params=query_params)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == 0

    @pytest.mark.parametrize(('query_params', 'jobs_count'), (
        #  the same values like in LastUpdatedWithingDays enum
        (
            {
                'posted_ago': enums.LastUpdatedWithingDays.FIVE_DAYS.value
            },
            0,
        ),
        (
            {
                'posted_ago': enums.LastUpdatedWithingDays.TEN_DAYS.value
            },
            0,
        ),
        (
            {
                'posted_ago': enums.LastUpdatedWithingDays.FIFTEEN_DAYS.value
            },
            1,
        )
    ))
    def test_list_job_seekers_filter_by_last_updated_date(
            self, job_seeker_client, job_for_filters, query_params, jobs_count):
        today = timezone.now() + datetime.timedelta(days=13)
        with mock.patch.object(timezone, 'now', new=lambda: today):
            resp = api_requests.get_job_list(
                job_seeker_client,
                query_params=query_params)
            assert resp.status_code == http.HTTPStatus.OK
            assert resp.json()['count'] == jobs_count

    @pytest.mark.parametrize(
        ('salary_min', 'salary_max', 'query_params', 'jobs_count'), (
            (
                150,
                200,
                {
                    'salary_min': 50,
                    'salary_max': 100
                },
                0
            ),
            (
                100,
                200,
                {
                    'salary_max': 50
                },
                0
            ),
            (
                100,
                None,
                {
                    'salary_min': 150,
                    'salary_max': 200
                },
                0
            ),
            (
                100,
                None,
                {
                    'salary_min': 150
                },
                0
            ),
            (
                100,
                200,
                {
                    'salary_min': 50,
                    'salary_max': 250
                },
                1
            ),
            (
                50,
                250,
                {
                    'salary_min': 100,
                    'salary_max': 200
                },
                1
            ),
            (
                100,
                200,
                {
                    'salary_min': 150,
                    'salary_max': 250
                },
                1
            ),
            (
                150,
                250,
                {
                    'salary_min': 100,
                    'salary_max': 200
                },
                1
            ),
            (
                100,
                None,
                {
                    'salary_min': 50,
                },
                1
            ),
            (
                100,
                None,
                {
                    'salary_min': 100,
                },
                1
            ),
            (
                100,
                None,
                {
                    'salary_max': 150,
                },
                1
            ),
            (
                None,
                200,
                {
                    'salary_min': 150,
                },
                1
            ),
            (
                None,
                200,
                {
                    'salary_min': 100,
                    'salary_max': 150
                },
                1
            ),
            (
                None,
                200,
                {
                    'salary_max': 150
                },
                1
            ),
            (
                None,
                150,
                {
                    'salary_max': 200
                },
                1
            ),
            (
                None,
                200,
                {
                    'salary_max': 200
                },
                1
            ),
            (
                100,
                200,
                {
                    'salary_min': 150
                },
                1
            ),
            (
                150,
                None,
                {
                    'salary_min': 100
                },
                1
            ),
        )
    )
    def test_salary_filter_for_job_list(
            self, job_seeker_client, job_for_filters,
            query_params, jobs_count, salary_min, salary_max):
        job_for_filters.salary_min = salary_min
        job_for_filters.salary_max = salary_max
        job_for_filters.save()
        resp = api_requests.get_job_list(
            job_seeker_client,
            query_params=query_params)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == jobs_count

    @pytest.mark.parametrize(('salary_negotiable', 'jobs_count'), (
        (True, 0), (False, 1)
    ))
    def test_salary_filter_dont_include_jobs_with_salary_niegotiable(
            self, job_seeker_client,
            job_for_filters, salary_negotiable, jobs_count):
        job_for_filters.salary_negotiable = salary_negotiable
        job_for_filters.save()
        query_params = {
            'salary_min': job_for_filters.salary_min,
            'salary_max': job_for_filters.salary_max
        }
        resp = api_requests.get_job_list(
            job_seeker_client,
            query_params=query_params)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == jobs_count

    @pytest.mark.parametrize(('city_fixture', 'jobs_count'), (
        (
            'city_ashville',
            0
        ),
        (
            'city_new_york',
            1
        )
    ))
    @pytest.mark.skipif(
        'postgres' not in settings.DATABASES['default']['ENGINE'],
        reason='sqlite does not support postgres full text search')
    def test_job_list_filter_by_locations(
            self, request, job_seeker_client,
            job_for_filters, city_fixture, jobs_count):
        city = request.getfixturevalue(city_fixture)
        query_params = {
            'location': [city.name]
        }
        resp = api_requests.get_job_list(
            job_seeker_client,
            query_params=query_params)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == jobs_count

    @pytest.mark.parametrize(
        (
            'query_params', 'jobs_count', 'exp_order_titles'
        ),
        (
            (
                {
                    'search': 'cook;construction',
                    'ordering': 'rank'
                },
                2,
                ['junior developer', 'project manager']
            ),
            (
                {
                    'search': 'cooks and other things, bad errors;; ',
                    'ordering': 'rank'
                },
                1,
                ['junior developer']
            ),
            (
                {
                    'search': 'cooks aboom',
                    'position_type': [enums.PositionTypesEnum.PART_TIME.name]
                },
                1,
                ['junior developer']
            ),
            (
                {
                    'search': 'senior',
                    'position_type': [enums.PositionTypesEnum.PART_TIME.name]
                },
                0,
                []
            ),
            (
                {
                    'search': 'senior developer',
                    'ordering': 'rank'
                },
                3,
                ['senior developer', 'junior developer', 'middle developer']
            ),
            (
                {
                    'search': 'senior developer',
                    'location': ['New York'],
                    'ordering': 'rank'
                },
                2,
                ['senior developer', 'junior developer']
            ),
            (
                {
                    'search': 'senior devel, spreadsheet, , ',
                    'location': ['New York'],
                    'ordering': 'rank'
                },
                1,
                ['senior developer']
            ),
            (
                {
                    'search': 'senior devel, spreadsheet, , ',
                    'location': ['New York', 'Ashville'],
                    'ordering': 'rank'
                },
                1,
                ['senior developer']
            ),
            # 'management' in group1, group3, 'document' in group3, software in all groups
            (
                {
                    'search': 'Document management software',
                    'ordering': 'rank'
                },
                4,
                [
                    'project manager',
                    'senior developer',
                    'junior developer',
                    'middle developer'
                ]
            ),
            (
                {
                    'search': 'first company',
                    'ordering': 'rank'
                },
                4,
                [
                    'project manager',
                    'senior developer',
                    'junior developer',
                    'middle developer',
                ]
            ),
            (
                {
                    'search': 'second',
                    'ordering': 'rank'
                },
                0,
                []
            ),
            # only 'project manager' job has keyword 'spreadsheet'
            (
                {
                    'search': 'spreadsheet',
                    'ordering': 'rank'
                },
                1,
                ['project manager']
            ),
        )
    )
    @pytest.mark.skipif(
        'postgres' not in settings.DATABASES['default']['ENGINE'],
        reason='sqlite does not support postgres full text search')
    def test_full_text_search_job_list(
            self, job_seeker_client, jobs_list,
            query_params, jobs_count, exp_order_titles):
        resp = api_requests.get_job_list(
            job_seeker_client,
            query_params=query_params)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == jobs_count
        validate_jobs_list_fts_ordering(
            exp_order_titles,
            resp.json()['results'])


class TestSavedSearchesAPI:
    @pytest.mark.parametrize(('query_params', 'exp_criteria_json'), (
            (
                    {
                        'search': 'Developer',
                        'location': 'New York',
                        'clearance': [
                            enums.ClearanceTypesEnum.PUBLIC_TRUST.name,
                            enums.ClearanceTypesEnum.CONFIDENTIAL.name
                        ],
                        'ordering': 'rank',
                        'position_type': [
                            enums.PositionTypesEnum.PART_TIME.name
                        ]
                    },
                    '{"clearance": ["2", "4"], '
                    '"location": ["New York"], "ordering": ["rank"], '
                    '"position_type": ["PART_TIME"], "search": ["Developer"]}'
            ),
            (
                    {
                        'clearance': [
                            enums.ClearanceTypesEnum.PUBLIC_TRUST.name,
                            enums.ClearanceTypesEnum.PUBLIC_TRUST.name,
                        ],
                        'limit': 1,
                        'offset': 1
                    },
                    '{"clearance": ["4"]}'
            ),
            (
                    {},
                    '{}'
            ),
            (
                    {'ordering': 'rank'}, '{"ordering": ["rank"]}'
            )
    ))
    @pytest.mark.skipif(
        'postgres' not in settings.DATABASES['default']['ENGINE'],
        reason='sqlite does not support postgres full text search')
    def test_save_search(
            self, query_params, exp_criteria_json,
            job_seeker_client, job_seeker):
        assert not job_seeker.searches.count()
        resp = api_requests.get_job_list(job_seeker_client, query_params)
        assert resp.status_code == http.HTTPStatus.OK
        assert job_seeker.searches.count() == 1
        search = job_seeker.searches.first()
        assert search.criteria == exp_criteria_json
        assert search.count == 1
        assert not search.is_saved

    @pytest.mark.skipif(
        'postgres' not in settings.DATABASES['default']['ENGINE'],
        reason='sqlite does not support postgres full text search')
    def test_count_increase_if_equal_search(
            self, job_seeker_client, job_seeker):
        assert not job_seeker.searches.count()
        query_params = {
            'search': 'Developer',
            'clearance': [
                enums.ClearanceTypesEnum.PUBLIC_TRUST.name,
                enums.ClearanceTypesEnum.CONFIDENTIAL.name
            ],
            'ordering': 'rank',
            'position_type': [
                enums.PositionTypesEnum.PART_TIME.name
            ]
        }
        resp = api_requests.get_job_list(job_seeker_client, query_params)
        assert resp.status_code == http.HTTPStatus.OK
        assert job_seeker.searches.count() == 1
        search = job_seeker.searches.first()
        assert search.count == 1
        query_params = {
            'search': 'Developer',
            'clearance': [
                enums.ClearanceTypesEnum.CONFIDENTIAL.name,
                enums.ClearanceTypesEnum.PUBLIC_TRUST.name
            ],
            'position_type': [
                enums.PositionTypesEnum.PART_TIME.name
            ],
            'limit': 10,
            'offset': 10,
            'ordering': 'rank'
        }
        resp = api_requests.get_job_list(job_seeker_client, query_params)
        assert resp.status_code == http.HTTPStatus.OK
        assert job_seeker.searches.count() == 1
        search = job_seeker.searches.first()
        assert search.count == 2
