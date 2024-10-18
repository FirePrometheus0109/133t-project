import http

import pytest

from apply import constants
from apply.models import Autoapply
from geo.models import Address
from job.models import Job, Industry
from leet import enums
from tests import api_requests
from tests import validators
from tests.utils import get_random_database_object


class TestAutoapplyApiCommon:

    def test_create_success(
            self, job_seeker_client, autoapply_base_data):
        resp = api_requests.save_autoapply(
            job_seeker_client, autoapply_base_data)
        assert resp.status_code == http.HTTPStatus.CREATED
        assert resp.json()['title'] == autoapply_base_data['title']
        assert (resp.json()['query_params'] ==
                autoapply_base_data['query_params'])
        assert (set(resp.json()['stopped_jobs']) ==
                set(autoapply_base_data['stopped_jobs']))
        assert (set(resp.json()['deleted_jobs']) ==
                set(autoapply_base_data['deleted_jobs']))
        assert resp.json()['number'] == autoapply_base_data['number']
        assert resp.json()['status'] == enums.AutoapplyStatusEnum.SAVED.name

    def test_update_success(
            self, job_seeker_client, job_seeker_autoapply, autoapply_base_data,
            job2, city_new_york):
        data = autoapply_base_data.copy()
        data.update({
            'title': 'New title',
            'query_params': 'title=Comp&city_id={}'.format(city_new_york.id),
            'stopped_jobs': [job2['id']],
            'deleted_jobs': [],
            'number': 1
        })
        resp = api_requests.update_autoapply(
            job_seeker_client, job_seeker_autoapply['id'], data)
        assert resp.status_code == http.HTTPStatus.OK

    def test_update_fails_if_invalid_city_id_in_query_params(
            self, job_seeker_client, job_seeker_autoapply, autoapply_base_data,
            job2, settings):
        data = autoapply_base_data.copy()
        data.update({
            'title': 'New title',
            'query_params': 'title=Comp&city_id={}'.format(9999999),
            'stopped_jobs': [job2['id']],
            'deleted_jobs': [],
            'number': 1
        })
        resp = api_requests.update_autoapply(
            job_seeker_client, job_seeker_autoapply['id'], data)
        emsg = constants.INVALID_CITY_ID_IN_QUERY_PARAMS_ERROR
        validators.validate_error_message(resp, emsg, 'query_params')

    def test_autoapply_title_unique_for_user(
            self, job_seeker_client, autoapply_base_data):
        resp = api_requests.save_autoapply(
            job_seeker_client, autoapply_base_data)
        assert resp.status_code == http.HTTPStatus.CREATED
        resp = api_requests.save_autoapply(
            job_seeker_client, autoapply_base_data)
        validators.validate_error_message(
            resp,
            constants.AUTOAPPLY_TITLE_SHOULD_BE_UNIQUE_ERROR,
            'title')

    @pytest.mark.usefixtures('started_autoapply')
    def test_autoapply_list(self, job_seeker_client):
        resp = api_requests.get_autoapplies(job_seeker_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == 1
        exp_fields = (
            'id',
            'title',
            'status',
            'jobs_count',
            'new_jobs_count',
            'days_to_completion'
        )
        data = resp.json()['results'][0]
        for i in exp_fields:
            assert i in data

    @pytest.mark.usefixtures('job_seeker_autoapply2')
    def test_autoapply_list_returns_correct_number_of_jobs(
            self, job_seeker_client, all_published_jobs):
        # NOTE job_seeker_autoapply2 does not have filters or excluded cases
        # jobs_count should be equal count all_published_jobs
        resp = api_requests.get_autoapplies(job_seeker_client)
        assert resp.status_code == http.HTTPStatus.OK
        jobs_count = resp.json()['results'][0]['jobs_count']
        assert jobs_count == len(all_published_jobs)


class TestAutoapplyApiAccess:
    def test_user_cant_update_not_own_autoapply(
            self, job_seeker_client, job_seeker_2_autoapply):
        resp = api_requests.update_autoapply(
            job_seeker_client, job_seeker_2_autoapply['id'], {})
        assert resp.status_code == http.HTTPStatus.NOT_FOUND

    def test_user_cant_view_not_own_autoapply(
            self, job_seeker_client, job_seeker_2_autoapply):
        resp = api_requests.get_autoapply(
            job_seeker_client, job_seeker_2_autoapply['id'])
        assert resp.status_code == http.HTTPStatus.NOT_FOUND

    def test_user_cant_specify_more_than_30_jobs_for_one_autoapply(
            self, job_seeker_client, autoapply_base_data):
        data = autoapply_base_data.copy()
        data.update({'number': 31})
        resp = api_requests.save_autoapply(
            job_seeker_client, data)
        validators.validate_error_message(
            resp,
            constants.MORE_THAN_30_JOBS_ERROR,
            'number')

    def test_user_cant_start_autoapply_if_profile_isnt_public(
            self, job_seeker_client, job_seeker, job_seeker_autoapply, job1):
        job_seeker.is_public = False
        job_seeker.save()
        resp = api_requests.start_autoapply(
            job_seeker_client, job_seeker_autoapply['id'],
            data={
                'applied_jobs': [
                    job1['id'],
                ]
            })
        validators.validate_error_message(
            resp,
            constants.PROFILE_ISNT_PUBLIC_ERROR,
            error_code=http.HTTPStatus.FORBIDDEN)


class TestInstantAutoapplyApiStart:
    def test_start_success(
            self, job_seeker_client, job_seeker_autoapply,
            job1, job2, job3):
        resp = api_requests.start_autoapply(
            job_seeker_client, job_seeker_autoapply['id'],
            data={
                'applied_jobs': [
                    job1['id'],
                    job2['id']]
            })
        assert resp.status_code == http.HTTPStatus.OK
        assert 'applied_jobs' in resp.json()
        assert 'status' in resp.json()
        for result in resp.json()['applied_jobs']:
            assert 'applied_at' in result
            assert 'apply_job_status' in result

    @pytest.mark.usefixtures('job2', 'job3')
    def test_start_autoapply_fails_if_it_was_started(
            self, job_seeker_client, job_seeker_autoapply, job1):
        resp = api_requests.start_autoapply(
            job_seeker_client, job_seeker_autoapply['id'],
            data={
                'applied_jobs': [job1['id']]
            })
        assert resp.status_code == http.HTTPStatus.OK
        resp = api_requests.start_autoapply(
            job_seeker_client, job_seeker_autoapply['id'],
            data={
                'applied_jobs': [job1['id']]
            })
        assert resp.status_code == http.HTTPStatus.BAD_REQUEST

    def test_start_autoapply_with_empty_job_list(
            self, job_seeker_client, job_seeker_autoapply):
        resp = api_requests.start_autoapply(
            job_seeker_client, job_seeker_autoapply['id'],
            data={'applied_jobs': []})
        assert resp.status_code == http.HTTPStatus.OK

    def test_start_autoapply_fails_if_more_than_30_job_in_list(
            self, job_seeker_client, job_seeker_autoapply, company,
            company_user, country_usa, city_ashville):
        industry = get_random_database_object(Industry.objects)
        Address.objects.create(city=city_ashville, country=country_usa)
        data = [{
            'title': 'JP{}'.format(i),
            'industry_id': industry.id,
            'company': company,
            'location': Address.objects.create(
                city=city_ashville, country=country_usa
            ),
            'owner': company_user
        } for i in range(31)]
        jobs = Job.objects.bulk_create(Job(**i) for i in data)
        resp = api_requests.start_autoapply(
            job_seeker_client, job_seeker_autoapply['id'],
            data={'applied_jobs': [job.id for job in jobs]})
        assert resp.status_code == http.HTTPStatus.BAD_REQUEST

    def test_apply_to_job_after_questionnaire_was_answered(
            self, job_seeker_client, job_seeker_autoapply_for_one_job,
            job_with_questions, answers_base_data,
            job_seeker):
        resp = api_requests.start_autoapply(
            job_seeker_client, job_seeker_autoapply_for_one_job['id'],
            data={
                'applied_jobs': [job_with_questions['id']]
            })
        assert resp.status_code == http.HTTPStatus.OK
        assert 'applied_jobs' in resp.json()
        autoapply_job = resp.json()['applied_jobs'][0]
        assert (autoapply_job['apply_job_status'] ==
                enums.ApplyStatusEnum.NEED_REVIEW.name)
        resp = api_requests.create_answers_to_questions(
            job_seeker_client,
            job_with_questions['id'],
            answers_base_data)
        assert resp.status_code == http.HTTPStatus.CREATED
        resp = api_requests.autoapply_to_job(
            job_seeker_client,
            job_seeker_autoapply_for_one_job['id'],
            job_with_questions['id']
        )
        assert resp.status_code == http.HTTPStatus.OK
        result = resp.json()
        assert 'applied_at' in result
        assert result['status'] == enums.ApplyStatusEnum.APPLIED.name
        assert result['owner'] == job_seeker.id
        assert result['job'] == job_with_questions['id']

    def test_autoapply_to_job_fails_if_number_exceed(
            self, job_seeker_client, job_seeker_autoapply,
            job, job1, job2, job3):
        resp = api_requests.start_autoapply(
            job_seeker_client, job_seeker_autoapply['id'],
            data={
                'applied_jobs': [job['id'], job1['id'], job3['id']]
            })
        assert resp.status_code == http.HTTPStatus.OK
        assert 'applied_jobs' in resp.json()
        resp = api_requests.autoapply_to_job(
            job_seeker_client,
            job_seeker_autoapply['id'],
            job2['id']
        )
        emsg = constants.AUTOAPPLY_NUMBER_EXCEED_ERROR
        validators.validate_error_message(resp, emsg)


class TestAutoapplyDeleteApi:
    def test_delete_autoapply_success(
            self, job_seeker_autoapply, job_seeker_client):
        resp = api_requests.delete_autoapply(
            job_seeker_client, job_seeker_autoapply['id']
        )
        assert resp.status_code == http.HTTPStatus.NO_CONTENT

    def test_delete_not_own_autoapply_fails(
            self, job_seeker_autoapply, job_seeker_2_client):
        resp = api_requests.delete_autoapply(
            job_seeker_2_client, job_seeker_autoapply['id']
        )
        assert resp.status_code == http.HTTPStatus.NOT_FOUND


class TestAutopplyStopApi:
    def test_stop_autoapply_success(
            self, job_seeker_autoapply, job_seeker_client):
        autoapply_inst = Autoapply.objects.get(id=job_seeker_autoapply['id'])
        autoapply_inst.status = enums.AutoapplyStatusEnum.IN_PROGRESS.name
        autoapply_inst.save()
        resp = api_requests.stop_autoapply(
            job_seeker_client,
            job_seeker_autoapply['id']
        )
        assert resp.status_code == http.HTTPStatus.OK
        assert 'status' in resp.json()
        assert resp.json()['status'] == enums.AutoapplyStatusEnum.STOPPED.name

    @pytest.mark.parametrize(('status',), (
            (enums.AutoapplyStatusEnum.SAVED.name,),
            (enums.AutoapplyStatusEnum.FINISHED.name,),
            (enums.AutoapplyStatusEnum.STOPPED.name,),
    ))
    def test_stop_not_in_progress_autoapply_fails(
            self, status, job_seeker_autoapply, job_seeker_client):
        autoapply_inst = Autoapply.objects.get(id=job_seeker_autoapply['id'])
        autoapply_inst.status = status
        autoapply_inst.save()
        resp = api_requests.stop_autoapply(
            job_seeker_client,
            job_seeker_autoapply['id']
        )
        emsg = constants.IMPOSSIBLE_TO_STOP_NOT_IN_PROGRESS_AUTOAPPLY_ERROR
        validators.validate_error_message(resp, emsg)

    def test_stop_not_own_autoapply_fails(
            self, job_seeker_autoapply, job_seeker_2_client):
        resp = api_requests.stop_autoapply(
            job_seeker_2_client, job_seeker_autoapply['id']
        )
        assert resp.status_code == http.HTTPStatus.NOT_FOUND


class TestAutoApplyPermissions:

    @pytest.mark.parametrize(('client', 'status'), (
        (
            'anonym_client',
            http.HTTPStatus.UNAUTHORIZED,
        ),
        (
            'job_seeker_client',
            http.HTTPStatus.CREATED,
        ),
        (
            'company_user_client',
            http.HTTPStatus.FORBIDDEN,
        ),
    ))
    def test_save_autoapply_permissions(
            self, request, client, status, autoapply_base_data):
        client = request.getfixturevalue(client)
        resp = api_requests.save_autoapply(
            client,
            autoapply_base_data)
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
        (
            'job_seeker_2_client',
            http.HTTPStatus.NOT_FOUND,
        )
    ))
    def test_update_autoapply_permissions(
            self, request, client, status, job_seeker_autoapply):
        data = {
            'title': 'New title',
            'query_params': '',
            'stopped_jobs': [],
            'deleted_jobs': [],
            'number': 1
        }
        client = request.getfixturevalue(client)
        resp = api_requests.update_autoapply(
            client,
            job_seeker_autoapply['id'],
            data)
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
        )
    ))
    def test_get_list_autoapplies_permissions(
            self, request, client, status):
        client = request.getfixturevalue(client)
        resp = api_requests.get_autoapplies(client)
        assert resp.status_code == status

    def test_get_list_aoutoapplies_job_seeker_can_see_only_his_autoapplies(
            self, job_seeker_2_client, job_seeker_autoapply):
        resp = api_requests.get_autoapplies(job_seeker_2_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == 0

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
        (
            'job_seeker_2_client',
            http.HTTPStatus.NOT_FOUND,
        )
    ))
    def test_get_autoapply(
            self, request, client, status, job_seeker_autoapply):
        client = request.getfixturevalue(client)
        resp = api_requests.get_autoapply(
            client,
            job_seeker_autoapply['id'])
        assert resp.status_code == status

    @pytest.mark.parametrize(('client', 'status'), (
        (
            'anonym_client',
            http.HTTPStatus.UNAUTHORIZED,
        ),
        (
            'job_seeker_client',
            http.HTTPStatus.NO_CONTENT,
        ),
        (
            'company_user_client',
            http.HTTPStatus.FORBIDDEN,
        ),
        (
            'job_seeker_2_client',
            http.HTTPStatus.NOT_FOUND,
        )
    ))
    def test_delete_autoapply(
            self, request, client, status, job_seeker_autoapply):
        client = request.getfixturevalue(client)
        resp = api_requests.delete_autoapply(
            client,
            job_seeker_autoapply['id'])
        assert resp.status_code == status
