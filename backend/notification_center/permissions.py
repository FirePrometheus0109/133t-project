from rest_framework import permissions


class NotificationTypePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':
            return request.user.has_perm(
                'notification_center.view_notificationtype')
        if request.method == 'PUT':
            return request.user.has_perm(
                'notification_center.manage_notifications')
        return False
