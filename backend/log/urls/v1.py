from rest_framework import routers

from log import views

app_name = 'api_v1_log'
router = routers.DefaultRouter()
router.register('logs', views.LogViewSet)
urlpatterns = router.urls
