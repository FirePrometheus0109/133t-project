from django import urls


app_name = 'notification_center'


urlpatterns = (
    urls.path(
        'v1/',
        urls.include('notification_center.urls.v1', namespace='api_v1')),
)
