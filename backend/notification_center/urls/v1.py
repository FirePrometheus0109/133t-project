from django import urls

from notification_center import views

app_name = 'api_v1_notification_center'

urlpatterns = [
    urls.path(
        'notification-types/',
        views.NotificationTypeView.as_view(),
        name='notification-types'
    ),
    urls.path(
        'user-notification-types/',
        views.UserNotificationTypesView.as_view(),
        name='user-notification-types'
    ),
    urls.path(
        'notifications/short/',
        views.NotificationsShortView.as_view(),
        name='short-notifications'
    ),
    urls.path(
        'notifications/',
        views.NotificationsFullView.as_view(),
        name='notifications'
    )
]
