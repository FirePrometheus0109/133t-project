import json

from django import urls


def create_job_seeker_comment(client, data):
    return _base_create_comment(client, data, 'job-seeker-comment-create')


def get_job_seeker_comment(client, comment_id):
    return _base_get_comment(client, comment_id, 'job-seeker-comment')


def update_job_seeker_comment(client, comment_id, data):
    return _base_update_comment(client, comment_id, data, 'job-seeker-comment')


def partial_update_job_seeker_comment(client, comment_id, data):
    return _base_partial_update__comment(client, comment_id, data,
                                         'job-seeker-comment')


def delete_job_seeker_comment(client, comment_id):
    return _base_delete_comment(client, comment_id, 'job-seeker-comment')


def get_job_seeker_comment_list(client, job_seeker_id):
    return _base_get_comment_list(client, job_seeker_id, 'job-seeker-comments')


def create_job_comment(client, data):
    return _base_create_comment(client, data, 'job-comment-create')


def get_job_comment(client, comment_id):
    return _base_get_comment(client, comment_id, 'job-comment')


def update_job_comment(client, comment_id, data):
    return _base_update_comment(client, comment_id, data, 'job-comment')


def partial_update_job_comment(client, comment_id, data):
    return _base_partial_update__comment(client, comment_id, data,
                                         'job-comment')


def delete_job_comment(client, comment_id):
    return _base_delete_comment(client, comment_id, 'job-comment')


def get_job_comment_list(client, job_id):
    return _base_get_comment_list(client, job_id, 'job-comments')


def _base_create_comment(client, data, url_name):
    return client.post(
        urls.reverse(f'comment:api_v1:{url_name}'),
        data=json.dumps(data),
        content_type='application/json')


def _base_get_comment(client, comment_id, url_name):
    return client.get(
        urls.reverse(
            f'comment:api_v1:{url_name}',
            kwargs={'pk': comment_id}))


def _base_update_comment(client, comment_id, data, url_name):
    return client.put(
        urls.reverse(f'comment:api_v1:{url_name}',
                     kwargs={'pk': comment_id}),
        data=json.dumps(data),
        content_type='application/json')


def _base_partial_update__comment(client, comment_id, data, url_name):
    return client.patch(
        urls.reverse(
            f'comment:api_v1:{url_name}',
            kwargs={'pk': comment_id}),
        data=json.dumps(data),
        content_type='application/json')


def _base_delete_comment(client, comment_id, url_name):
    return client.delete(
        urls.reverse(
            f'comment:api_v1:{url_name}',
            kwargs={'pk': comment_id}))


def _base_get_comment_list(client, source_id, url_name):
    return client.get(
        urls.reverse(
            f'comment:api_v1:{url_name}',
            kwargs={'pk': source_id}))
