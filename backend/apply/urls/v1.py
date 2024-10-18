from django.urls import path
from rest_framework import routers


from apply import views

app_name = 'api_v1_apply'

router = routers.SimpleRouter()
router.register('autoapply', views.AutoapplyModelViewSet,
                base_name='autoapply')

urlpatterns = [
    path(
        'apply/',
        views.ApplyCreateView.as_view(),
        name='manual-apply'
    ),
    path(
        'autoapply/job/',
        views.AutoapplyJobList.as_view(),
        name='new-autoapply-job-list'
    ),
    path(
        'autoapply/<int:pk>/job/',
        views.AutoapplyJobList.as_view(),
        name='autoapply-job-list'
    ),
    path(
        'autoapply/<int:autoapply_pk>/job/<int:job_pk>/apply/',
        views.AutoapplyToJobView.as_view(),
        name='autoapply-to-job'
    ),
    path(
        'autoapply/<int:autoapply_pk>/job/<int:job_pk>/cover-letter/',
        views.ApplyCoverLetterUpdateView.as_view(),
        name='set-cover-letter'
    ),
    path(
        'autoapply/job/<int:pk>/',
        views.AutoapplyJobDetails.as_view(),
        name='job-detail'
    ),
    path(
        'autoapply/<int:pk>/start/',
        views.StartAutoapplyView.as_view(),
        name='start-autoapply'
    ),
    path(
        'autoapply/<int:pk>/stop/',
        views.StopAutoapplyView.as_view(),
        name='stop-autoapply'
    ),
    path(
        'autoapply/<int:pk>/restart/',
        views.RestartAutoapplyView.as_view(),
        name='restart-autoapply'
    ),
    path(
        'applied-jobs/',
        views.AppliedJobsView.as_view(),
        name='applied-jobs'
    ),
    path(
        'job/<int:job_id>/reapply/',
        views.ReApplyJobView.as_view(),
        name='reapply'
    ),
    path(
        'autoapplies/stats/',
        views.AutoApplyStatsView.as_view(),
        name='autoapplies-stats'
    )
]

urlpatterns += router.urls
