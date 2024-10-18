from django.conf.urls import include
from django.urls import path


app_name = 'auth'


urlpatterns = (
    path('v1/auth/', include('auth.urls.v1', namespace='api_v1')),
)
