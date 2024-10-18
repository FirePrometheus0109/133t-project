from django.urls import path

from job_seeker import views

app_name = 'api_v1_job_seeker'

urlpatterns = [
    path(
        'job-seeker/',
        views.JobSeekerViewSet.as_view({
            'get': 'list'
        }),
        name='jobseeker-list'
    ),
    path(
        'job-seeker/<int:pk>/',
        views.JobSeekerViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update'
        }),
        name='jobseeker-detail'
    ),
    path(
        'job-seeker/<int:pk>/photo/',
        views.JobSeekerPhotoView.as_view(),
        name='job_seeker_photo'
    ),
    path(
        'job-seeker/<int:job_seeker_id>/job-experience/',
        views.JobExperienceViewSet.as_view({
            'get': 'list',
            'post': 'create'
        }),
        name='job-experience'
    ),
    path(
        'job-seeker/<int:job_seeker_id>/job-experience/<int:pk>/',
        views.JobExperienceViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'delete': 'destroy',
        }),
        name='job-experience-detail'
    ),
    path(
        'job-seeker/<int:job_seeker_id>/educations/',
        views.EducationViewSet.as_view({
            'post': 'create',
            'get': 'list'
        }),
        name='educations'
    ),
    path(
        'job-seeker/<int:job_seeker_id>/educations/<int:pk>/',
        views.EducationViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'delete': 'destroy',
        }),
        name='educations-detail'
    ),
    path(
        'job-seeker/<int:job_seeker_id>/documents/',
        views.DocumentViewSet.as_view({
            'post': 'create',
            'get': 'list'
        }),
        name='document'
    ),
    path(
        'job-seeker/<int:job_seeker_id>/documents/<int:pk>/',
        views.DocumentViewSet.as_view({
            'get': 'retrieve',
            'delete': 'destroy',
        }),
        name='document-detail'
    ),
    path(
        'job-seeker/<int:job_seeker_id>/certifications/',
        views.CertificationViewSet.as_view({
            'post': 'create',
            'get': 'list',
        }),
        name='certifications'
    ),
    path(
        'job-seeker/<int:job_seeker_id>/certifications/<int:pk>/',
        views.CertificationViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'delete': 'destroy',
        }),
        name='certifications-detail'
    ),
    path(
        'job-seeker/<int:pk>/favorites-jobs/',
        views.SavedJobView.as_view(),
        name='saved-jobs-list'
    ),
    path(
        'job-seeker/<int:job_seeker_id>/cover-letter/',
        views.CoverLetterViewSet.as_view({
            'get': 'list',
            'post': 'create'
        }),
        name='cover-letter-list'
    ),
    path(
        'job-seeker/<int:job_seeker_id>/cover-letter/<int:pk>/',
        views.CoverLetterViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'delete': 'destroy',
        }),
        name='cover-letter-detail'
    ),
    path(
        'job-seeker/<int:pk>/purchase/',
        views.JobSeekerProfilePurchaseView.as_view(),
        name='purchase-job-seeker-profile'
    ),
    path(
        'job-seeker/<int:pk>/viewers/',
        views.JobSeekerViewerList.as_view(),
        name='job-seeker-viewers'
    ),
    path(
        'job-seekers/<int:pk>/favorites/',
        views.SavedJobSeekerView.as_view(),
        name='saved-job-seekers'
    ),
]
