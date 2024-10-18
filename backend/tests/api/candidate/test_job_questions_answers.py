import http

import pytest

from candidate import constants
from leet import enums
from tests import api_requests
from tests import validators
from tests.api.candidate import expected


class TestAnswerJobQuestions:

    def test_create_answer_success(
            self, job_with_questions, job_seeker_client,
            answers_base_data):
        resp = api_requests.create_answers_to_questions(
            job_seeker_client,
            job_with_questions['id'],
            answers_base_data)
        assert resp.status_code == http.HTTPStatus.CREATED
        assert resp.json() == expected.EXPECTED_JOB_SEEKER_ANSWERS

    def test_list_answered_questions(
            self, job_seeker_client, job_seeker, job_with_ans_survey):
        resp = api_requests.get_answers(
            job_seeker_client,
            job_with_ans_survey['id'],
            job_seeker.id
        )
        assert resp.status_code == http.HTTPStatus.OK
        assert len(job_with_ans_survey['questions']) == len(resp.json())

    @pytest.mark.usefixtures('apply_with_questionnaire')
    def test_create_answers_if_job_seeker_already_applied_for_the_job(
            self, job_seeker_client, job_with_questions, answers_base_data):
        for i in answers_base_data:
            i['answer']['yes_no_value'] = enums.YesNoAnswerEnum.NO.name
        resp = api_requests.create_answers_to_questions(
            job_seeker_client,
            job_with_questions['id'],
            answers_base_data)
        assert resp.status_code == http.HTTPStatus.CREATED
        for i in resp.json():
            assert i['answer'] == enums.YesNoAnswerEnum.NO.name


class TestAnswerJobQuestionValidate:

    def test_create_answers_no_required_answers(
            self, job_with_questions, answers_base_data,
            job_seeker_client, job_questions):
        answers_base_data[0] = {
            'question': answers_base_data[0]['question'],
            'answer': {}
        }
        resp = api_requests.create_answers_to_questions(
            job_seeker_client,
            job_with_questions['id'],
            answers_base_data)
        assert resp.status_code == http.HTTPStatus.BAD_REQUEST
        errors = resp.json()['errors']
        assert int(errors[0]['question'][0]) == answers_base_data[0]['question']
        emsg = constants.ANSWER_IS_REQUIRED_ON_QUESTION_ERROR.format(
            job_questions[0]['body'])
        assert errors[0]['answer'] == [emsg]

    def test_create_answers_no_questions(
            self, job, job_seeker_client):
        data = [{
            'answer': {'yes_no_value': 'YES'}
        }]
        resp = api_requests.create_answers_to_questions(
            job_seeker_client,
            job['id'],
            data)
        assert resp.status_code == http.HTTPStatus.BAD_REQUEST

    def test_create_answers_no_data(
            self, job, job_seeker_client):
        resp = api_requests.create_answers_to_questions(
            job_seeker_client,
            job['id'],
            {})
        assert resp.status_code == http.HTTPStatus.BAD_REQUEST

    def test_create_answers_answer_value_is_empty_for_required_answer(
            self, job_with_questions, answers_base_data,
            job_seeker_client, job_questions):
        answers_base_data[0] = {
            'question': answers_base_data[0]['question'],
            'answer': {
                'yes_no_value': ''
            }
        }
        resp = api_requests.create_answers_to_questions(
            job_seeker_client,
            job_with_questions['id'],
            answers_base_data)
        assert resp.status_code == http.HTTPStatus.BAD_REQUEST
        errors = resp.json()['errors']
        assert int(errors[0]['question'][0]) == answers_base_data[0]['question']
        emsg = constants.ANSWER_IS_REQUIRED_ON_QUESTION_ERROR.format(
            job_questions[0]['body'])
        assert errors[0]['answer'] == [emsg]

    def test_create_answers_answer_only_yes_no_value(
            self, job_with_questions, answers_base_data,
            job_seeker_client):
        answers_base_data[0] = {
            'question': answers_base_data[0]['question'],
            'answer': {
                'yes_no_value': 'boo'
            }
        }
        resp = api_requests.create_answers_to_questions(
            job_seeker_client,
            job_with_questions['id'],
            answers_base_data)
        assert resp.status_code == http.HTTPStatus.BAD_REQUEST

    @pytest.mark.usefixtures('job_survey_answers')
    def test_add_new_answers_if_not_candidate(
            self, job_with_questions, answers_base_data, job_seeker_client):
        resp = api_requests.create_answers_to_questions(
            job_seeker_client,
            job_with_questions['id'],
            answers_base_data)
        validators.validate_error_message(resp, constants.ANSWERS_CREATE_ERROR)

    def test_create_answers_no_data_answers_and_questions(
            self, job_with_questions, job_seeker_client):
        data = []
        resp = api_requests.create_answers_to_questions(
            job_seeker_client,
            job_with_questions['id'],
            data)
        assert resp.status_code == http.HTTPStatus.BAD_REQUEST
        emsg = constants.INVALID_QUESTIONS_FOR_ANSWERS
        emsg_count = constants.INVALID_COUNT_QUESTIONS_FOR_ANSWERS
        message = [
            emsg.format(job_with_questions['title']),
            emsg_count.format(job_with_questions['title'])]
        validators.validate_error_message(resp, message)


class TestCreateAnswerPermissions:

    @pytest.mark.parametrize(('client', 'status'), (
        (
            'anonym_client',
            http.HTTPStatus.UNAUTHORIZED,
        ),
        (
            'job_seeker_client',
            http.HTTPStatus.CREATED,
        ),
        (
            'company_user_client',
            http.HTTPStatus.FORBIDDEN
        )
    ))
    def test_create_answer(
            self, request, client, status, job_with_questions,
            job_seeker_client, answers_base_data):
        client = request.getfixturevalue(client)
        resp = api_requests.create_answers_to_questions(
            client,
            job_with_questions['id'],
            answers_base_data)
        assert resp.status_code == status


class TestListAnswers:

    @pytest.mark.parametrize(('client', 'exp'), (
        (
            'job_seeker_client',
            expected.EXPECTED_JOB_SEEKER_ANSWERS
        ),
        (
            'company_user_client',
            expected.EXPECTED_JOB_SEEKER_ANSWERS_FOR_COMPANY_USER
        )
    ))
    def test_get_answers(
            self, job_with_questions, request, client, exp,
            job_survey_answers, job_seeker):
        client = request.getfixturevalue(client)
        resp = api_requests.get_answers(
            client,
            job_with_questions['id'],
            job_seeker.id)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json() == exp

    @pytest.mark.parametrize(('client',), (
        (
            'job_seeker_client',
        ),
        (
            'company_user_client',
        )
    ))
    def test_get_answers_no_answers(
            self, job_with_questions, job_seeker, request, client):
        client = request.getfixturevalue(client)
        resp = api_requests.get_answers(
            client,
            job_with_questions['id'],
            job_seeker.id)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json() == []

    def test_get_answers_after_updating_job_questions(
            self, job_with_questions, job_survey_answers, job_seeker,
            job_base_data, company_user_client):
        job_base_data['questions'] = [{'body': 'new'}]
        resp = api_requests.update_job(
            company_user_client,
            job_with_questions['id'],
            job_base_data)
        assert resp.status_code == http.HTTPStatus.OK
        new_questions = resp.json()['questions']
        assert len(new_questions) == 1
        assert (new_questions[0]['body'] ==
                job_base_data['questions'][0]['body'])

        resp = api_requests.get_answers(
            company_user_client,
            job_with_questions['id'],
            job_seeker.id)
        assert resp.status_code == http.HTTPStatus.OK
        assert (resp.json() ==
                expected.EXPECTED_JOB_SEEKER_ANSWERS_FOR_COMPANY_USER)


class TestListAnswersPermissions:

    @pytest.mark.parametrize(('client', 'status'), (
        (
            'anonym_client',
            http.HTTPStatus.UNAUTHORIZED,
        ),
        (
            'job_seeker_client',
            http.HTTPStatus.OK,
        ),
        (
            'company_user_client',
            http.HTTPStatus.OK
        )
    ))
    def test_get_answers(
            self, job_with_questions, request, client, status,
            job_survey_answers, job_seeker):
        client = request.getfixturevalue(client)
        resp = api_requests.get_answers(
            client,
            job_with_questions['id'],
            job_seeker.id)
        assert resp.status_code == status

    def test_get_answers_job_seeker_is_not_owner(
            self, job_with_questions, job_survey_answers,
            job_seeker_2_client, job_seeker):
        resp = api_requests.get_answers(
            job_seeker_2_client,
            job_with_questions['id'],
            job_seeker.id)
        assert resp.status_code == http.HTTPStatus.FORBIDDEN

    def test_get_answers_other_company_user(
            self, job_with_questions, job_survey_answers,
            company_2_user_client, job_seeker):
        resp = api_requests.get_answers(
            company_2_user_client,
            job_with_questions['id'],
            job_seeker.id)
        assert resp.status_code == http.HTTPStatus.FORBIDDEN
