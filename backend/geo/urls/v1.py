from django import urls
from rest_framework import routers

from geo import views

app_name = 'api_v1_geo'
router = routers.DefaultRouter()
router.register('country', views.CountryViewSet)
router.register('city', views.CityViewSet)
router.register('state', views.StateViewSet)
urlpatterns = router.urls

urlpatterns += (
    urls.path(
        'timezones/',
        views.TimezoneViewSet.as_view(),
        name='timezone-list'
    ),
    urls.path(
        'city/<int:pk>/zip/',
        views.ZipViewSet.as_view({'get': 'list'}),
        name='city-zips'
    ),
    urls.path('locations/', views.LocationView.as_view(), name='locations'),
)
