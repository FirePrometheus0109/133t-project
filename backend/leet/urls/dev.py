import debug_toolbar
from django.conf.urls import include
from django.urls import path
from rest_framework_swagger.views import get_swagger_view

from leet.urls.base import urlpatterns as base_urlpatterns

swagger_view = get_swagger_view(title='133t API', patterns=base_urlpatterns)

dev_tool_urlpatterns = [
    path('swagger-docs/', swagger_view),
    path('__debug__/', include(debug_toolbar.urls)),
]


urlpatterns = \
    dev_tool_urlpatterns + \
    base_urlpatterns
