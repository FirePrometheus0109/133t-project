from rest_framework import serializers

from survey import constants
from leet import enums


def validate_can_add_questions_to_saved(questions, company):
    """Validator for adding survey's questions to saved questions."""

    cnt_saved = 0
    for i in questions:
        if i['add_to_saved_questions']:
            cnt_saved += 1
    cnt_copmany_saved = company.saved_questions.all().count()
    cnt_total = cnt_saved + cnt_copmany_saved
    if cnt_total > constants.MAX_COUNT_SAVED_QUESTIONS:
        raise serializers.ValidationError(
            constants.MAX_COUNT_SAVED_QUESTIONS_ERROR)


def validate_can_add_new_questions_to_survey(questions, survey):
    """Validator for adding questions to existing survey."""
    cnt_survey_questions = survey.questions.all().count()
    total_cnt = len(questions) + cnt_survey_questions
    if total_cnt > constants.MAX_COUNT_QUESTIONS_IN_SURVEY:
        raise serializers.ValidationError(
            constants.MAX_COUNT_QUESTIONS_IN_SURVEY_ERROR)


def validate_can_edit_question(question):
    """User can not validate default questions."""
    if question is not None and question.is_default:
        raise serializers.ValidationError(
            constants.CAN_NOT_EDIT_DEFAULT_QUESTIONS_ERROR)


def validate_disqualifying_answer(answer):
    """At present disqualifying answer is only 'Yes', 'No'"""
    if (answer and answer != enums.YesNoAnswerEnum.YES.name  # noqa
            and answer != enums.YesNoAnswerEnum.NO.name):  # noqa
        raise serializers.ValidationError(
            constants.INVALID_DISQUALIFYING_ANSWER)


def validate_count_of_saved_questions(company):
    """Comapny can have only 30 saved questions."""
    count = company.saved_questions.all().count()
    if count >= constants.MAX_COUNT_SAVED_QUESTIONS:
        raise serializers.ValidationError(
            constants.MAX_COUNT_SAVED_QUESTIONS_ERROR)


def validate_survey_title(company, title):
    """Title of survey should be unique in company."""
    if company.surveys.filter(title=title).exists():
        raise serializers.ValidationError(constants.NOT_UNIQUE_SURVEY_TITLE)


def validate_max_count_of_questions_in_survey(questions):
    """Survey can have only 10 questions."""
    if len(questions) > constants.MAX_COUNT_QUESTIONS_IN_SURVEY:
        raise serializers.ValidationError(
            constants.MAX_COUNT_QUESTIONS_IN_SURVEY_ERROR)


def validate_count_of_surveys(company):
    """User can not create new survey if company has 50 surveys."""
    count = company.surveys.all().count()
    if count >= constants.MAX_COUNT_SURVEYS:
        raise serializers.ValidationError(constants.MAX_COUNT_SURVEYS_ERROR)


def validate_survey_patch_data(data):
    if 'questions' in data:
        raise serializers.ValidationError(
            constants.ONLY_TITLE_CAN_PARTIAL_UPDATE_IN_SURVEY)


def validate_required_answers(question, answer, emsg):
    """If question has mark 'is_answer_required'
        user should answer for question."""
    if question.is_answer_required:
        if not answer or not answer.get('yes_no_value', ''):
            error = {
                'question': question.id,
                'answer': emsg
            }
            raise serializers.ValidationError(error)
