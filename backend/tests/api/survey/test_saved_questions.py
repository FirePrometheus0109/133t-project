import http

import pytest

from survey import constants
from tests import api_requests
from tests import validators


class TestSavedQuestions:

    def test_create_question(
            self, company_user_client, saved_question_base_data):
        resp = api_requests.create_saved_question(
            company_user_client,
            saved_question_base_data)
        assert resp.status_code == http.HTTPStatus.CREATED
        assert resp.json()['body'] == saved_question_base_data['body']

    def get_saved_questions(self, company_user_client, saved_question):
        resp = api_requests.get_saved_questions(company_user_client)
        assert resp.json()['count'] == 1
        assert resp.json()['results'][0]['body'] == saved_question['body']

    def test_delete_question_from_saved_questions(
            self, company_user_client, saved_question):
        resp = api_requests.delete_saved_question(
            company_user_client,
            saved_question['id'])
        assert resp.status_code == http.HTTPStatus.NO_CONTENT
        resp = api_requests.get_saved_question(
            company_user_client,
            saved_question['id'])
        assert resp.status_code == http.HTTPStatus.NOT_FOUND

    def test_delete_question_from_saved_question_is_in_survey(
            self, company_user_client, survey_from_questions, saved_question):
        resp = api_requests.delete_saved_question(
            company_user_client,
            saved_question['id'])
        assert resp.status_code == http.HTTPStatus.NO_CONTENT

        resp = api_requests.get_survey(
            company_user_client,
            survey_from_questions['id'])
        assert resp.status_code == http.HTTPStatus.OK
        assert len(resp.json()['questions']) == 2
        question = next(i for i in resp.json()['questions']
                        if i['id'] == saved_question['id'])
        assert question['body'] == saved_question['body']

        resp = api_requests.get_saved_question(
            company_user_client,
            saved_question['id'])
        assert resp.status_code == http.HTTPStatus.NOT_FOUND

    def test_edit_saved_question(
            self, company_user_client, saved_question):
        assert not saved_question['is_answer_required']
        data = {'is_answer_required': True}
        resp = api_requests.edit_saved_question(
            company_user_client,
            saved_question['id'],
            data)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['is_answer_required']

    def test_edit_saved_question_question_is_in_survey(
            self, company_user_client, survey_from_questions, saved_question):
        assert not saved_question['is_answer_required']
        resp = api_requests.edit_saved_question(
            company_user_client,
            saved_question['id'],
            {'is_answer_required': True})
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['is_answer_required']

        resp = api_requests.get_survey(
            company_user_client,
            survey_from_questions['id'])
        assert resp.status_code == http.HTTPStatus.OK
        question = next(i for i in resp.json()['questions']
                        if i['id'] == saved_question['id'])
        assert question['is_answer_required']

    def test_create_saved_question_with_disqualifying_answer(
            self, company_user_client, saved_question_base_data):
        data = saved_question_base_data.copy()
        data['disqualifying_answer'] = 'YES'
        resp = api_requests.create_saved_question(
            company_user_client,
            data)
        assert resp.status_code == http.HTTPStatus.CREATED
        assert resp.json()['disqualifying_answer'] == 'YES'


class TestaSavedQuestionsValidate:

    def test_create_max_thirty_questions(
            self, company_user_client, saved_question_base_data):

        for i in range(30):
            data = saved_question_base_data.copy()
            data['body'] += str(i)
            resp = api_requests.create_saved_question(
                company_user_client,
                data)
            assert resp.status_code == http.HTTPStatus.CREATED

        resp = api_requests.create_saved_question(
            company_user_client,
            saved_question_base_data)
        emsg = constants.MAX_COUNT_SAVED_QUESTIONS_ERROR
        validators.validate_error_message(resp, emsg)

    def test_create_saved_question_with_invalid_disqualifying_answers(
            self, company_user_client, saved_question_base_data):
        data = saved_question_base_data.copy()
        data['disqualifying_answer'] = 'Invalid'
        resp = api_requests.create_saved_question(
            company_user_client,
            data)
        emsg = constants.INVALID_DISQUALIFYING_ANSWER
        validators.validate_error_message(
            resp, emsg, 'disqualifying_answer')


class TestSavedQuestionsPermissions:

    @pytest.mark.parametrize(('client', 'status'), (
        (
            'anonym_client',
            http.HTTPStatus.UNAUTHORIZED
        ),
        (
            'company_user_client',
            http.HTTPStatus.OK
        ),
        (
            'job_seeker_client',
            http.HTTPStatus.FORBIDDEN
        )
    ))
    def test_get_saved_questions(
            self, request, client, status):
        client = request.getfixturevalue(client)
        resp = api_requests.get_saved_questions(client)
        assert resp.status_code == status

    def test_get_saved_questions_only_company_questions(
            self, company_2_user_client, saved_question):
        resp = api_requests.get_saved_questions(company_2_user_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == 0
        assert not resp.json()['results']

    @pytest.mark.parametrize(('client', 'status'), (
        (
            'anonym_client',
            http.HTTPStatus.UNAUTHORIZED
        ),
        (
            'company_user_client',
            http.HTTPStatus.CREATED
        ),
        (
            'job_seeker_client',
            http.HTTPStatus.FORBIDDEN
        )
    ))
    def test_create_saved_question(
            self, request, client, status, saved_question_base_data):
        client = request.getfixturevalue(client)
        resp = api_requests.create_saved_question(
            client,
            saved_question_base_data)
        assert resp.status_code == status

    @pytest.mark.parametrize(('client', 'status'), (
        (
            'anonym_client',
            http.HTTPStatus.UNAUTHORIZED
        ),
        (
            'company_user_client',
            http.HTTPStatus.NO_CONTENT
        ),
        (
            'job_seeker_client',
            http.HTTPStatus.FORBIDDEN
        ),
        (
            'company_2_user_client',
            http.HTTPStatus.NOT_FOUND
        ),
    ))
    def test_delete_question(
            self, request, client, status,
            company_user_client, saved_question):
        client = request.getfixturevalue(client)
        resp = api_requests.delete_saved_question(
            client,
            saved_question['id'])
        assert resp.status_code == status

    @pytest.mark.parametrize(('client', 'status'), (
        (
            'anonym_client',
            http.HTTPStatus.UNAUTHORIZED
        ),
        (
            'company_user_client',
            http.HTTPStatus.OK
        ),
        (
            'job_seeker_client',
            http.HTTPStatus.FORBIDDEN
        ),
        (
            'company_2_user_client',
            http.HTTPStatus.NOT_FOUND
        ),
    ))
    def test_edit_question(
            self, request, client, status, company_user_client,
            saved_question_base_data, saved_question):
        client = request.getfixturevalue(client)
        resp = api_requests.edit_saved_question(
            client,
            saved_question['id'],
            saved_question_base_data)
        assert resp.status_code == status
