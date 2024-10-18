from django.urls import path

from public_api import views

app_name = 'api_v1_public_api'

urlpatterns = (
    # urls for obtaining of settings, constants
    path('initial-settings/', views.initial_settings, name='initial-settings'),
    path('enums/', views.enums_view, name='enums'),
    path('industry/', views.IndustryListView.as_view(), name='industry-list'),
    path('skills/', views.SkillListView.as_view(), name='skill-list'),
    # public site urls
    path(
        'company/',
        views.PublicCompanyViewSet.as_view({
            'get': 'list'
        }),
        name='company-list'
    ),
    path(
        'company/<int:pk>/',
        views.PublicCompanyViewSet.as_view({
            'get': 'retrieve'
        }),
        name='company-details'),
    path(
        'job/',
        views.PublicJobViewSet.as_view({
            'get': 'list',
        }),
        name='job-list'
    ),
    path(
        'job/<int:pk>/',
        views.PublicJobViewSet.as_view({
            'get': 'retrieve',
        }),
        name='job-detail'
    ),
    path(
        'shared-job/<uuid:guid>/',
        views.SharedJobView.as_view(),
        name='shared-job-detail'
    ),
    path(
        'candidate-statuses/',
        views.CandidateStatusView.as_view(),
        name='candidate-statuses'
    ),
    path(
        'job-seeker/<uuid:guid>/',
        views.PublicJobSeekerRetrieveView.as_view(),
        name='public-job-seeker'
    )
)
