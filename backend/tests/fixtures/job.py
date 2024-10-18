import http

import pytest

from job import models
from leet import enums
from tests import api_requests


@pytest.fixture
def industry_construction(db):
    return models.Industry.objects.get_or_create(name='Construction')[0]


@pytest.fixture
def industry_manufacturing(db):
    return models.Industry.objects.get_or_create(name='Manufacturing')[0]


@pytest.fixture
def document_management_software_skill():
    return models.Skill.objects.get_or_create(
        name='Document management software')[0]


@pytest.fixture
def electronic_mail_software_skill():
    return models.Skill.objects.get_or_create(
        name='Electronic mail software')[0]


@pytest.fixture
def office_suite_software_skill():
    return models.Skill.objects.get_or_create(
        name='Office suite software')[0]


@pytest.fixture
def operating_system_software_skill():
    return models.Skill.objects.get_or_create(
        name='Operating system software')[0]


@pytest.fixture
def project_management_software_skill():
    return models.Skill.objects.get_or_create(
        name='Project management software')[0]


@pytest.fixture
def spreadsheet_software_skill():
    return models.Skill.objects.get_or_create(
        name='Spreadsheet software')[0]


@pytest.fixture
def mysql_skill():
    return models.Skill.objects.get_or_create(name='MySQL')[0]


@pytest.fixture
def outlook_skill():
    return models.Skill.objects.get_or_create(name='Microsoft Outlook')[0]


@pytest.fixture
def required_skills(electronic_mail_software_skill):
    return [electronic_mail_software_skill.id]


@pytest.fixture
def optional_skills(operating_system_software_skill):
    return [operating_system_software_skill.id]


@pytest.fixture
def job_base_data(
        industry_manufacturing, company,
        required_skills, optional_skills, city_ashville, country_usa):
    return {
        'title': 'title',
        'status': enums.JobStatusEnum.ACTIVE.name,
        'description': 'description',
        'location': {'city': city_ashville.id, 'country': country_usa.id},
        'industry': industry_manufacturing.id,
        'position_type': enums.PositionTypesEnum.CONTRACT.name,
        'education': enums.EducationTypesEnum.ASSOCIATES_DEGREE.name,
        'salary_negotiable': False,
        'salary_min': 200,
        'salary_max': 400,
        'clearance': enums.ClearanceTypesEnum.CONFIDENTIAL.name,
        'experience': enums.ExperienceEnum.FROM_1_TO_2.name,
        'benefits': enums.BenefitsEnum.FOUR_OH_ONE_KEY.name,
        'travel': enums.TravelOpportunitiesEnum.NO_TRAVEL.name,
        'required_skills': required_skills,
        'optional_skills': optional_skills,
        'autoapply_minimal_percent': 50
    }


@pytest.fixture
def job1(
        company_user_client, job_base_data, electronic_mail_software_skill,
        document_management_software_skill, office_suite_software_skill,
        project_management_software_skill):
    data = job_base_data.copy()
    data['title'] = 'JP1'
    data['required_skills'] = [
        document_management_software_skill.id,
        office_suite_software_skill.id,
        electronic_mail_software_skill.id
    ]
    data['optional_skills'] = [project_management_software_skill.id,]
    resp = api_requests.create_job(
        company_user_client, data)
    return resp.json()


@pytest.fixture
def job2(
        company_user_client, job_base_data, electronic_mail_software_skill,
        document_management_software_skill, office_suite_software_skill,
        operating_system_software_skill, project_management_software_skill):
    data = job_base_data.copy()
    data['title'] = 'JP2'
    data['required_skills'] = [
        electronic_mail_software_skill.id,
        document_management_software_skill.id,
        office_suite_software_skill.id,
        operating_system_software_skill.id,
        project_management_software_skill.id
    ]
    data['optional_skills'] = []
    resp = api_requests.create_job(
        company_user_client, data)
    return resp.json()


@pytest.fixture
def job3(company_user_client, job_base_data,
         document_management_software_skill):
    data = job_base_data.copy()
    data['title'] = 'JP3'
    data['required_skills'] = [document_management_software_skill.id]
    data['optional_skills'] = []
    resp = api_requests.create_job(
        company_user_client, data)
    return resp.json()


@pytest.fixture
def job4(company_user_client, job_base_data, electronic_mail_software_skill,
         office_suite_software_skill, spreadsheet_software_skill):
    data = job_base_data.copy()
    data['title'] = 'JP4'
    data['required_skills'] = [
        electronic_mail_software_skill.id,
        office_suite_software_skill.id,
        spreadsheet_software_skill.id
    ]
    data['optional_skills'] = []
    resp = api_requests.create_job(
        company_user_client, data)
    return resp.json()


@pytest.fixture
def job5(
        company_user_client, job_base_data, electronic_mail_software_skill,
        operating_system_software_skill, project_management_software_skill,
        spreadsheet_software_skill):
    data = job_base_data.copy()
    data['title'] = 'JP5'
    data['required_skills'] = [
        electronic_mail_software_skill.id,
        operating_system_software_skill.id,
        project_management_software_skill.id,
        spreadsheet_software_skill.id
    ]
    data['optional_skills'] = []
    resp = api_requests.create_job(
        company_user_client, data)
    return resp.json()


@pytest.fixture
def job6(
        company_user_client, job_base_data, electronic_mail_software_skill,
        document_management_software_skill, office_suite_software_skill,
        operating_system_software_skill,
        project_management_software_skill,
        spreadsheet_software_skill):
    data = job_base_data.copy()
    data['title'] = 'JP6'
    data['required_skills'] = [
        electronic_mail_software_skill.id,
        document_management_software_skill.id,
        office_suite_software_skill.id,
        operating_system_software_skill.id,
        project_management_software_skill.id,
        spreadsheet_software_skill.id
    ]
    data['optional_skills'] = []
    resp = api_requests.create_job(
        company_user_client, data)
    return resp.json()


@pytest.fixture
def job_questions_data():
    return [
        {
            'body': 'question1',
            'is_answer_required': True,
            'disqualifying_answer': 'YES'
        },
        {
            'body': 'question2',
            'disqualifying_answer': 'NO'
        },
        {
            'body': 'question3',
        },
    ]


@pytest.fixture
def job(company_user_client, job_base_data, required_skills, optional_skills):
    """Published job of company"""
    data = job_base_data.copy()
    data['required_skills'] = required_skills
    data['optional_skills'] = optional_skills
    resp = api_requests.create_job(
        company_user_client,
        data
    )
    assert resp.status_code == http.HTTPStatus.CREATED
    return resp.json()


@pytest.fixture
def job_with_questions(
        company_user_client, job_base_data,
        required_skills, optional_skills, job_questions_data):
    data = job_base_data.copy()
    data['title'] += data['title']
    data['required_skills'] = required_skills
    data['optional_skills'] = optional_skills
    data['questions'] = job_questions_data
    resp = api_requests.create_job(
        company_user_client,
        data
    )
    assert resp.status_code == http.HTTPStatus.CREATED
    return resp.json()


@pytest.fixture
def job_questions(job_with_questions):
    return job_with_questions['questions']


@pytest.fixture
def answers_base_data(job_questions):
    return [
        {
            'question': job_questions[0]['id'],
            'answer': {
                'yes_no_value': enums.YesNoAnswerEnum.NO.name
            }
        },
        {
            'question': job_questions[1]['id'],
            'answer': {
                'yes_no_value': enums.YesNoAnswerEnum.YES.name
            }
        },
        {
            'question': job_questions[2]['id'],
            'answer': {}
        }
    ]


@pytest.fixture
def job_survey_answers(
        job_with_questions, job_seeker_client, answers_base_data):
    resp = api_requests.create_answers_to_questions(
        job_seeker_client,
        job_with_questions['id'],
        answers_base_data)
    assert resp.status_code == http.HTTPStatus.CREATED
    return resp.json()


@pytest.fixture
def job_survey_only_required_answers(
        job_with_questions, job_seeker_client, answers_base_data):
    resp = api_requests.create_answers_to_questions(
        job_seeker_client,
        job_with_questions['id'],
        [answers_base_data[0]])
    assert resp.status_code == http.HTTPStatus.CREATED
    return resp.json()


@pytest.fixture
def company_deleted_job(
        company_user_client, job_base_data):
    """Deleted company job"""
    data = job_base_data.copy()
    data['title'] += data['title']
    create_job_resp = api_requests.create_job(
        company_user_client,
        data
    )
    assert create_job_resp.status_code == http.HTTPStatus.CREATED
    resp = api_requests.delete_job(
        company_user_client,
        create_job_resp.json()['id']
    )
    assert resp.status_code == http.HTTPStatus.NO_CONTENT
    return create_job_resp.json()


@pytest.fixture
def company_inactive_job_id(
        company_user_client, job_base_data):
    """Hard deleted company job"""
    data = job_base_data.copy()
    data['title'] += data['title']
    create_job_resp = api_requests.create_job(
        company_user_client,
        data
    )
    job_id = create_job_resp.json()['id']
    assert create_job_resp.status_code == http.HTTPStatus.CREATED
    resp = api_requests.delete_job(
        company_user_client,
        create_job_resp.json()['id']
    )
    assert resp.status_code == http.HTTPStatus.NO_CONTENT
    job = models.Job.objects.get(id=job_id)
    job.is_active = False
    job.save()
    return job_id


@pytest.fixture
def company_2_job(
        company_2_user_client, job_base_data, electronic_mail_software_skill,
        document_management_software_skill, office_suite_software_skill):
    data = job_base_data.copy()
    data['title'] = 'JP1'
    data['required_skills'] = [
        document_management_software_skill.id, office_suite_software_skill.id,
        electronic_mail_software_skill.id]
    data['optional_skills'] = []
    resp = api_requests.create_job(
        company_2_user_client, data)
    return resp.json()


@pytest.fixture
def all_published_jobs(
        job, company_2_job, job1, job2,
        job3, job4, job5, job6):
    return (
        job, company_2_job, job1, job2,
        job3, job4, job5, job6
    )


@pytest.fixture
def company_jobs(job1, job2, job3, job4, job5, job6):
    return job1, job2, job3, job4, job5, job6


@pytest.fixture
def job_draft(company_user_client, job_base_data):
    """Company's draft job
    This job matched with job seeker skills and education, etc."""
    data = job_base_data.copy()
    data['status'] = enums.JobStatusEnum.DRAFT.name
    resp = api_requests.create_job(
        company_user_client,
        data)
    assert resp.status_code == http.HTTPStatus.CREATED
    return resp.json()


@pytest.fixture
def job_obj(company_user_client, job1):
    job = models.Job.objects.get(id=job1['id'])
    return job


@pytest.fixture
def job_closed(company_user_client, job, job_base_data):
    """Closed company job"""
    data = job_base_data.copy()
    data['status'] = enums.JobStatusEnum.CLOSED.name
    resp = api_requests.update_job(
        company_user_client,
        job['id'],
        data)
    assert resp.status_code == http.HTTPStatus.OK
    return resp.json()
