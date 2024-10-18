from django.urls import path

from permission import views

app_name = 'api_v1_permission'

urlpatterns = (
    path(
        'permission-groups/',
        views.PermissionsGroupsView.as_view(),
        name='permission-groups-list'
    ),
    path(
        'initial-permission-groups/',
        views.InitialPermissionsGroupsView.as_view(),
        name='initial-permission-groups-list'
    ),
)
