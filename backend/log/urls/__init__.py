from django import urls


app_name = 'log'


urlpatterns = (
    urls.path('v1/', urls.include('log.urls.v1', namespace='api_v1')),
)
