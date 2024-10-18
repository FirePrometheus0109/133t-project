import http

from django.utils import timezone

from subscription import constants
from tests import api_requests, validators
from tests.api.subscription import expected


class TestSubscriptPlanAPIList:
    def test_get_trial_plans_success(
            self, company_user_client_without_subscription,
            subscription_plans):
        resp = api_requests.get_trial_subscription_plans(
            company_user_client_without_subscription)
        assert resp.status_code == http.HTTPStatus.OK
        plans = resp.json()['results']
        not_free_plans_actual_count = subscription_plans.filter(
            price__gt=0
        ).count()
        assert len(plans) == not_free_plans_actual_count
        for plan in plans:
            assert plan == expected.EXPECTED_PLAN_LIST_ITEM
            assert plan['price']

    def test_get_all_plans_success(
            self, company_user_client, subscription_plans,
            corporate_package_50_new_price):
        resp = api_requests.get_subscription_plans(
            company_user_client)
        assert resp.status_code == http.HTTPStatus.OK
        plans = resp.json()['results']
        assert len(plans) == subscription_plans.count()
        for plan in plans:
            assert plan == expected.EXPECTED_PLAN_LIST_ITEM

    def test_get_default_plans_list_when_custom_plan_is_deleted(
            self, company_user_client, subscription_plans,
            custom_subscription, deleted_custom_subscription_plan):
        resp = api_requests.get_subscription_plans(
            company_user_client)
        assert resp.status_code == http.HTTPStatus.OK
        plans = resp.json()['results']
        assert len(plans) == subscription_plans.count()
        for plan in plans:
            assert plan == expected.EXPECTED_PLAN_LIST_ITEM

    def test_plan_list_contains_plan_for_deletion(
            self, company_user_client, subscription_plans,
            deleted_corporate_package_50):
        resp = api_requests.get_subscription_plans(
            company_user_client)
        assert resp.status_code == http.HTTPStatus.OK
        plans = resp.json()['results']
        assert len(plans) == subscription_plans.count()
        plan_for_deletion = next(
            plan for plan in plans
            if plan['id'] == deleted_corporate_package_50.id
        )
        assert plan_for_deletion['deletion_date']


class TestPlanLimitations:
    def test_check_company_report_is_forbidden(
            self, company_user_client, company_user):
        now = timezone.now()
        from_date = now + timezone.timedelta(days=-7)
        plan = company_user.subscription_set.first().plan
        plan.is_reporting_enabled = False
        plan.save()
        resp = api_requests.company_report(
            company_user_client, company_user.company.id,
            from_date, now, 'day')
        emsg = constants.PLAN_HAS_NOT_REPORTING_ERROR
        validators.validate_error_message(
            resp, emsg, error_code=http.HTTPStatus.FORBIDDEN)

    def test_check_company_users_activity_is_forbidden(
            self, company_user_client, company_user):
        plan = company_user.subscription_set.first().plan
        plan.is_reporting_enabled = False
        plan.save()
        resp = api_requests.get_company_users_activity(
            company_user_client, company_user.company.id)
        emsg = constants.PLAN_HAS_NOT_REPORTING_ERROR
        validators.validate_error_message(
            resp, emsg, error_code=http.HTTPStatus.FORBIDDEN)

    def test_cant_invite_more_users_than_limit(
            self, company_user_client, company_user,
            invited_company_user_data):
        plan = company_user.subscription_set.first().plan
        plan.users_number = 1
        plan.save()
        resp = api_requests.create_company_user(
            company_user_client, invited_company_user_data)
        emsg = constants.PLAN_NUMBER_OF_USERS_EXCEEDED_ERROR.format(1)
        validators.validate_error_message(resp, emsg)
