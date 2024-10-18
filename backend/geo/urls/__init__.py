from django.conf.urls import include
from django.urls import path


app_name = 'geo'


urlpatterns = (
    path('v1/geo/', include('geo.urls.v1', namespace='api_v1')),
)
