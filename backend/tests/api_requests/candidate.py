import json

from django import urls


def get_job_candidates(client, job_id, filters=None):
    return client.get(
        urls.reverse(
            'candidate:api_v1:job-candidates',
            kwargs={'pk': job_id}),
        filters if filters else {})


def get_candidates(client, query_params=None):
    return client.get(
        urls.reverse(
            'candidate:api_v1:candidates'
        ), query_params if query_params else {}
    )


def create_answers_to_questions(client, job_id, data):
    return client.post(
        urls.reverse(
            'candidate:api_v1:answers-for-questions',
            kwargs={'pk': job_id}),
        data=json.dumps(data),
        content_type='application/json')


def get_answers(client, job_id, job_seeker_id):
    return client.get(
        urls.reverse(
            'candidate:api_v1:candidate-answers',
            kwargs={
                'job_id': job_id,
                'job_seeker_id': job_seeker_id
            }
        ))


def assign_candidate_to_job(client, data):
    return client.post(
        urls.reverse('candidate:api_v1:assign-candidate'),
        data=json.dumps(data),
        content_type='application/json')


def get_candidate(client, candidate_id):
    return client.get(
        urls.reverse(
            'candidate:api_v1:candidate-details',
            kwargs={'pk': candidate_id}))


def change_candidate_rating(client, candidate_id, data):
    return client.put(
        urls.reverse(
            'candidate:api_v1:change-candidate-rating',
            kwargs={'pk': candidate_id}),
        data=json.dumps(data),
        content_type='application/json')


def get_candidate_quick_view(client, query_params=None):
    return client.get(
        urls.reverse('candidate:api_v1:candidate-quick-view'),
        query_params if query_params else {})


def update_candidate_status(client, candidate_id, data):
    return client.patch(
        urls.reverse(
            'candidate:api_v1:candidate-status',
            kwargs={'pk': candidate_id}),
        data=json.dumps(data),
        content_type='application/json')


def restore_candidate(client, candidate_id):
    return client.post(
        urls.reverse(
            'candidate:api_v1:candidate-restore',
            kwargs={'pk': candidate_id}))


def get_candidates_workflow_stats(client, query_params=None):
    return client.get(
        urls.reverse('candidate:api_v1:candidates-workflow-stats'),
        query_params if query_params else {})


def company_report(client, company_id, from_date, to_date, basis):
    return client.get(
        urls.reverse(
            'candidate:api_v1:company-report',
            kwargs={'pk': company_id}
        ),
        {
            'from_date': from_date,
            'to_date': to_date,
            'basis': basis})


def get_candidates_activities(client):
    return client.get(urls.reverse('candidate:api_v1:candidates-activities'))


def get_quick_list(client, query_params=None):
    query_params = query_params if query_params is not None else {}
    return client.get(
        urls.reverse('candidate:api_v1:candidates-quick-list'),
        query_params
    )


def get_company_users_activity(client, company_id):
    return client.get(
        urls.reverse('candidate:api_v1:company-users-activity',
                     kwargs={'pk': company_id}),
        content_type='application/json')


def export_candidates_to_csv(client, query_params):
    return client.get(
        urls.reverse('candidate:api_v1:candidate-export-csv'),
        query_params
    )


def get_candidates_enums(client, query_params=None):
    query_params = query_params if query_params is not None else {}
    return client.get(
        urls.reverse('candidate:api_v1:enums-candidates'),
        query_params
    )
