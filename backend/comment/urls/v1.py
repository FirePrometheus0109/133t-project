from django.urls import path

from comment.views import JobSeekerCommentViewSet, JobCommentViewSet

app_name = 'api_v1_comment'


urlpatterns = [
    path(
        'job-seeker/<int:pk>/comment/',
        JobSeekerCommentViewSet.as_view({
            'get': 'list'
        }),
        name='job-seeker-comments'
    ),
    path(
        'job-seeker-comment/',
        JobSeekerCommentViewSet.as_view({
            'post': 'create'
        }),
        name='job-seeker-comment-create'
    ),
    path(
        'job-seeker-comment/<int:pk>/',
        JobSeekerCommentViewSet.as_view({
            'get': 'retrieve',
            'patch': 'partial_update',
            'put': 'update',
            'delete': 'destroy',
        }),
        name='job-seeker-comment'
    ),
    path(
        'job/<int:pk>/comment/',
        JobCommentViewSet.as_view({
            'get': 'list'
        }),
        name='job-comments'
    ),
    path(
        'job-comment/',
        JobCommentViewSet.as_view({
            'post': 'create',
        }),
        name='job-comment-create'
    ),
    path(
        'job-comment/<int:pk>/',
        JobCommentViewSet.as_view({
            'get': 'retrieve',
            'patch': 'partial_update',
            'put': 'update',
            'delete': 'destroy',
        }),
        name='job-comment'
    )
]
