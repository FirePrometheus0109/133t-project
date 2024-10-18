from django.urls import path
from rest_framework import routers

from company import views

app_name = 'api_v1_company'
router = routers.SimpleRouter()
router.register(
    'company-user', views.CompanyUserViewSet, base_name='company-user')

urlpatterns = router.urls

urlpatterns += [
    path(
        'company/<int:pk>/',
        views.CompanyRetrieveUpdateAPIView.as_view(),
        name='company'
    ),
    path(
        'company/<int:pk>/photo/',
        views.CompanyPhotoUpdateView.as_view(),
        name='company-photo'
    ),
    path(
        'company-user-restore/',
        views.CompanyUserRestoreView.as_view(),
        name='company-user-restore'
    ),
    path(
        'enums/companies/',
        views.CompanyEnumView.as_view(),
        name='enums-companies'
    ),
    path(
        'viewed-candidates-statuses/',
        views.CandidatesStatusesManagementView.as_view(),
        name='viewed-candidates-statuses'
    ),
    path(
        'enums/company-users/',
        views.CompanyUserEnumView.as_view(),
        name='enums-company-users'
    ),
    path(
        'job-owners/',
        views.JobOwnersView.as_view(),
        name='job-owners'
    ),
]
