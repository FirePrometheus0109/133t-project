import json

from django import urls


def get_new_autoapply_jobs_list(client, query_params=None):
    return client.get(
        urls.reverse('apply:api_v1:new-autoapply-job-list'),
            query_params if query_params else {}
    )


def get_autoapply_jobs_list(client, autoapply_id):
    return client.get(
        urls.reverse('apply:api_v1:autoapply-job-list',
                     kwargs={'pk': autoapply_id})
    )


def get_autoapply_job_details(client, job_id):
    return client.get(
        urls.reverse('apply:api_v1:job-detail',
                     kwargs={'pk': job_id})
    )


def save_autoapply(client, data):
    return client.post(
        urls.reverse('apply:api_v1:autoapply-list'),
        data=json.dumps(data),
        content_type='application/json')


def update_autoapply(client, autoapply_id, data):
    return client.put(
        urls.reverse('apply:api_v1:autoapply-detail',
                     kwargs={'pk': autoapply_id}),
        data=json.dumps(data),
        content_type='application/json')


def get_autoapply(client, autoapply_id):
    return client.get(
        urls.reverse('apply:api_v1:autoapply-detail',
                     kwargs={'pk': autoapply_id}),
        content_type='application/json')


def start_autoapply(client, autoapply_id, data):
    return client.put(
        urls.reverse('apply:api_v1:start-autoapply',
                     kwargs={'pk': autoapply_id}),
        data=json.dumps(data),
        content_type='application/json')


def get_applied_jobs(client):
    return client.get(urls.reverse('apply:api_v1:applied-jobs'))


def get_autoapplies(client):
    return client.get(urls.reverse('apply:api_v1:autoapply-list'))


def apply_to_job(client, data):
    return client.post(
        urls.reverse('apply:api_v1:manual-apply'),
        data=json.dumps(data),
        content_type='application/json'
    )


def autoapply_to_job(client, autoapply_id, job_id):
    return client.put(
        urls.reverse(
            'apply:api_v1:autoapply-to-job',
            kwargs={
                'autoapply_pk': autoapply_id,
                'job_pk': job_id,
            }
        )
    )


def delete_autoapply(client, autoapply_id):
    return client.delete(
        urls.reverse(
            'apply:api_v1:autoapply-detail',
            kwargs={'pk': autoapply_id})
    )


def stop_autoapply(client, autoapply_id):
    return client.put(
        urls.reverse('apply:api_v1:stop-autoapply',
                     kwargs={'pk': autoapply_id}))


def reapply_for_job(client, job_id, data={}):
    return client.post(
        urls.reverse(
            'apply:api_v1:reapply',
            kwargs={'job_id': job_id}),
        data=json.dumps(data),
        content_type='application/json')


def get_autoapplies_stats(client):
    return client.get(urls.reverse('apply:api_v1:autoapplies-stats'))
