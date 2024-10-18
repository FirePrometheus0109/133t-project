import http

import stripe
from tests import api_requests
from tests import validators


class TestSetBillingInformationAPI:

    def test_set_billing_information_success(
            self, company_user_client,
            company, customer_retrieve_mock):
        assert not company.customer.is_billing_info_provided
        resp = api_requests.create_payment_source(
            company_user_client, data={
                'token': 'token',
                'email': 'email@mail.com',
                'auto_renew_subscription': True
            }
        )
        assert resp.status_code == http.HTTPStatus.CREATED
        company.refresh_from_db()
        assert company.customer.is_billing_info_provided
        assert company.customer.auto_renew_subscription
        customer_retrieve_mock.return_value.sources.create.assert_called_once_with(
            source='token'
        )
        assert (customer_retrieve_mock.return_value.email
                == 'email@mail.com')
        assert (customer_retrieve_mock.return_value.default_source
                == 'payment_source_id')
        customer_retrieve_mock.return_value.save.assert_called_once()

    def test_set_billing_information_fails_with_invalid_email(
            self, company_user_client, company):
        resp = api_requests.create_payment_source(
            company_user_client, data={
                'token': 'token',
                'email': 'invalid email',
                'auto_renew_subscription': True
            }
        )
        assert resp.status_code == http.HTTPStatus.BAD_REQUEST
        assert resp.json()['field_errors']['email']

    def test_is_billing_info_provided_is_false_if_set_payment_source_fails(
            self, company_user_client, company,
            customer_retrieve_mock):
        customer_retrieve_mock.return_value.sources.create.side_effect = \
            stripe.error.StripeError('Some message')
        resp = api_requests.create_payment_source(
            company_user_client, data={
                'token': 'token',
                'email': 'email@mail.com',
                'auto_renew_subscription': True
            }
        )
        assert resp.status_code == http.HTTPStatus.INTERNAL_SERVER_ERROR
        company.refresh_from_db()
        assert not company.customer.is_billing_info_provided
