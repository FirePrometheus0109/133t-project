# pylint: disable=arguments-differ, abstract-method
from rest_framework import serializers

from survey import models
from survey import utils
from survey import validators


class BaseQuestionSerializer(serializers.ModelSerializer):
    """Base Serializer for questions and surveys."""

    is_saved_question = serializers.SerializerMethodField()

    class Meta:
        model = models.Question
        fields = (
            'id',
            'body',
            'is_answer_required',
            'is_default',
            'disqualifying_answer',
            'answer_type',
            'is_saved_question'
        )
        read_only_fields = (
            'is_default',
            'answer_type',
            'is_saved_question'
        )

    def validate(self, attrs):
        """Default Questions are not changed."""
        validators.validate_can_edit_question(self.instance)
        return attrs

    @staticmethod
    def validate_disqualifying_answer(answer):
        """At present disqualifying answer is only 'Yes', 'No'"""
        validators.validate_disqualifying_answer(answer)
        return answer

    @staticmethod
    def get_is_saved_question(question):
        return question.company is not None


class SavedQuestionSerializer(BaseQuestionSerializer):
    """
    Serializer for saved questions that are not saved in survey.
    This serializer has validation for max count of saved questions.
    Create question with company relation.
    """

    def validate(self, attrs):
        validators.validate_count_of_saved_questions(self.context['company'])
        return attrs

    def create(self, validated_data):
        validated_data['company'] = self.context['company']
        return super().create(validated_data)


class BaseSurveyQuestionsSerializer(BaseQuestionSerializer):
    """
    Extended BaseQuestionSerializer.
    Added field 'add_to_saved_question'.
    This serializer is used if SurveySerializer. If there is in question data
        this flag that means that question should be add to 'saved questions.'
    """

    add_to_saved_questions = serializers.BooleanField(
        default=False,
        write_only=True
    )

    class Meta(BaseQuestionSerializer.Meta):
        fields = (
            BaseQuestionSerializer.Meta.fields + ('add_to_saved_questions',)
        )


class BaseSurveySerializer(serializers.ModelSerializer):
    """Base Survey serializer.
    This serializer Contains default validations and Meta data.
    """

    questions = BaseSurveyQuestionsSerializer(many=True)

    class Meta:
        model = models.Survey
        fields = (
            'id',
            'title',
            'questions',
            'company'
        )
        read_only_fields = ('company',)

    def validate_title(self, title):
        validators.validate_survey_title(self.context['company'], title)
        return title

    @staticmethod
    def validate_questions(questions):
        validators.validate_max_count_of_questions_in_survey(questions)
        return questions


class SurveySerializer(BaseSurveySerializer):
    """Serializer for Survey."""

    def validate(self, attrs):
        company = self.context['company']
        questions = attrs.get('questions', [])

        validators.validate_count_of_surveys(company)
        if questions:
            validators.validate_can_add_questions_to_saved(questions, company)

        return attrs

    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        questions = utils.create_questions(
            questions_data,
            self.context['company'])
        survey = utils.create_survey(
            validated_data,
            self.context['company'])
        utils.add_questions_to_survey(survey, questions)
        return survey


class SurveyFromSelectedQuestionsSerializer(BaseSurveySerializer):
    """Serializer only for creating a survey from selected questions."""

    questions = serializers.PrimaryKeyRelatedField(
        queryset=models.Question.objects.all(),
        many=True
    )

    def create(self, validated_data):
        questions = validated_data.pop('questions')
        survey = utils.create_survey(
            validated_data,
            self.context['company'])
        utils.add_questions_to_survey(survey, questions)
        return survey

    def to_representation(self, survey):
        ret = super().to_representation(survey)
        ret['questions'] = BaseQuestionSerializer(
            survey.questions.all().order_by('id'), many=True).data
        return ret


class SurveyPatchSerializer(BaseSurveySerializer):
    """Serializer for updating survey title."""

    class Meta(BaseSurveySerializer.Meta):
        read_only_fields = ('company', 'questions')

    def validate(self, attrs):
        validators.validate_survey_patch_data(attrs)
        return attrs


class SurveyCreateQuestionsSerializer(serializers.ListSerializer):

    child = BaseSurveyQuestionsSerializer()

    def validate(self, attrs):
        validators.validate_can_add_new_questions_to_survey(
            attrs, self.context['survey'])

        validators.validate_can_add_questions_to_saved(
            attrs, self.context['company'])

        return attrs

    def create(self, validated_data):
        questions = utils.create_questions(
            validated_data,
            self.context['company'])
        survey = self.context['survey']
        utils.add_questions_to_survey(survey, questions)
        return questions


class SurveyAddExistingQuestionsSerializer(serializers.Serializer):

    questions = serializers.PrimaryKeyRelatedField(
        queryset=models.Question.objects.all(),
        many=True
    )

    def validate_questions(self, questions):
        validators.validate_can_add_new_questions_to_survey(
            questions, self.context['survey'])
        return questions


class QuestionEnumSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Question
        fields = (
            'id',
            'body'
        )


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Answer
        fields = (
            'id',
            'yes_no_value'
        )


class JobSeekerJobQuestionsSerializer(QuestionEnumSerializer):

    class Meta(QuestionEnumSerializer.Meta):
        fields = (
            QuestionEnumSerializer.Meta.fields + ('is_answer_required',)
        )
