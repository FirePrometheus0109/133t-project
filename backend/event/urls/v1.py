from django import urls
from rest_framework import routers

from event import views

app_name = 'api_v1_event'
router = routers.DefaultRouter()
router.register('attendees', views.AttendeeEventStatusViewSet)
router.register('events', views.EventViewSet)
router.register('event-types', views.EventTypeViewSet)

urlpatterns = [
    urls.path(
        'another-events/',
        views.AnotherEventView.as_view(),
        name='another-events'
    )
]

urlpatterns += router.urls
