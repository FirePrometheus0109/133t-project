import json

from django import urls


def get_subscription_plans(client):
    return client.get(urls.reverse('subscription:api_v1:plan-list'))


def get_trial_subscription_plans(client):
    return client.get(urls.reverse('subscription:api_v1:trial-plan-list'))


def subscribe_to_trial_plan(client, data):
    return client.post(
        urls.reverse(
            'subscription:api_v1:trial-subscription-create'
        ), data=json.dumps(data), content_type='application/json')


def subscribe(client, data):
    return client.post(
        urls.reverse(
            'subscription:api_v1:subscription-create'
        ), data=json.dumps(data), content_type='application/json')


def get_active_subscription(client):
    return client.get(urls.reverse('subscription:api_v1:subscription-active'))


def create_payment_source(client, data):
    return client.post(
        urls.reverse('subscription:api_v1:billing-information-create'),
        data=json.dumps(data), content_type='application/json'
    )


def subscription_webhook(client, data):
    return client.post(
        urls.reverse('subscription:api_v1:subscription-webhook'),
        data=json.dumps(data), content_type='application/json'
    )


def unsubscribe(client, subscription_id):
    return client.put(
        urls.reverse('subscription:api_v1:unsubscribe',
                     kwargs={'pk': subscription_id}))
