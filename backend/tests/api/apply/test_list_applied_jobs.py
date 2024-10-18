import http

import pytest

from apply.models import Apply
from leet.enums import BanStatusEnum
from tests import api_requests, utils


class TestJobSeekerAppliedJobs:

    @pytest.mark.parametrize(('client', 'status'), (
        (
            'anonym_client',
            http.HTTPStatus.UNAUTHORIZED,
        ),
        (
            'company_user_client',
            http.HTTPStatus.FORBIDDEN,
        )
    ))
    def test_get_applied_jobs_permissions(
            self, request, client, status):
        client = request.getfixturevalue(client)
        resp = api_requests.get_applied_jobs(client)
        assert resp.status_code == status

    @pytest.mark.usefixtures('started_autoapply')
    @pytest.mark.parametrize(('client', 'count'), (
        (
            'job_seeker_client',
            1,
        ),
        (
            'job_seeker_2_client',
            0,
        )
    ))
    def test_get_applied_jobs_user_see_only_self_applies_jobs(
            self, request, client, count, started_autoapply):
        client = request.getfixturevalue(client)
        resp = api_requests.get_applied_jobs(client)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == count


class TestBannedJobAppliedJobList:

    def test_banned_job_present_in_applied_job_list(self, job_seeker_client,
                                                    apply):
        apply_object = Apply.objects.first()

        resp = api_requests.get_applied_jobs(job_seeker_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == 1

        utils.ban_entity(apply_object.job)
        resp = api_requests.get_applied_jobs(job_seeker_client)
        resp_data = resp.json()
        assert resp.status_code == http.HTTPStatus.OK
        assert resp_data['count'] == 1
        assert (resp_data['results'][0]['ban_status'] ==
                BanStatusEnum.BANNED.name)
