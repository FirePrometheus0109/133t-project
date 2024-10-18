import http

import pytest

from tests import api_requests
from tests import factories
from tests.api.job_seeker import constants


@pytest.fixture
def education(job_seeker_client, job_seeker, education_data):
    resp = api_requests.add_education(
        job_seeker_client,
        job_seeker.id,
        education_data)
    assert resp.status_code == http.HTTPStatus.CREATED
    return resp.json()


@pytest.fixture
def certification(job_seeker_client, job_seeker, certification_data):
    resp = api_requests.add_certification(
        job_seeker_client,
        job_seeker.id,
        certification_data)
    assert resp.status_code == http.HTTPStatus.CREATED
    return resp.json()


@pytest.fixture
def cover_letters(job_seeker_client, job_seeker, cover_letter_data):

    def create_cover_letter(data):
        req_data = cover_letter_data.copy()
        req_data.update(data)
        resp = api_requests.create_cover_letter(
            job_seeker_client,
            job_seeker.id,
            req_data)
        assert resp.status_code == http.HTTPStatus.CREATED
        cover_letters.append(resp.json())

    cover_letters = []

    create_cover_letter({'title': 'title1'})
    create_cover_letter({'title': 'title2'})
    create_cover_letter({'title': 'title3'})
    create_cover_letter({'title': 'title4'})
    create_cover_letter({'title': 'title5'})
    return cover_letters


@pytest.fixture
def add_saved_job_data(job):
    return {
        'add': True,
        'job': job['id']
    }


@pytest.fixture
def remove_saved_job_data(job):
    return {
        'remove': True,
        'job': job['id']
    }


@pytest.fixture
def saved_job(
        job_seeker_client, job_seeker, add_saved_job_data):
    resp = api_requests.add_remove_to_saved(
        job_seeker_client,
        job_seeker.id,
        add_saved_job_data
    )
    assert resp.status_code == http.HTTPStatus.OK


@pytest.fixture
def job_seekers(
        job_seeker_info, job_seeker_base_data,
        office_suite_software_skill, project_management_software_skill,
        spreadsheet_software_skill, city_new_york,
        zip_new_york, country_usa, city_ashville, zip_ashville, city_packwood,
        zip_packwood):

    def create_job_seeker(user_data, js_data, address_data, skills):
        user = factories.create_base_user(**user_data)
        address = factories.create_address(**address_data)
        job_seeker = factories.create_job_seeker(
            user=user,
            address=address,
            is_public=True,
            skills=skills,
            **js_data)
        job_seeker.save()
        result.append(job_seeker)

    result = []
    skills = [
        office_suite_software_skill,
        project_management_software_skill,
    ]
    for i, item in enumerate(constants.JOB_SEEKERS_DATA_FOR_TESTING_FILTERS):
        js_skills = skills.copy()
        address_data = {
            'address': 'unique_address{}'.format(i),
            'country': country_usa,
        }
        if item['city'] == city_new_york.name:
            address_data['city'] = city_new_york
            address_data['zip'] = zip_new_york
        elif item['city'] == city_ashville.name:
            address_data['city'] = city_ashville
            address_data['zip'] = zip_ashville
        else:
            address_data['city'] = city_packwood
            address_data['zip'] = zip_packwood

        if item.get('add_more_skills', False):
            js_skills.append(spreadsheet_software_skill)
        create_job_seeker(
            item['user_data'],
            item['js_data'],
            address_data,
            js_skills)

    return result


@pytest.fixture
def job_seeker_profile_view(job_seeker, company_user_client):
    resp = api_requests.get_job_seeker_details(company_user_client,
                                               job_seeker.id)
    assert resp.status_code == http.HTTPStatus.OK


@pytest.fixture
def viewed_profiles(
        job_seeker, job_seeker_2, company_user_client, company_2_user_client):

    def view_profile(client, js_id):
        resp = api_requests.get_job_seeker_details(client, js_id)
        assert resp.status_code == http.HTTPStatus.OK

    job_seekers = (job_seeker, job_seeker_2)
    clients = (company_user_client, company_2_user_client)
    for js in job_seekers:
        for client in clients:
            view_profile(client, js.id)
    return (job_seeker, job_seeker_2)


@pytest.fixture
def remove_job_seeker_data(job_seeker):
    return {
        'remove': True,
    }
