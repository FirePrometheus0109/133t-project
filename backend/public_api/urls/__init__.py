from django.conf.urls import include
from django.urls import path

app_name = 'public_api'

urlpatterns = (
    path('v1/public/', include('public_api.urls.v1', namespace='api_v1')),
)
