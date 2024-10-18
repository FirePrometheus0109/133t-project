from django.conf.urls import include
from django.urls import path


app_name = 'job_seeker'


urlpatterns = (
    path('v1/', include('job_seeker.urls.v1', namespace='api_v1')),
)
