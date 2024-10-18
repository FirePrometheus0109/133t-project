from django.conf.urls import include
from django.urls import path


app_name = 'company'


urlpatterns = (
    path('v1/', include('company.urls.v1', namespace='api_v1')),
)
