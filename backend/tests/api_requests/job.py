import json

from django import urls


def create_job(client, data):
    return client.post(
        urls.reverse('job:api_v1:job-list'),
        data=json.dumps(data),
        content_type='application/json')


def update_job(client, job_id, data):
    return client.put(
        urls.reverse(
            'job:api_v1:job-detail',
            kwargs={'pk': job_id}),
        data=json.dumps(data),
        content_type='application/json')


def get_job(client, job_id):
    return client.get(
        urls.reverse(
            'job:api_v1:job-detail',
            kwargs={'pk': job_id}))


def get_job_list(client, query_params=None):
    return client.get(
            urls.reverse('job:api_v1:job-list'),
            query_params if query_params else {})


def partial_update_job(client, job_id, data):
    return client.patch(
        urls.reverse(
            'job:api_v1:job-detail',
            kwargs={'pk': job_id}),
        data=json.dumps(data),
        content_type='application/json')


def get_job_viewers(client, job_id):
    return client.get(
        urls.reverse(
            'job:api_v1:job-viewers',
            kwargs={'pk': job_id}))


def delete_job_list(client, data):
    return client.post(
        urls.reverse('job:api_v1:job-list-delete'),
        data=json.dumps(data),
        content_type='application/json'
    )


def restore_job(client, job_id):
    return client.put(
        urls.reverse('job:api_v1:job-restore',
                     kwargs={'pk': job_id})
    )


def delete_job(client, job_id):
    return client.delete(
        urls.reverse('job:api_v1:job-detail',
                     kwargs={'pk': job_id}))


def export_job_list_csv(client, query_params):
    return client.get(
            urls.reverse('job:api_v1:job-export-csv'),
            query_params)


def share_job(client, job_id, data):
    return client.put(
        urls.reverse('job:api_v1:job-share',
                     kwargs={'pk': job_id}),
        data=json.dumps(data),
        content_type='application/json'
    )


def get_job_enums(client):
    return client.get(urls.reverse('job:api_v1:enums-jobs'))
