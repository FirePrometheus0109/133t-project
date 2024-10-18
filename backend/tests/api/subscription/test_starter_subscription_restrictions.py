import copy
import http

from django.utils import timezone

from auth import constants as auth_constants
from leet import enums
from tests import api_requests
from tests import constants
from tests import validators


class TestStarterSubscriptionRestrictions:

    def test_create_job_with_schedule_forbidden_for_starter_subscription(
            self, company_user_client, job_base_data, starter_subscription):
        data = copy.deepcopy(job_base_data)
        data['status'] = enums.JobStatusEnum.DELAYED.name
        resp = api_requests.create_job(company_user_client, data)
        assert resp.status_code == http.HTTPStatus.FORBIDDEN

    def test_create_job_with_cover_letter_required_forbidden_for_starter_subscription(
            self, company_user_client, job_base_data, starter_subscription):
        data = copy.deepcopy(job_base_data)
        data['is_cover_letter_required'] = True
        resp = api_requests.create_job(company_user_client, data)
        assert resp.status_code == http.HTTPStatus.FORBIDDEN

    def test_create_job_with_closing_date_forbidden_for_starter_subscription(
            self, company_user_client, job_base_data, starter_subscription):
        data = copy.deepcopy(job_base_data)
        data['closing_date'] = str(timezone.now())
        resp = api_requests.create_job(company_user_client, data)
        assert resp.status_code == http.HTTPStatus.FORBIDDEN

    def test_comment_job_forbidden_for_starter_package(
            self, company_user_client, starter_subscription):
        resp = api_requests.create_job_comment(company_user_client, {})
        assert resp.status_code == http.HTTPStatus.FORBIDDEN

    def test_comment_job_seeker_forbidden_for_starter_package(
            self, company_user_client, starter_subscription):
        resp = api_requests.create_job_seeker_comment(company_user_client, {})
        assert resp.status_code == http.HTTPStatus.FORBIDDEN

    def test_create_company_user_forbidden_for_starter_package(
            self, company_user_client, starter_subscription):
        resp = api_requests.create_company_user(company_user_client, {})
        assert resp.status_code == http.HTTPStatus.FORBIDDEN

    def test_company_users_disabled_after_starter_subscription_starts(
            self, company_user_client, active_company_user,
            starter_subscription, anonym_client):
        resp = api_requests.login(
            anonym_client,
            data={
                'email': active_company_user['user']['email'],
                'password': constants.DEFAULT_PASSWORD
            })
        emsg = auth_constants.DISABLED_BECAUSE_OF_SUBSCRIPTION_LOGIN_ERROR
        validators.validate_error_message(resp, emsg)
