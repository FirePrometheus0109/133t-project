import datetime
import http
from unittest import mock

import pytest
from django.utils import timezone

from job_seeker import tasks
from tests import api_requests


class TestViewJobSeeker:

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
    def test_get_job_seeker_view_list(self, job_seeker, request, client,
                                      status, job_seeker_profile_view):
        client = request.getfixturevalue(client)
        resp = api_requests.get_job_seeker_view_list(client, job_seeker.id)
        assert resp.status_code == status

    def test_job_seeker_view_correct_data(
            self, job_seeker, job_seeker_client, company_user,
            job_seeker_2, job_seeker_2_client, company_user_client):
        resp = api_requests.get_job_seeker_view_list(job_seeker_client,
                                                     job_seeker.id)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == 0

        resp = api_requests.get_job_seeker_details(company_user_client,
                                                   job_seeker.id)
        assert resp.status_code == http.HTTPStatus.OK

        resp = api_requests.get_job_seeker_view_list(job_seeker_client,
                                                     job_seeker.id)
        assert resp.status_code == http.HTTPStatus.OK
        resp_data = resp.json()
        assert resp_data['count'] == 1
        assert (resp_data['results'][0]['company']['id'] ==
                company_user.company_id)

    def test_job_seeker_profile_view_unique(
            self, job_seeker_profile_view, company_user_client,
            job_seeker_client, job_seeker):
        resp = api_requests.get_job_seeker_view_list(job_seeker_client,
                                                     job_seeker.id)
        assert resp.status_code == http.HTTPStatus.OK
        view_date = resp.json()['results'][0]['created_at']

        resp = api_requests.get_job_seeker_details(company_user_client,
                                                   job_seeker.id)
        assert resp.status_code == http.HTTPStatus.OK
        resp = api_requests.get_job_seeker_view_list(job_seeker_client,
                                                     job_seeker.id)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['results'][0]['created_at'] == view_date

    def test_job_seeker_view_through_candidate_quick_view(
            self, job_seeker, job_seeker_client, company_user_client,
            candidate, company_user):
        resp = api_requests.get_job_seeker_view_list(job_seeker_client,
                                                     job_seeker.id)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == 0

        resp = api_requests.get_candidate_quick_view(company_user_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['results'][0]['job_seeker']['id'] == job_seeker.id

        resp = api_requests.get_job_seeker_view_list(job_seeker_client,
                                                     job_seeker.id)
        assert resp.status_code == http.HTTPStatus.OK
        resp_data = resp.json()
        assert resp_data['count'] == 1
        assert (resp_data['results'][0]['company']['id'] ==
                company_user.company_id)

    def test_job_seeker_profile_one_view_for_one_company(
            self, job_seeker_profile_view, job_seeker_client,
            company_user_2_client, company_2_user_client,
            job_seeker):
        mockname = 'django.utils.timezone.now'
        mock_date = timezone.now() + datetime.timedelta(days=1)
        # second company user from first company viewed profile
        with mock.patch(mockname, new=lambda: mock_date):
            resp = api_requests.get_job_seeker_details(
                company_user_2_client,
                job_seeker.id)
            assert resp.status_code == http.HTTPStatus.OK
        mock_date += datetime.timedelta(days=1)
        # company user from second company viewed profile
        with mock.patch(mockname, new=lambda: mock_date):
            resp = api_requests.get_job_seeker_details(
                company_2_user_client,
                job_seeker.id)
            assert resp.status_code == http.HTTPStatus.OK

        resp = api_requests.get_job_seeker_view_list(
            job_seeker_client,
            job_seeker.id)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == 2

    def test_send_notifications_for_job_seekers_about_view(
            self, viewed_profiles, mailoutbox, companies_list):
        mailoutbox.clear()
        tasks.send_profile_views.delay()
        len(mailoutbox) == len(viewed_profiles)
        for email in mailoutbox:
            for company in companies_list:
                assert company.name in email.message().as_string()

    def test_send_notifications_job_seeker_unsubscribed(
            self, viewed_profiles, job_seeker_client,
            mailoutbox, job_seeker_2):
        mailoutbox.clear()
        data = {'notification_types': []}
        resp = api_requests.manage_notifications(
            job_seeker_client,
            data)
        assert resp.status_code == http.HTTPStatus.OK
        tasks.send_profile_views.delay()
        assert len(mailoutbox) == 1
        message = mailoutbox[0].message()
        assert job_seeker_2.user.first_name in message.as_string()
        assert job_seeker_2.user.last_name in message.as_string()
