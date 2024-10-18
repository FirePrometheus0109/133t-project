from django.conf.urls import include
from django.urls import path


app_name = 'permission'


urlpatterns = (
    path('v1/', include('permission.urls.v1', namespace='api_v1')),
)
