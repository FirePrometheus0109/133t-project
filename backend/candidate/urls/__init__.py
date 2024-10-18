from django.conf.urls import include
from django.urls import path


app_name = 'candidate'


urlpatterns = (
    path('v1/', include('candidate.urls.v1', namespace='api_v1')),
)
