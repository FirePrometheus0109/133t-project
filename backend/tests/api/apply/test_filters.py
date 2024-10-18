import datetime
import http
from unittest import mock

import pytest
from django.conf import settings
from django.utils import timezone

from leet import enums
from tests import api_requests
from tests import validators
from ..job.conftest import (
    job_for_filters, skills, location, industry,
    skills_group1, skills_group2, skills_group3
)


class TestListAutoapplyJobFilters:
    # @pytest.mark.usefixtures(
    #     'job1', 'job2', 'job3', 'job4', 'job5', 'job6')
    def test_list_jobs_no_filters(
            self, job_seeker_client, all_published_jobs):
        resp = api_requests.get_new_autoapply_jobs_list(
            job_seeker_client)
        assert resp.json()['count'] == 8

    def test_filter_by_fav_companies(self, job_seeker_client, company_2, all_published_jobs):
        include_company_names = ['google', company_2.name, "Unknown company"]
        resp = api_requests.get_new_autoapply_jobs_list(
            job_seeker_client,
            query_params={'include_company_names': include_company_names})
        assert resp.json()['results'][0]['company']['name'] == company_2.name

    def test_filter_by_exclude_companies(self, job_seeker_client, company_2, all_published_jobs):
        exclude_company_names = ['google', company_2.name, "Unknown company"]
        resp = api_requests.get_new_autoapply_jobs_list(
            job_seeker_client,
            query_params={'exclude_company_names': exclude_company_names})
        assert resp.json()['count'] == 7


    @pytest.mark.parametrize(
        ('salary_min', 'salary_max', 'query_params', 'jobs_count'), (
            (
                100,
                200,
                {
                    'salary': 50
                },
                0
            ),
            (
                100,
                200,
                {
                    'salary': 100
                },
                1
            ),(
                100,
                200,
                {
                    'salary': 150
                },
                1
            ),
            (
                100,
                200,
                {
                    'salary': 200
                },
                1
            ),
            (
                100,
                200,
                {
                    'salary': 250
                },
                0
            ),

            (
                100,
                None,
                {
                    'salary': 100,
                },
                1
            ),
            (
                100,
                None,
                {
                    'salary': 50,
                },
                1
            ),(
                100,
                None,
                {
                    'salary': 150,
                },
                0
            ),
            (
                None,
                200,
                {
                    'salary': 150,
                },
                1
            ),
            (
                None,
                200,
                {
                    'salary': 200
                },
                1
            ),
            (
                None,
                200,
                {
                    'salary': 250
                },
                0
            ),
        )
    )
    def test_filter_by_salary(
            self, job_seeker_client, job_for_filters,
            query_params, jobs_count, salary_min, salary_max):
        job_for_filters.salary_min = salary_min
        job_for_filters.salary_max = salary_max
        job_for_filters.save()
        resp = api_requests.get_new_autoapply_jobs_list(
            job_seeker_client,
            query_params=query_params)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == jobs_count
