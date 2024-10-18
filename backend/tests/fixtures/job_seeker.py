import http

import pytest
from django.utils import timezone

from auth import services
from geo import models as geo_models
from leet import enums
from tests import api_requests
from tests import constants
from tests import factories
from tests import utils


def purchase_job_seeker(client, job_seeker):
    resp = api_requests.purchase_job_seeker(client, job_seeker.id)
    assert resp.status_code == http.HTTPStatus.OK
    return job_seeker


@pytest.fixture
def job_seeker_base_data(db):
    return {
        'email': utils.get_unique_user_email(),
        'first_name': constants.JOB_SEEKER_FIRST_NAME,
        'last_name': constants.JOB_SEEKER_LAST_NAME,
        'password': constants.DEFAULT_PASSWORD,
    }


@pytest.fixture
def job_seeker_info(industry_construction):
    return {
        'position_type': enums.PositionTypesEnum.CONTRACT.name,
        'education': enums.EducationTypesEnum.ASSOCIATES_DEGREE.name,
        'salary_public': True,
        'salary_min': 200,
        'salary_max': 400,
        'clearance': enums.ClearanceTypesEnum.CONFIDENTIAL.name,
        'experience': enums.ExperienceEnum.FROM_1_TO_2.name,
        'benefits': enums.BenefitsEnum.FOUR_OH_ONE_KEY.name,
        'travel': enums.JSTravelOpportunitiesEnum.NO_TRAVEL.name,
        'phone': '+375297777777',
        'about': 'about'
    }


@pytest.fixture
def job_seeker(job_seeker_base_data, job_seeker_info,
               electronic_mail_software_skill, operating_system_software_skill,
               document_management_software_skill, country_usa,
               industry_construction, city_new_york, zip_new_york):
    user = factories.create_base_user(**job_seeker_base_data)
    user = services.create_job_seeker(user)
    job_seeker = user.job_seeker
    for attr, val in job_seeker_info.items():
        setattr(job_seeker, attr, val)
    job_seeker.is_public = True
    job_seeker.skills.add(
        electronic_mail_software_skill,
        operating_system_software_skill,
        document_management_software_skill)
    job_seeker.address = geo_models.Address.objects.create(
        address='6942 Mccoy Lakes',
        country=country_usa,
        city=city_new_york,
        zip=zip_new_york,
    )
    job_seeker.industries.add(industry_construction)
    job_seeker.save()
    return job_seeker


@pytest.fixture
def job_seeker_with_photo(job_seeker_client, job_seeker, fake_photo):
    data = {"photo": fake_photo}
    resp = api_requests.upload_photo(
        job_seeker_client,
        job_seeker.id,
        data)
    assert resp.status_code == http.HTTPStatus.OK
    return job_seeker


@pytest.fixture
def shared_job_seeker(job_seeker):
    job_seeker.is_shared = True
    job_seeker.save()
    return job_seeker


@pytest.fixture
def job_seeker_2(db, job_seeker_base_data, country_usa, city_ashville,
                 zip_ashville):
    data = job_seeker_base_data.copy()
    data['last_name'] = '{}_second'.format(data['last_name'])
    data['first_name'] = '{}_second'.format(data['first_name'])
    data['email'] = 'second{}'.format(data['email'])
    user = factories.create_base_user(**data)
    user = services.create_job_seeker(user)
    job_seeker = user.job_seeker
    job_seeker.is_public = True
    job_seeker.address = geo_models.Address.objects.create(
        address='0691 Regina Crest',
        country=country_usa,
        city=city_ashville,
        zip=zip_ashville,
    )
    job_seeker.save()
    return job_seeker


@pytest.fixture
def job_seeker_3(db, job_seeker_base_data, country_usa, city_ashville,
                 zip_ashville):
    data = job_seeker_base_data.copy()
    data['last_name'] = '{}_third'.format(data['last_name'])
    data['first_name'] = '{}_third'.format(data['first_name'])
    data['email'] = 'third{}'.format(data['email'])
    user = factories.create_base_user(**data)
    user = services.create_job_seeker(user)
    job_seeker = user.job_seeker
    job_seeker.is_public = True
    job_seeker.address = geo_models.Address.objects.create(
        address='0691 Regina Crest',
        country=country_usa,
        city=city_ashville,
        zip=zip_ashville,
    )
    job_seeker.save()
    return job_seeker


@pytest.fixture
def purchased_job_seeker(company_user_client, job_seeker):
    return purchase_job_seeker(company_user_client, job_seeker)


@pytest.fixture
def purchased_job_seeker_2(company_user_client, job_seeker_2):
    return purchase_job_seeker(company_user_client, job_seeker_2)


@pytest.fixture
def purchased_job_seeker_3(company_user_client, job_seeker_3):
    return purchase_job_seeker(company_user_client, job_seeker_3)


@pytest.fixture
def purchased_job_seekers(purchased_job_seeker, purchased_job_seeker_2):
    return [purchased_job_seeker, purchased_job_seeker_2]


@pytest.fixture
def cover_letter_data():
    return {
        'title': 'title',
        'body': 'body',
        'is_default': False
    }


@pytest.fixture
def cover_letter(job_seeker_client, job_seeker, cover_letter_data):
    resp = api_requests.create_cover_letter(
        job_seeker_client,
        job_seeker_id=job_seeker.id,
        data=cover_letter_data
    )
    assert resp.status_code == http.HTTPStatus.CREATED
    return resp.json()


@pytest.fixture
def job_seeker_hidden(job_seeker):
    job_seeker.is_public = False
    job_seeker.save()
    return job_seeker


@pytest.fixture
def education_data():
    return {
        'institution': 'institution',
        'field_of_study': 'study',
        'degree': '',
        'date_from': str(utils.date(2018, 1, 1)),
        'date_to': str(utils.date(2018, 9, 1)),
        'location': 'location',
        'description': 'descripion',
    }


@pytest.fixture
def certification_data():
    return {
        'institution': 'institution',
        'field_of_study': 'study',
        'graduated': str(utils.date(2018, 9, 1)),
        'licence_number': '10001aoooa',
        'location': 'location',
        'description': 'descripion',
    }


@pytest.fixture
def educations(job_seeker_client, job_seeker, education_data):
    """This fixture use for testing list of educations of job seeker"""

    def add_education(data, is_current=False):
        req_data = education_data.copy()
        req_data.update(data)
        if is_current:
            req_data.pop('date_to')
            req_data['is_current'] = is_current
        resp = api_requests.add_education(
            job_seeker_client,
            job_seeker.id,
            req_data)
        assert resp.status_code == http.HTTPStatus.CREATED
        educations.append(resp.json())

    educations = []

    add_education({'institution': 'education1'})
    add_education({'institution': 'education2'}, is_current=True)
    add_education({'institution': 'education3'})
    return educations


@pytest.fixture
def certifications(job_seeker_client, job_seeker, certification_data):
    """This fixture use for testing list of certifications of job seeker"""

    def add_certification(data, is_current=False):
        req_data = certification_data.copy()
        req_data.update(data)
        if is_current:
            req_data.pop('graduated')
            req_data.pop('licence_number')
            req_data['is_current'] = is_current
        resp = api_requests.add_certification(
            job_seeker_client,
            job_seeker.id,
            req_data)
        assert resp.status_code == http.HTTPStatus.CREATED
        certifications.append(resp.json())

    certifications = []

    add_certification({'institution': 'certification1'})
    add_certification({'institution': 'certification2'}, is_current=True)
    add_certification({'institution': 'certification3'})
    return certifications


@pytest.fixture
def job_experience(
        job_seeker_client, job_seeker, job_experience_data):
    resp = api_requests.add_job_experience(
        job_seeker_client,
        job_seeker.id,
        job_experience_data)
    assert resp.status_code == http.HTTPStatus.CREATED
    return resp.json()


@pytest.fixture
def job_experience_data():
    return {
        'company': 'job seeker company',
        'job_title': 'title',
        'date_from': str(timezone.datetime(2018, 1, 1)),
        'description': 'some description',
        'is_current': True,
        'employment': enums.EmploymentEnum.FULL_TIME.name
    }


@pytest.fixture
def document_doc():
    return open('tests/test_files/sample.doc', 'rb')


@pytest.fixture
def document_docx():
    return open('tests/test_files/sample.docx', 'rb')


@pytest.fixture
def document_odt():
    return open('tests/test_files/sample.odt', 'rb')


@pytest.fixture
def document_pdf():
    return open('tests/test_files/sample.pdf', 'rb')


@pytest.fixture
def document_rtf():
    return open('tests/test_files/sample.rtf', 'rb')


@pytest.fixture
def document_txt():
    return open('tests/test_files/sample.txt', 'rb')


@pytest.fixture
def document_wrong_extension():
    return open('tests/test_files/sample_wrong_extension.odt', 'rb')


@pytest.fixture
def document_data(document_doc, job_seeker):
    return {
        'file': document_doc,
        'name': 'test doc',
    }

@pytest.fixture
def document(job_seeker_client, job_seeker, document_data):
    resp = api_requests.add_document(
        job_seeker_client,
        job_seeker.id,
        document_data)
    assert resp.status_code == http.HTTPStatus.CREATED
    return resp.json()


@pytest.fixture
def save_job_seeker_data(job_seeker):
    return {
        'add': True,
    }


@pytest.fixture
def photo_png():
    return open('tests/test_files/photo_sample.png', 'rb')


@pytest.fixture
def photo_bmp():
    return open('tests/test_files/photo_sample.bmp', 'rb')


@pytest.fixture
def photo_gif():
    return open('tests/test_files/photo_sample.gif', 'rb')


@pytest.fixture
def photo_jpg():
    return open('tests/test_files/photo_sample.jpg', 'rb')


@pytest.fixture
def photo_tiff():
    return open('tests/test_files/photo_sample.tiff', 'rb')


@pytest.fixture
def photo_wrong_extension():
    return open('tests/test_files/photo_sample_wrong_extension.png', 'rb')


@pytest.fixture
def photo_data(photo_png):
    return {
        'photo': photo_png,
    }

@pytest.fixture
def saved_job_seeker(company_user_client, job_seeker, save_job_seeker_data):
    resp = api_requests.save_remove_job_seeker(
        company_user_client,
        job_seeker.id,
        save_job_seeker_data)
    assert resp.status_code == http.HTTPStatus.OK
    return job_seeker
