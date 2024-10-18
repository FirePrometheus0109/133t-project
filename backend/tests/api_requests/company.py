import json

from django import urls


def get_company(client, company_id):
    return client.get(
        urls.reverse('company:api_v1:company', kwargs={'pk': company_id}),
        content_type='application/json')


def update_company(client, company_id, data):
    return client.put(
        urls.reverse('company:api_v1:company', kwargs={'pk': company_id}),
        data=json.dumps(data),
        content_type='application/json')


def partial_update_company(client, company_id, data):
    return client.patch(
        urls.reverse('company:api_v1:company', kwargs={'pk': company_id}),
        data=json.dumps(data),
        content_type='application/json')


def upload_company_photo(client, company_id, data):
    return client.put(
        urls.reverse(
            'company:api_v1:company-photo',
            kwargs={'pk': company_id}),
        data=data,
        format='multipart')


def delete_company_photo(client, company_id, data):
    return client.put(
        urls.reverse(
            'company:api_v1:company-photo',
            kwargs={'pk': company_id}),
        data=json.dumps(data),
        content_type='application/json')


def create_company_user(client, data):
    return client.post(
        urls.reverse(
            'company:api_v1:company-user-list'),
        data=json.dumps(data),
        content_type='application/json')


def get_company_users(client):
    return client.get(
        urls.reverse(
            'company:api_v1:company-user-list'))


def get_company_user(client, company_user_id):
    return client.get(
        urls.reverse(
            'company:api_v1:company-user-detail',
            kwargs={'pk': company_user_id}))


def delete_company_user(client, company_user_id):
    return client.delete(
        urls.reverse(
            'company:api_v1:company-user-detail',
            kwargs={'pk': company_user_id}))


def restore_company_user(client, data):
    return client.post(
        urls.reverse(
            'company:api_v1:company-user-restore'),
        data=json.dumps(data),
        content_type='application/json')


def edit_company_user(client, company_user_id, data):
    return client.put(
        urls.reverse(
            'company:api_v1:company-user-detail',
            kwargs={'pk': company_user_id}),
        data=json.dumps(data),
        content_type='application/json')


def get_enums_companies(client, query_params={}):
    return client.get(
        urls.reverse('company:api_v1:enums-companies'),
        query_params
    )


def manage_viewed_candidate_statuses(client, data):
    return client.post(
        urls.reverse('company:api_v1:viewed-candidates-statuses'),
        data=json.dumps(data),
        content_type='application/json')


def get_company_users_enums(client, query_params=None):
    query_params = query_params if query_params is not None else {}
    return client.get(
        urls.reverse('company:api_v1:enums-company-users'),
        query_params
    )
