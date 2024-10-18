from django.urls import path
from rest_framework import routers

from survey.views import (DefaultQuestionsViewSet, SavedQuestionsViewSet,
                          SurveyAddExistingQuestionsViewSet,
                          SurveyFromSelectedQuestionsViewSet,
                          SurveyQuestionViewSet, SurveyViewSet)

app_name = 'api_v1_survey'
router = routers.SimpleRouter()
router.register(r'saved-question', SavedQuestionsViewSet)
router.register(r'survey', SurveyViewSet)

urlpatterns = router.urls

urlpatterns += [
    path(
        r'default-question/',
        DefaultQuestionsViewSet.as_view({
            'get': 'list'
        }),
        name='default-questions'
    ),
    path(
        r'survey-from-selected/',
        SurveyFromSelectedQuestionsViewSet.as_view({
            'post': 'create'
        }),
        name='surveys-from-selected-questions'
    ),
    path(
        r'survey/<int:survey_id>/question/',
        SurveyQuestionViewSet.as_view({
            'post': 'create',
        }),
        name='survey-questions-list'
    ),
    path(
        r'survey/<int:survey_id>/question/<int:pk>/',
        SurveyQuestionViewSet.as_view({
            'get': 'retrieve',
            'patch': 'partial_update',
            'delete': 'destroy'
        }),
        name='survey-questions-details'
    ),
    path(
        r'survey/<int:survey_id>/existing-questions/',
        SurveyAddExistingQuestionsViewSet.as_view({
            'post': 'create'
        }),
        name='survey-add-existing-questions'
    ),
]
