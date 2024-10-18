from django import urls


app_name = 'letter_template'


urlpatterns = (
    urls.path(
        'v1/',
        urls.include('letter_template.urls.v1', namespace='api_v1')),
)
