import json

from django import urls


def get_notification_types(client):
    return client.get(
        urls.reverse('notification_center:api_v1:notification-types')
    )


def get_user_notifications_types(client):
    return client.get(
        urls.reverse('notification_center:api_v1:user-notification-types')
    )


def manage_notifications(client, data):
    return client.put(
        urls.reverse('notification_center:api_v1:user-notification-types'),
        data=json.dumps(data),
        content_type='application/json')


def get_short_notifications(client):
    return client.get(
        urls.reverse('notification_center:api_v1:short-notifications'))


def get_notifications(client):
    return client.get(
        urls.reverse('notification_center:api_v1:notifications'))
