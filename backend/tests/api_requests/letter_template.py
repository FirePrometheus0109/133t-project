import json

from django import urls


def get_letter_templates_list(client, query_params=None):
    query_params = query_params if query_params is not None else {}
    return client.get(
        urls.reverse('letter_template:api_v1:lettertemplate-list'),
        query_params
    )


def create_letter_template(client, data):
    return client.post(
        urls.reverse('letter_template:api_v1:lettertemplate-list'),
        data=json.dumps(data),
        content_type='application/json'
    )


def get_letter_template_details(client, l_template_id):
    return client.get(
        urls.reverse(
            'letter_template:api_v1:lettertemplate-detail',
            kwargs={'pk': l_template_id}
        )
    )


def update_letter_template(client, l_template_id, data):
    return client.put(
        urls.reverse(
            'letter_template:api_v1:lettertemplate-detail',
            kwargs={'pk': l_template_id}
        ),
        data=json.dumps(data),
        content_type='application/json'
    )


def delete_letter_template(client, l_template_id):
    return client.delete(
        urls.reverse(
            'letter_template:api_v1:lettertemplate-detail',
            kwargs={'pk': l_template_id}
        )
    )
