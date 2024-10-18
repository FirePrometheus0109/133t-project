import mock
from dateutil import relativedelta
from django.conf import settings
from django.utils import timezone

from subscription import tasks


class TestPlanPriceUpdateDeletion:

    def test_price_isnt_updated_before_date_comes(
            self, company, subscription, corporate_package_50_new_price):
        old_price = corporate_package_50_new_price.price
        months_count = settings.MONTHS_COUNT_BEFORE_PLAN_CHANGES_APPLY
        time_before_price_change = (
                timezone.now()
                + relativedelta.relativedelta(months=+months_count - 1,
                                              days=+20)
        )
        with mock.patch('django.utils.timezone.now',
                        new=lambda: time_before_price_change):
            tasks.update_plan_prices.delay()
        corporate_package_50_new_price.refresh_from_db()
        assert corporate_package_50_new_price.new_price
        assert corporate_package_50_new_price.price_apply_date
        assert corporate_package_50_new_price.price == old_price

    def test_plan_prices_update_success(
            self, company, subscription, corporate_package_50_new_price,
            stripe_subscription_list_mock, subscription_retrieve_mock,
            plan_retrieve_mock, create_stripe_plan_mock):
        new_price = corporate_package_50_new_price.new_price
        old_stripe_plan_id = corporate_package_50_new_price.stripe_id
        months_count = settings.MONTHS_COUNT_BEFORE_PLAN_CHANGES_APPLY
        time_after_apply_date = (
                timezone.now()
                + relativedelta.relativedelta(months=+months_count)
        )
        subscription_mock = mock.MagicMock()
        stripe_subscription_list_mock.return_value = {
            'data': [subscription_mock, ], 'has_more': False}
        with mock.patch('django.utils.timezone.now',
                        new=lambda: time_after_apply_date):
            tasks.update_plan_prices.delay()
        corporate_package_50_new_price.refresh_from_db()
        assert corporate_package_50_new_price.price == new_price
        assert not corporate_package_50_new_price.price_apply_date
        assert corporate_package_50_new_price.stripe_id != old_stripe_plan_id
        assert subscription_mock.cancel_at_period_end
        subscription_mock.save.assert_called_once()


