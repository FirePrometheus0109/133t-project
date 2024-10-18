import http

from job_seeker import constants, models
from leet.enums import BanStatusEnum
from tests import api_requests
from tests import utils
from tests import validators


class TestSavedJob:

    def test_no_action_job(
            self, job_seeker_client,
            job_seeker, add_saved_job_data):
        data = add_saved_job_data.copy()
        data.pop('add')
        resp = api_requests.add_remove_to_saved(
            job_seeker_client,
            job_seeker.id,
            data)
        assert resp.status_code == http.HTTPStatus.BAD_REQUEST
        emsg = constants.NO_ACTIONS_FOR_ADDING_TO_SAVED_ERROR
        validators.validate_error_message(resp, emsg)

    def test_two_action_job(
            self, job_seeker_client,
            job_seeker, add_saved_job_data):
        data = add_saved_job_data.copy()
        data['remove'] = True
        resp = api_requests.add_remove_to_saved(
            job_seeker_client,
            job_seeker.id,
            data)
        assert resp.status_code == http.HTTPStatus.BAD_REQUEST
        emsg = constants.TWO_ACTIONS_FOR_ADDING_TO_SAVED_ERROR
        validators.validate_error_message(resp, emsg)

    def test_no_job(
            self, job_seeker_client,
            job_seeker, add_saved_job_data):
        data = add_saved_job_data.copy()
        data.pop('job')
        resp = api_requests.add_remove_to_saved(
            job_seeker_client,
            job_seeker.id,
            data)
        assert resp.status_code == http.HTTPStatus.BAD_REQUEST

    def test_add_job_to_saved_user_is_not_job_seeker(
            self, company_user_client,
            job_seeker, add_saved_job_data):
        resp = api_requests.add_remove_to_saved(
            company_user_client,
            job_seeker.id,
            add_saved_job_data)
        assert resp.status_code == http.HTTPStatus.FORBIDDEN

    def test_add_saved_job_success(
            self, job_seeker_client,
            job_seeker, add_saved_job_data):
        resp = api_requests.add_remove_to_saved(
            job_seeker_client,
            job_seeker.id,
            add_saved_job_data)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['saved_at']

    def test_add_second_time_saved_job_success(
            self, job_seeker_client, job_seeker,
            add_saved_job_data, saved_job):
        resp = api_requests.add_remove_to_saved(
            job_seeker_client,
            job_seeker.id,
            add_saved_job_data)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['saved_at']

    def test_remove_saved_job(
            self, job_seeker_client, job_seeker,
            remove_saved_job_data, saved_job):
        resp = api_requests.add_remove_to_saved(
            job_seeker_client,
            job_seeker.id,
            remove_saved_job_data)
        assert resp.status_code == http.HTTPStatus.NO_CONTENT

    def test_remove_saved_job_no_saved(
            self, job_seeker_client, job_seeker,
            remove_saved_job_data, saved_job):
        resp = api_requests.add_remove_to_saved(
            job_seeker_client,
            job_seeker.id,
            remove_saved_job_data)
        assert resp.status_code == http.HTTPStatus.NO_CONTENT

    def test_view_jobs_with_saveds(
            self, job_seeker_client, job_seeker, job,
            saved_job, company_2_job):
        resp = api_requests.get_job_list(job_seeker_client)
        assert resp.status_code == http.HTTPStatus.OK
        saved = next(
            i for i in resp.json()['results']
            if i['saved_at'])
        assert saved['id'] == job['id']
        not_saved = next(
            i for i in resp.json()['results']
            if not i['saved_at'])
        assert not_saved['id'] == company_2_job['id']

    def test_view_saved_jobs(
            self, job_seeker_client, job_seeker, saved_job):
        resp = api_requests.get_saved_jobs(job_seeker_client, job_seeker.id)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == 1

    def test_view_saved_jobs_no_saved_jobs(
            self, job_seeker_2_client, job_seeker_2, saved_job):
        resp = api_requests.get_saved_jobs(
            job_seeker_2_client, job_seeker_2.id)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == 0

    def test_two_job_seekers_save_job(
            self, job_seeker_client, job_seeker,
            job_seeker_2_client, add_saved_job_data, job_seeker_2):
        job_seekers = (job_seeker, job_seeker_2)
        clients = (job_seeker_client, job_seeker_2_client)
        for js, client in zip(job_seekers, clients):
            resp = api_requests.add_remove_to_saved(
                client,
                js.id,
                add_saved_job_data)
            assert resp.status_code == http.HTTPStatus.OK
        resp = api_requests.get_saved_jobs(job_seeker_client, job_seeker.id)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == 1


class TestBannedJob:

    def test_banned_job_present_in_saved_jobs(
            self, job_seeker_client, job_seeker, job_obj):
        saved_job = models.SavedJob.objects.create(job_seeker=job_seeker,
                                                   job=job_obj)
        resp = api_requests.get_saved_jobs(job_seeker_client, job_seeker.id)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == 1

        utils.ban_entity(saved_job.job)
        assert (models.SavedJob.objects.first().job.ban_status ==
                BanStatusEnum.BANNED.name)
        resp = api_requests.get_saved_jobs(job_seeker_client, job_seeker.id)
        assert resp.status_code == http.HTTPStatus.OK
        resp_data = resp.json()
        assert resp_data['count'] == 1
        assert (resp_data['results'][0]['ban_status'] ==
                BanStatusEnum.BANNED.name)
