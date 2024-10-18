import http

import pytest

from tests import api_requests


@pytest.fixture
def default_questions(company_user_client):
    resp = api_requests.get_default_questions(company_user_client)
    assert resp.status_code == http.HTTPStatus.OK
    return resp.json()['results']


@pytest.fixture
def saved_question_base_data():
    return {'body': 'Saved Question'}


@pytest.fixture
def saved_question(company_user_client, saved_question_base_data):
    """Saved Question of first company.
    question fields:
        body: Saved Question,
        is_answer_required: False,
        company: id of company,
        is_default: False
    """
    resp = api_requests.create_saved_question(
        company_user_client,
        saved_question_base_data)
    assert resp.status_code == http.HTTPStatus.CREATED
    return resp.json()


@pytest.fixture
def questions_for_survey(saved_question, default_questions):
    return [
            saved_question['id'],
            default_questions[0]['id']
        ]


@pytest.fixture
def survey_from_questions(
        company_user_client, questions_for_survey):
    data = {
        'title': 'Survey from one saved question and one default question',
        'questions': questions_for_survey
    }
    resp = api_requests.create_survey_from_selected_questions(
        company_user_client,
        data)
    assert resp.status_code == http.HTTPStatus.CREATED
    return resp.json()


@pytest.fixture
def questions_data_for_survey():
    return [
        {'body': 'question 1'},
        {'body': 'question 2'},
        {'body': 'question 3'},
        {'body': 'question 4'},
        {'body': 'question 5'},
    ]


@pytest.fixture
def survey(company_user_client, questions_data_for_survey):
    data = {
            'title': 'Survey',
            'questions': questions_data_for_survey
        }
    resp = api_requests.create_survey(company_user_client, data)
    assert resp.status_code == http.HTTPStatus.CREATED
    return resp.json()
