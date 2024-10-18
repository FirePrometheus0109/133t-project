import http

import pytest
from faker import Faker

from apply import tasks
from job.models import Job
from tests import utils
from leet import enums
from tests import api_requests


fake = Faker()


EXPECTED_JOB_LIST_FIELDS = [
    'id',
    'title',
    'company',
    'location',
    'matching_percent',
    'created_at',
    'position_type',
    'salary_negotiable',
    'education',
    'clearance',
    'travel',
    'benefits',
    'experience',
    'all_required_skills_count',
    'matched_required_skills_count',
    'is_clearance_match',
    'is_required_skills_match',
    'is_questionnaire_answered',
]

EXPECTED_JOB_DETAILS_FIELDS = EXPECTED_JOB_LIST_FIELDS + [
    'required_skills', 'optional_skills', 'description']


class TestNewAutoapplyJobApiList:

    @pytest.mark.usefixtures(
        'job1', 'job2', 'job3', 'job4', 'job5', 'job6')
    def test_list_items_contain_appropriate_fields(
            self, job_seeker_client):
        resp = api_requests.get_new_autoapply_jobs_list(job_seeker_client)
        assert resp.status_code == http.HTTPStatus.OK
        for jp in resp.json()['results']:
            for field in EXPECTED_JOB_LIST_FIELDS:
                assert field in jp

    def test_job_list_filter_by_position(self, job_seeker_client, job1, job2):
        job2_obj = Job.objects.get(id=job2['id'])
        job2_obj.position_type = enums.PositionTypesEnum.COMMISSION.name
        job2_obj.save()
        resp = api_requests.get_new_autoapply_jobs_list(job_seeker_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['results'][0]['id'] == job1['id']
        assert resp.json()['count'] == 1

    @pytest.mark.usefixtures(
        'job1', 'job2', 'job3', 'job4', 'job5', 'job6')
    def test_job_list_ordered_correctly(
            self, job_seeker_client, job_seeker,
            document_management_software_skill,
            spreadsheet_software_skill):
        job_seeker.skills.clear()
        job_seeker.skills.add(
            document_management_software_skill,
            spreadsheet_software_skill)
        resp = api_requests.get_new_autoapply_jobs_list(job_seeker_client)
        assert resp.status_code == http.HTTPStatus.OK
        expected_job_info = [
            {'title': 'JP3', 'matching_percent': '100.00'},
            {'title': 'JP1', 'matching_percent': '33.33'},
            {'title': 'JP4', 'matching_percent': '33.33'},
            {'title': 'JP6', 'matching_percent': '33.33'},
            {'title': 'JP5', 'matching_percent': '25.00'},
            {'title': 'JP2', 'matching_percent': '20.00'}
        ]
        for i in range(len(resp.json()['results'])):
            assert (resp.json()['results'][i]['title'] ==
                    expected_job_info[i]['title'])
            assert (resp.json()['results'][i]['matching_percent'] ==
                    expected_job_info[i]['matching_percent'])

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
            http.HTTPStatus.FORBIDDEN,
        ),
    ))
    def test_get_autoapply_jobs_list_permissions(
            self, request, client, status, job_seeker_autoapply):
        client = request.getfixturevalue(client)
        resp = api_requests.get_new_autoapply_jobs_list(client)
        assert resp.status_code == status


class TestSavedAutoapplyJobApiList:

    def test_new_job_tried_to_apply_after_list_obtaining(
            self, job_seeker_client, job_seeker_autoapply, job3, job5):
        resp = api_requests.start_autoapply(
            job_seeker_client, job_seeker_autoapply['id'],
            data={
                'applied_jobs': [
                    job3['id']]
            })
        assert resp.status_code == http.HTTPStatus.OK
        assert (resp.json()['status'] ==
                enums.AutoapplyStatusEnum.IN_PROGRESS.name)
        tasks.find_autoapply_jobs.delay()
        status = enums.ApplyStatusEnum.APPLIED.name
        resp = api_requests.get_autoapply_jobs_list(
            job_seeker_client,
            job_seeker_autoapply['id']
        )
        assert resp.status_code == http.HTTPStatus.OK
        assert 'results' in resp.json()
        new_job = next(
            j for j in resp.json()['results'] if j['id'] == job5['id']
        )
        assert new_job['apply_job_status'] == status

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
            http.HTTPStatus.FORBIDDEN,
        ),
    ))
    def test_start_autoapply_permissions(
            self, request, client, status, job3, job_seeker_autoapply):
        client = request.getfixturevalue(client)
        resp = api_requests.start_autoapply(
            client,
            job_seeker_autoapply['id'],
            data={
                'applied_jobs': [
                    job3['id']]
            })
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
            http.HTTPStatus.FORBIDDEN,
        ),
    ))
    def test_get_autoapply_jobs_list_permissions(
            self, request, client, status, job_seeker_autoapply):
        client = request.getfixturevalue(client)
        resp = api_requests.get_autoapply_jobs_list(
                client,
                job_seeker_autoapply['id']
            )
        assert resp.status_code == status


class TestAutoapplyJobApiDetails:

    def test_get_job_details_contains_appropriate_fields(
            self, job_seeker_client, job1):
        resp = api_requests.get_autoapply_job_details(
            job_seeker_client, job1['id'])
        assert resp.status_code == http.HTTPStatus.OK
        for field in EXPECTED_JOB_DETAILS_FIELDS:
            assert field in resp.json()

    def test_get_job_details_shows_skills_matching(
            self, job_seeker_client, job_seeker,
            document_management_software_skill,
            electronic_mail_software_skill, job6):
        job_seeker.skills.clear()
        job_seeker.skills.add(
            document_management_software_skill,
            electronic_mail_software_skill)
        resp = api_requests.get_autoapply_job_details(
            job_seeker_client, job6['id'])
        assert resp.status_code == http.HTTPStatus.OK
        required_skills = resp.json()['required_skills']
        for skill in required_skills:
            if any((skill['id'] == document_management_software_skill.id,
                    skill['id'] == electronic_mail_software_skill.id)):
                assert skill['match'] is True
            else:
                assert skill['match'] is False

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
            http.HTTPStatus.FORBIDDEN,
        ),
    ))
    def test_get_autoaply_job_details_permissions(
            self, request, client, status, job1):
        client = request.getfixturevalue(client)
        resp = api_requests.get_autoapply_job_details(
            client,
            job1['id'])
        assert resp.status_code == status


class TestBannedJobAutoApplyList:

    def test_banned_job_not_in_autoapply_list(self, job_seeker_client,
                                              job_obj):
        resp = api_requests.get_new_autoapply_jobs_list(job_seeker_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == 1

        utils.ban_entity(job_obj)
        resp = api_requests.get_new_autoapply_jobs_list(job_seeker_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == 0
