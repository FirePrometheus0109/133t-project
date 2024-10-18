import json

from django import urls


def get_default_questions(client):
    return client.get(urls.reverse('survey:api_v1:default-questions'))


def create_saved_question(client, data):
    return client.post(
        urls.reverse('survey:api_v1:question-list'),
        data=json.dumps(data),
        content_type='application/json'
    )


def get_saved_questions(client):
    return client.get(urls.reverse('survey:api_v1:question-list'))


def get_saved_question(client, question_id):
    return client.get(
        urls.reverse(
            'survey:api_v1:question-detail',
            kwargs={'pk': question_id}))


def delete_saved_question(client, question_id):
    return client.delete(
        urls.reverse(
            'survey:api_v1:question-detail',
            kwargs={'pk': question_id}))


def edit_saved_question(client, question_id, data):
    return client.patch(
        urls.reverse(
            'survey:api_v1:question-detail',
            kwargs={'pk': question_id}),
        data=json.dumps(data),
        content_type='application/json')


def create_survey(client, data):
    return client.post(
        urls.reverse('survey:api_v1:survey-list'),
        data=json.dumps(data),
        content_type='application/json'
    )


def create_survey_from_selected_questions(client, data):
    return client.post(
        urls.reverse('survey:api_v1:surveys-from-selected-questions'),
        data=json.dumps(data),
        content_type='application/json'
    )


def edit_survey(client, survey_id, data):
    return client.patch(
        urls.reverse(
            'survey:api_v1:survey-detail',
            kwargs={'pk': survey_id}),
        data=json.dumps(data),
        content_type='application/json'
    )


def edit_survey_put(client, survey_id, data):
    return client.put(
        urls.reverse(
            'survey:api_v1:survey-detail',
            kwargs={'pk': survey_id}),
        data=json.dumps(data),
        content_type='application/json'
    )


def add_new_questions_to_survey(client, survey_id, data):
    return client.post(
        urls.reverse(
            'survey:api_v1:survey-questions-list',
            kwargs={'survey_id': survey_id}),
        data=json.dumps(data),
        content_type='application/json'
    )


def add_existing_questions_to_survey(client, survey_id, data):
    return client.post(
        urls.reverse(
            'survey:api_v1:survey-add-existing-questions',
            kwargs={'survey_id': survey_id}),
        data=json.dumps(data),
        content_type='application/json'
    )


def edit_survey_question(client, survey_id, question_id, data):
    return client.patch(
        urls.reverse(
            'survey:api_v1:survey-questions-details',
            kwargs={
                'survey_id': survey_id,
                'pk': question_id
            }),
        data=json.dumps(data),
        content_type='application/json'
    )


def get_survey(client, survey_id):
    return client.get(
        urls.reverse(
            'survey:api_v1:survey-detail',
            kwargs={'pk': survey_id}))


def delete_survey(client, survey_id):
    return client.delete(
        urls.reverse(
            'survey:api_v1:survey-detail',
            kwargs={'pk': survey_id}))


def get_company_servies(client):
    return client.get(urls.reverse('survey:api_v1:survey-list'))


def remove_question_from_survey(client, survey_id, question_id):
    return client.delete(
        urls.reverse(
            'survey:api_v1:survey-questions-details',
            kwargs={
                'survey_id': survey_id,
                'pk': question_id}))


def partial_update_survey_question(client, survey_id, question_id, data):
    return client.patch(
        urls.reverse(
            'survey:api_v1:survey-questions-details',
            kwargs={
                'survey_id': survey_id,
                'pk': question_id}),
            data=json.dumps(data),
            content_type='application/json')


def get_survey_list(client, query_params={}):
    return client.get(urls.reverse('survey:api_v1:survey-list'), query_params)
