from rest_framework import routers

from letter_template import views

app_name = 'api_v1_letter_template'
router = routers.DefaultRouter()
router.register('letter-templates', views.LetterTemplateViewSet)
urlpatterns = router.urls
