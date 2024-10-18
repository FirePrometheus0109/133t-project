from django import urls


def get_company_logs(client, query_params=None):
    query_params = {} if query_params is None else query_params
    return client.get(urls.reverse('log:api_v1:log-list'), query_params)


def delete_log(client, log_id):
    return client.delete(
        urls.reverse('log:api_v1:log-detail', kwargs={'pk': log_id})
    )
