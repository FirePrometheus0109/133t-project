from django import urls


app_name = 'event'


urlpatterns = (
    urls.path('v1/', urls.include('event.urls.v1', namespace='api_v1')),
)
