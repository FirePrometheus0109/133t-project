import json

from django import urls


def update_job_seeker(client, job_seeker_id, data):
    return client.put(
        urls.reverse(
            'job_seeker:api_v1:jobseeker-detail',
            kwargs={'pk': job_seeker_id}),
        data=json.dumps(data),
        content_type='application/json')


def partial_update_job_seeker(client, job_seeker_id, data):
    return client.patch(
        urls.reverse(
            'job_seeker:api_v1:jobseeker-detail',
            kwargs={'pk': job_seeker_id}),
        data=json.dumps(data),
        content_type='application/json')


def upload_photo(client, job_seeker_id, data):
    return client.put(
        urls.reverse(
            'job_seeker:api_v1:job_seeker_photo',
            kwargs={'pk': job_seeker_id}),
        data=data,
        format='multipart')


def delete_photo(client, job_seeker_id, data):
    return client.put(
        urls.reverse(
            'job_seeker:api_v1:job_seeker_photo',
            kwargs={'pk': job_seeker_id}),
        data=json.dumps(data),
        content_type='application/json')


def get_job_seeker_details(client, job_seeker_id):
    return client.get(
        urls.reverse(
            'job_seeker:api_v1:jobseeker-detail',
            kwargs={'pk': job_seeker_id}))


def get_job_seekers(client, query_params=None):
    query_params = query_params if query_params is not None else {}
    return client.get(
        urls.reverse('job_seeker:api_v1:jobseeker-list'),
        query_params)


def get_job_experience(client, job_seeker_id):
    return client.get(
        urls.reverse(
            'job_seeker:api_v1:job-experience',
            kwargs={'job_seeker_id': job_seeker_id})
    )


def get_job_experience_details(client, job_seeker_id, pk):
    return client.get(
        urls.reverse(
            'job_seeker:api_v1:job-experience-detail',
            kwargs={
                'job_seeker_id': job_seeker_id,
                'pk': pk
            }
        ))


def delete_job_experience(client, job_seeker_id, pk):
    return client.delete(
        urls.reverse(
            'job_seeker:api_v1:job-experience-detail',
            kwargs={
                'job_seeker_id': job_seeker_id,
                'pk': pk
            }
        ))


def add_job_experience(client, job_seeker_id, data):
    return client.post(
        urls.reverse(
            'job_seeker:api_v1:job-experience',
            kwargs={'job_seeker_id': job_seeker_id}),
        data=json.dumps(data),
        content_type='application/json')


def update_job_experience(client, job_seeker_id, pk, data):
    return client.put(
        urls.reverse(
            'job_seeker:api_v1:job-experience-detail',
            kwargs={
                'job_seeker_id': job_seeker_id,
                'pk': pk
            }
        ),
        data=json.dumps(data),
        content_type='application/json')


def get_document(client, job_seeker_id):
    return client.get(
        urls.reverse(
            'job_seeker:api_v1:document',
            kwargs={'job_seeker_id': job_seeker_id})
    )


def get_document_details(client, job_seeker_id, pk):
    return client.get(
        urls.reverse(
            'job_seeker:api_v1:document-detail',
            kwargs={
                'job_seeker_id': job_seeker_id,
                'pk': pk
            }
        ))


def delete_document(client, job_seeker_id, pk):
    return client.delete(
        urls.reverse(
            'job_seeker:api_v1:document-detail',
            kwargs={
                'job_seeker_id': job_seeker_id,
                'pk': pk
            }
        ))


def add_document(client, job_seeker_id, data):
    return client.post(
        urls.reverse(
            'job_seeker:api_v1:document',
            kwargs={'job_seeker_id': job_seeker_id}),
        data=data,
        format='multipart')


def get_education_detail(client, job_seeker_id, pk):
    return client.get(
        urls.reverse(
            'job_seeker:api_v1:educations-detail',
            kwargs={
                'job_seeker_id': job_seeker_id,
                'pk': pk
            }
        ))


def add_education(client, job_seeker_id, data):
    return client.post(
        urls.reverse(
            'job_seeker:api_v1:educations',
            kwargs={'job_seeker_id': job_seeker_id}),
        data=json.dumps(data),
        content_type='application/json')


def update_education(client, job_seeker_id, pk, data):
    return client.put(
        urls.reverse(
            'job_seeker:api_v1:educations-detail',
            kwargs={
                'job_seeker_id': job_seeker_id,
                'pk': pk
            }
        ),
        data=json.dumps(data),
        content_type='application/json')


def delete_education(client, job_seeker_id, pk):
    return client.delete(
        urls.reverse(
            'job_seeker:api_v1:educations-detail',
            kwargs={
                'job_seeker_id': job_seeker_id,
                'pk': pk
            }
        ))


def delete_certification(client, job_seeker_id, pk):
    return client.delete(
        urls.reverse(
            'job_seeker:api_v1:certifications-detail',
            kwargs={
                'job_seeker_id': job_seeker_id,
                'pk': pk
            }
        ))


def get_certification_detail(client, job_seeker_id, pk):
    return client.get(
        urls.reverse(
            'job_seeker:api_v1:certifications-detail',
            kwargs={
                'job_seeker_id': job_seeker_id,
                'pk': pk
            }
        ))


def add_certification(client, job_seeker_id, data):
    return client.post(
        urls.reverse(
            'job_seeker:api_v1:certifications',
            kwargs={'job_seeker_id': job_seeker_id}),
        data=json.dumps(data),
        content_type='application/json')


def update_certification(client, job_seeker_id, pk, data):
    return client.put(
        urls.reverse(
            'job_seeker:api_v1:certifications-detail',
            kwargs={
                'job_seeker_id': job_seeker_id,
                'pk': pk
            }
        ),
        data=json.dumps(data),
        content_type='application/json')


def get_educations(client, job_seeker_id):
    return client.get(
        urls.reverse(
            'job_seeker:api_v1:educations',
            kwargs={'job_seeker_id': job_seeker_id}))


def get_certifications(client, job_seeker_id):
    return client.get(
        urls.reverse(
            'job_seeker:api_v1:certifications',
            kwargs={'job_seeker_id': job_seeker_id}))


def add_remove_to_saved(client, job_seeker_id, data):
    return client.post(
        urls.reverse(
            'job_seeker:api_v1:saved-jobs-list',
            kwargs={'pk': job_seeker_id}),
        data=json.dumps(data),
        content_type='application/json')


def get_saved_jobs(client, job_seeker_id):
    return client.get(
        urls.reverse(
            'job_seeker:api_v1:saved-jobs-list',
            kwargs={'pk': job_seeker_id}))


def delete_job_seeker_profile(client, job_seeker_id):
    return client.delete(
        urls.reverse(
            'job_seeker:api_v1:jobseeker-detail',
            kwargs={'pk': job_seeker_id}))


def create_cover_letter(client, job_seeker_id, data):
    return client.post(
        urls.reverse(
            'job_seeker:api_v1:cover-letter-list',
            kwargs={'job_seeker_id': job_seeker_id}
        ),
        data=json.dumps(data),
        content_type='application/json'
    )


def get_cover_letters(client, job_seeker_id):
    return client.get(
        urls.reverse(
            'job_seeker:api_v1:cover-letter-list',
            kwargs={
                'job_seeker_id': job_seeker_id,
            }
        ))


def get_cover_letter(client, job_seeker_id, pk):
    return client.get(
        urls.reverse(
            'job_seeker:api_v1:cover-letter-detail',
            kwargs={
                'job_seeker_id': job_seeker_id,
                'pk': pk
            }
        ))


def update_cover_letter(client, job_seeker_id, pk, data):
    return client.put(
        urls.reverse(
            'job_seeker:api_v1:cover-letter-detail',
            kwargs={
                'job_seeker_id': job_seeker_id,
                'pk': pk
            }
        ),
        data=json.dumps(data),
        content_type='application/json'
    )


def delete_cover_letter(client, job_seeker_id, pk):
    return client.delete(
        urls.reverse(
            'job_seeker:api_v1:cover-letter-detail',
            kwargs={
                'job_seeker_id': job_seeker_id,
                'pk': pk
            }
        ),
    )


def purchase_job_seeker(client, job_seeker_id):
    return client.put(
        urls.reverse(
            'job_seeker:api_v1:purchase-job-seeker-profile',
            kwargs={'pk': job_seeker_id}))


def get_purchased_job_seekers(client):
    return client.get(
        urls.reverse('job_seeker:api_v1:purchased-job-seeker-list'))


def get_job_seeker_view_list(client, job_seeker_id, query_params=None):
    return client.get(
        urls.reverse(
            'job_seeker:api_v1:job-seeker-viewers',
            kwargs={'pk': job_seeker_id}
        ),
        query_params if query_params else {})


def get_saved_job_seekers(client, company_user_id):
    return client.get(
        urls.reverse(
            'job_seeker:api_v1:saved-job-seeker',
            kwargs={'pk': company_user_id}))


def save_remove_job_seeker(client, job_seeker_id, data):
    return client.post(
        urls.reverse(
            'job_seeker:api_v1:saved-job-seekers',
            kwargs={'pk': job_seeker_id}),
        data=json.dumps(data),
        content_type='application/json')
