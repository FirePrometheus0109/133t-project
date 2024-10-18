# pylint: disable=arguments-differ, no-member
from django import shortcuts
from rest_framework import filters
from rest_framework import mixins
from rest_framework import status
from rest_framework import response
from rest_framework import viewsets

from survey import models
from survey import serializers
from survey import utils
from permission import permissions as base_permissions


class BaseQuestionSurveyView:
    """Base view class for all views in this module.
        Only for internal use.
    """
    permission_classes = (
        base_permissions.BaseModelPermissions,
        base_permissions.HasSubscription
    )

    def get_queryset(self):
        company = self.get_company()
        return self.queryset.filter(company=company)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        company = self.request.user.company_user.company
        context['company'] = company
        return context

    def get_company(self):
        if hasattr(self.request.user, 'company_user'):
            return self.request.user.company_user.company
        return None


class DefaultQuestionsViewSet(BaseQuestionSurveyView,
                              mixins.ListModelMixin,
                              viewsets.GenericViewSet):

    """ViewSet for all default questions in the system.
        list:
            Return list of default questions.
            Default questions are read only.
            Default question can add to Survey
    """

    queryset = (models.Question.objects
                      .select_related('company')
                      .filter(is_default=True).order_by('id'))
    serializer_class = serializers.BaseQuestionSerializer

    def get_queryset(self):
        return self.queryset


class SavedQuestionsViewSet(BaseQuestionSurveyView, viewsets.ModelViewSet):

    """View for company's saved questions.
        list:
            Return list of saved questions.
        create:
            Create new question and add it to saved questions survey.
            Max count of saved questions is 30 per company.
            Example request data:\n
                {
                    "body": "question body",
                    "is_answer_required": true, (optional),
                    "disqualivying_answer": "YES" or "NO", (optional)
                    "add_to_saved_questions": true, (optional)
                }
        retrieve:
            review saved question
        patch:
            update saved question
        destroy:
            delete saved question
    """

    queryset = models.Question.objects.select_related('company').all()
    serializer_class = serializers.SavedQuestionSerializer

    def perform_destroy(self, question):
        """If question added to surveys just set company None."""
        are_surveys_exist = question.surveys.exists()

        if question.company is not None and are_surveys_exist:
            question.company = None
            question.save()
        elif not are_surveys_exist:
            question.delete()


class SurveyViewSet(BaseQuestionSurveyView, viewsets.ModelViewSet):
    """VievSet for working with Surveys.
        list:
            Return list of company surveys.
        create:
            Create new survey with questions.
            Example request data:\n
                {
                    'title': 'title',
                    'questions': [
                        {
                            "body": "question body",
                            "is_answer_required": true, (optional),
                            "disqualivying_answer": "YES" or "NO", (optional)
                            "add_to_saved_questions": true, (optional)
                        }
                    ]
                }
        partial_update:
            Update survey (only title).
        retrieve:
            Review details of survey.
        destroy:
            Delete a survey.
    """

    queryset = (models.Survey.objects
                      .prefetch_related('questions')
                      .select_related('company')
                      .order_by('created_at'))

    filter_backends = (filters.SearchFilter,)
    search_fields = (
        'title',
    )

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return serializers.SurveyPatchSerializer
        return serializers.SurveySerializer

    def update(self, request, *args, **kwargs):
        if self.action == 'update':
            return self.http_method_not_allowed(request, *args, **kwargs)
        return super().update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        models.Question.objects.filter(
            job__isnull=True,
            is_default=False,
            company__isnull=True,
            surveys=instance).delete()
        super().perform_destroy(instance)


class SurveyFromSelectedQuestionsViewSet(BaseQuestionSurveyView,
                                         mixins.CreateModelMixin,
                                         viewsets.GenericViewSet):

    """ViewSet for creating a survey from selected questions.
        create:
            Create a survey from questions.
            Example request data:\n
                {
                    "title": "title",
                    "questions": [
                        1,
                        2,
                        ...
                    ]
                }
    """

    queryset = (models.Survey.objects
                      .prefetch_related('questions')
                      .select_related('company')
                      .all())
    serializer_class = serializers.SurveyFromSelectedQuestionsSerializer


class SurveyQuestionViewSet(BaseQuestionSurveyView, viewsets.ModelViewSet):

    """ViewSet for deleting question from survey.
        create:
            Create and add new questions to the existing survey.
            Example request data:\n
                [
                    {
                        "body": "question body",
                        "is_answer_required": true, (optional),
                        "disqualivying_answer": "YES" or "NO", (optional)
                        "add_to_saved_questions": true, (optional)
                    }
                ]
        retrieve:
            review question details.
        patch:
            update question data.
        delete:
            delete question from survey.
    """

    def get_queryset(self):
        company = self.get_company()
        survey = shortcuts.get_object_or_404(
            models.Survey,
            pk=self.kwargs.get('survey_id'),
            company=company)
        return models.Question.objects.filter(surveys=survey)

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.SurveyCreateQuestionsSerializer
        return serializers.BaseQuestionSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.kwargs:
            context['survey'] = shortcuts.get_object_or_404(
                models.Survey,
                pk=self.kwargs.get('survey_id'))
        return context

    def perform_destroy(self, question):
        """If question has only one survey
            and question is not in saved questions delete question from system.
        In other wey remove relation between this question and certain survey.
        """
        count_surveys = question.surveys.count()
        company = question.company
        if not question.is_default and count_surveys == 1 and company is None:
            question.delete()
        else:
            question.surveys.remove(self.kwargs.get('survey_id'))
            question.save()


class SurveyAddExistingQuestionsViewSet(BaseQuestionSurveyView,
                                        viewsets.GenericViewSet):

    """View for adding existing questions to existing survey.
        create:
            Add questions to survey.
            Example request data:\n
                {
                    "questions": [1, 2, 3]
                }
    """

    queryset = models.Question.objects.none()
    serializer_class = serializers.SurveyAddExistingQuestionsSerializer

    def get_queryset(self):
        return self.queryset

    def create(self, request, *args, **kwargs):
        survey = shortcuts.get_object_or_404(
            models.Survey,
            pk=self.kwargs.get('survey_id'),
            company=request.user.company_user.company)

        serializer = self.get_serializer(data=request.data)
        serializer.context['survey'] = survey
        serializer.is_valid(raise_exception=True)
        utils.add_questions_to_survey(
            survey,
            serializer.validated_data['questions'])
        resp_data = serializers.BaseQuestionSerializer(
            survey.questions.all(),
            many=True).data
        return response.Response(
            data=resp_data,
            status=status.HTTP_201_CREATED)
