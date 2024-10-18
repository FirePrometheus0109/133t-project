from django.conf.urls import include
from django.urls import path


app_name = 'comment'


urlpatterns = (
    path('v1/', include('comment.urls.v1', namespace='api_v1')),
)
