from django.conf.urls import include
from django.urls import path


app_name = 'apply'


urlpatterns = (
    path('v1/', include('apply.urls.v1', namespace='api_v1')),
)
