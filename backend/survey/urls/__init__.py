from django.conf.urls import include
from django.urls import path


app_name = 'survey'


urlpatterns = (
    path('v1/', include('survey.urls.v1', namespace='api_v1')),
)
