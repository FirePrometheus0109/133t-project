from django.conf.urls import include
from django.urls import path


app_name = 'subscription'


urlpatterns = (
    path('v1/', include('subscription.urls.v1', namespace='api_v1')),
)
