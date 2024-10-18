import copy
import http

import pytest

from survey import constants
from tests import api_requests
from tests import validators


class TestSurvey:

    def test_create_survey(
            self, company_user_client, questions_data_for_survey):
        data = {
            'title': 'QL1',
            'questions': questions_data_for_survey
        }
        resp = api_requests.create_survey(company_user_client, data)
        assert resp.status_code == http.HTTPStatus.CREATED
        act_questions = sorted(
            resp.json()['questions'], key=lambda i: i['body'])
        exp_questions = questions_data_for_survey
        for act, exp in zip(act_questions, exp_questions):
            assert act['body'] == exp['body']

    def test_create_survey_and_add_question_to_saved(
            self, company_user_client, questions_data_for_survey):
        questions = copy.deepcopy(questions_data_for_survey)
        questions[0]['add_to_saved_questions'] = True
        data = {
                'title': 'Question List',
                'questions': questions
            }
        resp = api_requests.create_survey(company_user_client, data)
        assert resp.status_code == http.HTTPStatus.CREATED

        resp = api_requests.get_saved_questions(company_user_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == 1
        question = resp.json()['results'][0]
        assert question['body'] == data['questions'][0]['body']

    def test_create_survey_from_questions(
            self, company_user_client, questions_for_survey,
            saved_question, default_questions):
        data = {
            'title': 'title',
            'questions': questions_for_survey
        }
        resp = api_requests.create_survey_from_selected_questions(
            company_user_client,
            data)
        assert resp.status_code == http.HTTPStatus.CREATED
        questions_set = {i['body'] for i in resp.json()['questions']}
        expected_set = {saved_question['body'], default_questions[0]['body']}
        assert questions_set == expected_set

    def test_edit_survey_questions(
            self, company_user_client, survey):
        question = next(q for q in survey['questions']
                        if q['body'] == 'question 1')
        data = {
            'body': 'newbody'
        }
        resp = api_requests.edit_survey_question(
            company_user_client,
            survey['id'],
            question['id'],
            data)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['body'] == data['body']

        resp = api_requests.get_survey(company_user_client, survey['id'])
        assert resp.status_code == http.HTTPStatus.OK
        edited_question = next(q for q in resp.json()['questions']
                               if q['id'] == question['id'])
        assert edited_question['body'] == data['body']

    def test_remove_question_from_survey(
            self, company_user_client, survey_from_questions, saved_question):
        resp = api_requests.remove_question_from_survey(
            company_user_client,
            survey_from_questions['id'],
            saved_question['id'])
        assert resp.status_code == http.HTTPStatus.NO_CONTENT
        resp = api_requests.get_survey(
            company_user_client,
            survey_from_questions['id'])
        assert resp.status_code == http.HTTPStatus.OK
        assert len(resp.json()['questions']) == 1
        assert resp.json()['questions'][0]['body'] != saved_question['body']

        resp = api_requests.get_saved_question(
            company_user_client,
            saved_question['id'])
        assert resp.status_code == http.HTTPStatus.OK

    def test_remove_question_from_survey_question_is_not_in_other_surveys(
            self, company_user_client, survey):
        question = survey['questions'][0]
        resp = api_requests.remove_question_from_survey(
            company_user_client,
            survey['id'],
            question['id'])
        assert resp.status_code == http.HTTPStatus.NO_CONTENT

    def test_remove_default_question_from_survey(
            self, company_user_client,
            survey_from_questions, default_questions):
        question = default_questions[0]
        resp = api_requests.remove_question_from_survey(
            company_user_client,
            survey_from_questions['id'],
            question['id'])
        assert resp.status_code == http.HTTPStatus.NO_CONTENT

        resp = api_requests.get_default_questions(company_user_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == len(default_questions)

    def test_update_survey_title(self, company_user_client, survey):
        data = {'title': 'new title'}
        resp = api_requests.edit_survey(
            company_user_client,
            survey['id'],
            data
        )
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['title'] == data['title']

    def test_add_new_questions(self, company_user_client, survey):
        count_questions = len(survey['questions'])
        data = [{'body': 'question1'}]
        resp = api_requests.add_new_questions_to_survey(
            company_user_client,
            survey['id'],
            data)
        assert resp.status_code == http.HTTPStatus.CREATED
        count_questions += 1
        resp = api_requests.get_survey(company_user_client, survey['id'])
        assert resp.status_code == http.HTTPStatus.OK
        assert len(resp.json()['questions']) == count_questions

    def test_add_existing_questions_to_survey(
            self, company_user_client, survey, questions_for_survey):
        resp = api_requests.add_existing_questions_to_survey(
            company_user_client,
            survey['id'],
            {'questions': questions_for_survey})
        assert resp.status_code == http.HTTPStatus.CREATED

        resp = api_requests.get_survey(company_user_client, survey['id'])
        assert resp.status_code == http.HTTPStatus.OK
        expected_count = len(survey['questions']) + len(questions_for_survey)
        assert len(resp.json()['questions']) == expected_count

    def test_update_survey_method_put_not_allowed(
            self, company_user_client, survey):
        data = {
            'title': 'new title',
            'questions': [{'body': 'not_allowed'}]}
        resp = api_requests.edit_survey_put(
            company_user_client,
            survey['id'],
            data
        )
        assert resp.status_code == http.HTTPStatus.METHOD_NOT_ALLOWED

    def test_delete_survey_from_questions(
            self, company_user_client, survey_from_questions):
        resp = api_requests.delete_survey(
            company_user_client,
            survey_from_questions['id'])
        assert resp.status_code == http.HTTPStatus.NO_CONTENT

    def test_delete_survey(self, company_user_client, survey):
        resp = api_requests.delete_survey(
            company_user_client,
            survey['id'])
        assert resp.status_code == http.HTTPStatus.NO_CONTENT

    @pytest.mark.parametrize(('query_params', 'count'), (
        (
            {'search': 'firsttitle'},
            1
        ),
        (
            {'search': 'first'},
            1
        ),
        (
            {'search': 'title'},
            2
        ),
    ))
    def test_search_survey(self, company_user_client, query_params, count):
        titles = ['firsttitle', 'secondtitle']
        for t in titles:
            data = {
                'title': t,
                'questions': []
            }
            resp = api_requests.create_survey(company_user_client, data)
            assert resp.status_code == http.HTTPStatus.CREATED

        resp = api_requests.get_survey_list(
            company_user_client,
            query_params=query_params)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == count


class TestSurveyValidate:

    def test_create_survey_title_not_unique(
            self, company_user_client, survey):
        data = {
            'title': survey['title'],
        }
        resp = api_requests.create_survey(company_user_client, data)
        emsg = constants.NOT_UNIQUE_SURVEY_TITLE
        validators.validate_error_message(resp, emsg, 'title')

    def test_create_survey_more_ten_questions(
            self, company_user_client):
        data = {
            'title': 'QL1',
            'questions': [
                {
                    'body': 'question'
                } for _ in range(11)
            ]
        }
        resp = api_requests.create_survey(company_user_client, data)
        emsg = constants.MAX_COUNT_QUESTIONS_IN_SURVEY_ERROR
        validators.validate_error_message(resp, emsg, 'questions')

    def test_create_survey_max_fifty_question_lists(
            self, company_user_client):

        for i in range(50):
            data = {
                'title': str(i),
                'questions': [
                    {
                        'body': 'question'
                    }
                ]
            }
            resp = api_requests.create_survey(
                company_user_client,
                data)
            assert resp.status_code == http.HTTPStatus.CREATED

        data = {
                'title': 'survey',
                'questions': [
                    {
                        'body': 'question'
                    }
                ]
            }
        resp = api_requests.create_survey(company_user_client, data)
        emsg = constants.MAX_COUNT_SURVEYS_ERROR
        validators.validate_error_message(resp, emsg)

    def test_create_survey_and_add_question_to_saved_max_count(
            self, company_user_client):

        for i in range(30):
            data = {'body': 'question{0}'.format(i)}
            resp = api_requests.create_saved_question(
                company_user_client,
                data)
            assert resp.status_code == http.HTTPStatus.CREATED

        data = {
                'title': 'survey',
                'questions': [
                    {
                        'body': 'question 1',
                        'add_to_saved_questions': True
                    }
                ]
            }

        resp = api_requests.create_survey(company_user_client, data)
        emsg = constants.MAX_COUNT_SAVED_QUESTIONS_ERROR
        validators.validate_error_message(resp, emsg)

    def test_create_survey_from_questions_max_ten_questions(
            self, company_user_client, default_questions):
        data = {
            'title': 'Survey from default questions',
            'questions': [q['id'] for q in default_questions]
        }
        resp = api_requests.create_survey_from_selected_questions(
            company_user_client,
            data)
        emsg = constants.MAX_COUNT_QUESTIONS_IN_SURVEY_ERROR
        validators.validate_error_message(resp, emsg, 'questions')

    def test_edit_default_queston_in_survey(
            self, company_user_client,
            survey_from_questions, default_questions):
        question = default_questions[0]
        data = {'is_answer_required': True}
        resp = api_requests.partial_update_survey_question(
            company_user_client,
            survey_from_questions['id'],
            question['id'],
            data)
        emsg = constants.CAN_NOT_EDIT_DEFAULT_QUESTIONS_ERROR
        validators.validate_error_message(resp, emsg)

    def test_add_new_questions_max_count(self, company_user_client, survey):
        data = [{'body': 'question1'} for _ in range(10)]
        resp = api_requests.add_new_questions_to_survey(
            company_user_client,
            survey['id'],
            data)
        emsg = constants.MAX_COUNT_QUESTIONS_IN_SURVEY_ERROR
        validators.validate_error_message(resp, emsg)

    def test_add_new_questions_and_add_to_saved_questions_max_count(
            self, company_user_client, survey):

        for i in range(30):
            data = {'body': 'question{0}'.format(i)}
            resp = api_requests.create_saved_question(
                company_user_client,
                data)
            assert resp.status_code == http.HTTPStatus.CREATED

        data = [{'body': 'question1', 'add_to_saved_questions': True}]
        resp = api_requests.add_new_questions_to_survey(
            company_user_client,
            survey['id'],
            data)
        emsg = constants.MAX_COUNT_SAVED_QUESTIONS_ERROR
        validators.validate_error_message(resp, emsg)

    def test_add_existing_questions_to_survey_max_count_of_questions(
            self, company_user_client, survey, default_questions):
        resp = api_requests.add_existing_questions_to_survey(
            company_user_client,
            survey['id'],
            {'questions': [i['id'] for i in default_questions]})
        emsg = constants.MAX_COUNT_QUESTIONS_IN_SURVEY_ERROR
        validators.validate_error_message(resp, emsg, 'questions')

    def test_update_survey_title_not_unique(
            self, company_user_client, survey):
        data = {'title': survey['title']}
        resp = api_requests.edit_survey(
            company_user_client,
            survey['id'],
            data
        )
        emsg = constants.NOT_UNIQUE_SURVEY_TITLE
        validators.validate_error_message(resp, emsg, 'title')

    def test_update_survey_questions(self, company_user_client, survey):
        data = {
            'questions': [
                {'body': 'fail'}
            ]
        }
        resp = api_requests.edit_survey(
            company_user_client,
            survey['id'],
            data
        )
        emsg = constants.ONLY_TITLE_CAN_PARTIAL_UPDATE_IN_SURVEY
        validators.validate_error_message(resp, emsg)


class TestSurveyPermissions:

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
    def test_get_surveys(
            self, request, client, status):
        client = request.getfixturevalue(client)
        resp = api_requests.get_company_servies(client)
        assert resp.status_code == status

    def test_get_surveys_only_company_surveys(
            self, company_2_user_client, survey):
        resp = api_requests.get_company_servies(company_2_user_client)
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
    def test_create_survey(
            self, request, client, status):
        client = request.getfixturevalue(client)
        data = {
            'title': 'QL1',
            'questions': [
                {
                    'body': 'question'
                }
            ]
        }
        resp = api_requests.create_survey(client, data)
        assert resp.status_code == status

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
    def test_create_survey_from_questions(
            self, request, client, status,
            company_user_client, questions_for_survey):
        client = request.getfixturevalue(client)
        data = {
            'title': 'title',
            'questions': questions_for_survey
        }
        resp = api_requests.create_survey_from_selected_questions(
            client,
            data)
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
    def test_review_survey(
            self, request, client, status, survey_from_questions):
        client = request.getfixturevalue(client)
        resp = api_requests.get_survey(client, survey_from_questions['id'])
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
    def test_edit_survey(
            self, request, client, status, survey):
        client = request.getfixturevalue(client)
        data = {'title': 'new_title'}
        resp = api_requests.edit_survey(client, survey['id'], data)
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
    def test_delete_survey(
            self, request, client, status, survey):
        client = request.getfixturevalue(client)
        resp = api_requests.delete_survey(client, survey['id'])
        assert resp.status_code == status

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
        ),
        (
            'company_2_user_client',
            http.HTTPStatus.NOT_FOUND
        ),
    ))
    def test_add_existing_questions_to_survey(
            self, request, client, status, survey, questions_for_survey):
        client = request.getfixturevalue(client)
        resp = api_requests.add_existing_questions_to_survey(
            client,
            survey['id'],
            {'questions': questions_for_survey})
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
            http.HTTPStatus.NOT_FOUND
        ),
        (
            'company_2_user_client',
            http.HTTPStatus.NOT_FOUND
        ),
    ))
    def test_edit_survey_question(
            self, request, client, status, survey):
        client = request.getfixturevalue(client)
        data = {
            'body': 'newbody'
        }
        resp = api_requests.edit_survey_question(
            client,
            survey['id'],
            survey['questions'][0]['id'],
            data)
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
            http.HTTPStatus.NOT_FOUND
        ),
        (
            'company_2_user_client',
            http.HTTPStatus.NOT_FOUND
        ),
    ))
    def test_delete_question_from_survey(
            self, request, client, status, survey):
        client = request.getfixturevalue(client)
        resp = api_requests.remove_question_from_survey(
            client,
            survey['id'],
            survey['questions'][0]['id'])
        assert resp.status_code == status
