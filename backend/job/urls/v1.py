from django import urls
from rest_framework import routers

from job import views

app_name = 'api_v1_job'

router = routers.SimpleRouter()
router.register('job', views.JobViewSet, base_name='job')

urlpatterns = [
    urls.path(
        'job/create_dummy/',
        views.DummyJobView.as_view(),
        name='create-dummy'
    ),
    urls.path(
        'job/<int:pk>/viewers/',
        views.JobViewersView.as_view(),
        name='job-viewers'
    ),
    urls.path(
        'job/<int:pk>/restore/',
        views.JobRestoreView.as_view(),
        name='job-restore'
    ),
    urls.path(
        'job/<int:pk>/share/',
        views.JobShareView.as_view(),
        name='job-share'
    ),
    urls.path(
        'job/delete-list/',
        views.JobListSoftDeleteView.as_view(),
        name='job-list-delete'
    ),
    urls.path(
        'job/export-csv/',
        views.JobListCSVExportView.as_view(),
        name='job-export-csv'
    ),
    urls.path(
        'enums/jobs/',
        views.JobActiveEnumView.as_view(),
        name='enums-jobs'
    )
]
urlpatterns += router.urls
