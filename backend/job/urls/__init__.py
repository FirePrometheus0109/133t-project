from django.conf.urls import include
from django.urls import path


app_name = 'job'


urlpatterns = (
    path('v1/', include('job.urls.v1', namespace='api_v1')),
)
