import copy
import datetime
import http
from unittest import mock

import pytest
from django.utils import timezone

from job import services
from leet import enums
from tests import api_requests
from tests import utils
from tests.api.job import constants


def create_job_for_find_job_page(
        job_base_data, job_data, skills, location,
        industry, company_user):
    data = copy.deepcopy(job_base_data)
    data.update(job_data)
    data_skills = copy.deepcopy(skills)
    data['required_skills'] = data_skills.pop(data['required_skills'], [])
    data['optional_skills'] = data_skills.pop(data['optional_skills'], [])
    data['location'] = location[job_data['location']]
    data['industry'] = industry[job_data['industry']]
    data['owner'] = company_user
    data['company'] = company_user.company
    job = services.create_job(data)
    return job


@pytest.fixture
def jobs(company_user_client, job_base_data):
    def create_jp(date, status, title):
        data = job_base_data.copy()
        data['status'] = status
        data['title'] += str(title)
        if status == enums.JobStatusEnum.DELAYED.name:
            data['publish_date'] = str(date + datetime.timedelta(days=1))
        mockname = 'django.utils.timezone.now'
        with mock.patch(mockname, new=lambda: date):
            resp = api_requests.create_job(
                company_user_client, data)
            assert resp.status_code == http.HTTPStatus.CREATED
            jobs.append(resp.json())

    jobs = []

    create_jp(utils.date(2018, 10, 1), enums.JobStatusEnum.ACTIVE.name, 3)
    create_jp(utils.date(2018, 10, 2), enums.JobStatusEnum.ACTIVE.name, 4)
    create_jp(utils.date(2018, 10, 1), enums.JobStatusEnum.DELAYED.name, 1)
    create_jp(utils.date(2018, 10, 2), enums.JobStatusEnum.DELAYED.name, 2)
    return jobs


@pytest.fixture
def job_delayed(company_user_client, job_base_data):
    """Company's Job with schedule"""
    data = job_base_data.copy()
    data['status'] = enums.JobStatusEnum.DELAYED.name
    data['publish_date'] = str(timezone.now() + datetime.timedelta(days=1))
    resp = api_requests.create_job(company_user_client, data)
    assert resp.status_code == http.HTTPStatus.CREATED
    return resp.json()


@pytest.fixture
def jobs_with_closing_dates(
        company_user_client, company_2_user_client, job_base_data):

    def create_job(client, title, data):
        data['title'] = title
        data['closing_date'] = str(timezone.now() + datetime.timedelta(days=4))
        resp = api_requests.create_job(client, data)
        assert resp.status_code == http.HTTPStatus.CREATED
        jobs.append(resp.json)

    jobs = []

    create_job(company_user_client, 'company_first_job', job_base_data)
    create_job(company_user_client, 'company_second_job', job_base_data)
    create_job(
        company_2_user_client, 'second_company_first_job', job_base_data)
    return jobs


@pytest.fixture
def skills_group1(
        office_suite_software_skill,
        project_management_software_skill):
    return [
        office_suite_software_skill,
        project_management_software_skill
    ]


@pytest.fixture
def skills_group2(
        spreadsheet_software_skill,
        electronic_mail_software_skill):
    return [
        spreadsheet_software_skill,
        electronic_mail_software_skill
    ]


@pytest.fixture
def skills_group3(
        document_management_software_skill,
        operating_system_software_skill):
    return [
        document_management_software_skill,
        operating_system_software_skill
    ]


@pytest.fixture
def skills(skills_group1, skills_group2, skills_group3):
    return {
        'group1': skills_group1,
        'group2': skills_group2,
        'group3': skills_group3,
    }


@pytest.fixture
def location(
        country_usa, city_new_york, city_ashville, city_packwood,
        zip_new_york, zip_ashville, zip_packwood):
    return {
        'new_york': {
            'city': city_new_york,
            'country': country_usa,
            'zip': zip_new_york
        },
        'ashville': {
            'city': city_ashville,
            'country': country_usa,
            'zip': zip_ashville
        },
        'packwood': {
            'city': city_packwood,
            'country': country_usa,
            'zip': zip_packwood
        },
    }


@pytest.fixture
def industry(industry_manufacturing, industry_construction):
    return {
        'manufacturing': industry_manufacturing,
        'construction': industry_construction
    }


@pytest.fixture
def job_for_filters(
        trial_subscription, company_user, company_2_user, job_base_data,
        skills, location, industry):
    job_data = constants.JOBS_DATA_FOR_TESTING_FILTERS_BY_JOB_SEEKER[0]
    job = create_job_for_find_job_page(
        job_base_data, job_data, skills, location,
        industry, company_user)
    return job


@pytest.fixture
def jobs_list(
        trial_subscription, company_user, company_2_user, job_base_data,
        skills, location, industry):
    jobs = []
    for job_data in constants.JOBS_DATA_FOR_TESTING_FILTERS_BY_JOB_SEEKER:
        job = create_job_for_find_job_page(
            job_base_data, job_data, skills, location,
            industry, company_user)
        jobs.append(job)

    return jobs
