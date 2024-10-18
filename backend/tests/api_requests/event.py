import json

import pytz
from django.utils import timezone

from django import urls


def get_event_types(client):
    return client.get(urls.reverse('event:api_v1:eventtype-list'))


def create_event(client, data):
    return client.post(
        urls.reverse('event:api_v1:event-list'),
        data=json.dumps(data),
        content_type='application/json'
    )


def get_events(client, query_params=None):
    query_params = query_params if query_params is not None else {}
    if 'tz' not in query_params:
        query_params['tz'] = pytz.UTC,
    if 'month' not in query_params and 'day' not in query_params:
        query_params['month'] = str(timezone.now().date())
    return client.get(
        urls.reverse('event:api_v1:event-list'),
        query_params
    )


def get_event_details(client, event_id):
    return client.get(
        urls.reverse(
            'event:api_v1:event-detail',
            kwargs={'pk': event_id}
        )
    )


def delete_event(client, event_id):
    return client.delete(
        urls.reverse(
            'event:api_v1:event-detail',
            kwargs={'pk': event_id}
        )
    )


def update_event(client, event_id, data):
    return client.put(
        urls.reverse(
            'event:api_v1:event-detail',
            kwargs={'pk': event_id}
        ),
        data=json.dumps(data),
        content_type='application/json'
    )


def change_attendee_status(client, attendee_id, data):
    return client.put(
        urls.reverse(
            'event:api_v1:attendee-detail',
            kwargs={'pk': attendee_id}
        ),
        data=json.dumps(data),
        content_type='application/json'
    )


def check_another_events(client, query_params):
    return client.get(
        urls.reverse('event:api_v1:another-events'),
        query_params
    )
