from django import urls


def get_job_unauthorized(client, pk):
    return client.get(
        urls.reverse(
            'public-api:api_v1:job-detail',
            kwargs={'pk': pk}))


def get_job_list_unauthorized(client):
    return client.get(urls.reverse('public-api:api_v1:job-list'))


def get_public_company(client, company_id):
    return client.get(
        urls.reverse(
            'public-api:api_v1:company-details',
            kwargs={'pk': company_id}))


def get_companies(client):
    return client.get(urls.reverse('public-api:api_v1:company-list'))


def get_enums(client):
    return client.get(urls.reverse('public_api:api_v1:enums'))


def get_ini_settings(client):
    return client.get(urls.reverse('public_api:api_v1:initial-settings'))


def get_candidate_statuses(client):
    return client.get(urls.reverse('public_api:api_v1:candidate-statuses'))


def get_industries(client, query_params=None):
    if query_params is None:
        query_params = {'limit': 100, 'offset': 0}
    return client.get(
        urls.reverse('public_api:api_v1:industry-list'),
        query_params
    )


def get_job_seeker_public(client, guid):
    return client.get(
        urls.reverse('public_api:api_v1:public-job-seeker',
                     kwargs={'guid': guid}),
    )


def get_shared_job(client, guid):
    return client.get(
        urls.reverse('public_api:api_v1:shared-job-detail',
                     kwargs={'guid': guid}),
    )
