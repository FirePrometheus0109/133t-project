from django.conf import settings
from rest_framework import generics
from rest_framework import permissions as drf_permissions
from rest_framework import response
from rest_framework import views

from notification_center import models
from notification_center import serializers
from notification_center import permissions
from notification_center import utils


class NotificationTypeView(views.APIView):

    def get(self, request, *args, **kwargs):
        """
        View available notification types grouped by format that can be
        menaged by user.
        Example response JSON:\n
        ```
            {
                "133T Web": [
                    {
                        "id": 2,
                        "name": "Auto apply results notifications"
                    }
                ],
                "Email": [
                    {
                        "id": 1,
                        "name": "Auto apply results notifications"
                    },
                    {
                        "id": 3,
                        "name": "Profile viewes"
                    },
                    {
                        "id": 4,
                        "name": "Invitation received"
                    }
                ]
            }
        ```
        """
        queryset = models.NotificationType.objects.order_by('id')
        queryset = utils.get_notif_types_for_manage(request.user, queryset)
        data = utils.get_grouped_notification_types(queryset)
        return response.Response(data=data)


class UserNotificationTypesView(views.APIView):

    permission_classes = (
        drf_permissions.IsAuthenticated,
        permissions.NotificationTypePermission
    )

    @staticmethod
    def get_user_notification_types(user):
        queryset = user.subscribed_notifications.order_by('id')
        queryset = utils.get_notif_types_for_manage(user, queryset)
        data = utils.get_grouped_notification_types(queryset)
        return response.Response(data=data)

    def get(self, request, *args, **kwargs):
        """View user subscribed notification types.
        Example JSON response:\n
        ```
            {
                "133T Web": [],
                "Email": [
                    {
                        "id": 4,
                        "name": "Invitation received"
                    }
                ]
            }
        ```
        """
        return self.get_user_notification_types(request.user)

    def put(self, request, *args, **kwargs):
        """
        Add/Remove subscribed notification types.
        Example JSON request:\n
        ```
        {
            "notification_types": [1, 2]
        }
        ```
        """
        serializer = serializers.NotificationTypeManageSerializer(
            data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        types_qs = models.NotificationType.objects.order_by('id')
        types = utils.get_notif_types_for_manage(user, types_qs)
        request.user.subscribed_notifications.remove(*types)
        request.user.subscribed_notifications.add(
            *serializer.validated_data['notification_types'])
        return self.get_user_notification_types(user)


class NotificationsShortView(views.APIView):

    permission_classes = (
        drf_permissions.IsAuthenticated,
    )

    def get(self, request, *args, **kwargs):
        """
        View list of short notifications (4 items)
        Example JSON response for job seeker:\n
        ```
        [
            {
                "id": 2,
                "timestamp": "2019-02-05T05:11:02Z",
                "description": "Auto apply clickabletitle: new jobs found",
                "data": {
                    "autoapply": {
                        "id": 1,
                        "title": "title 1"
                    }
                }
            },
            {
                "id": 1,
                "timestamp": "2019-02-05T05:10:02Z",
                "description": "Auto apply clickabletitle: finished execution",
                "data": {
                    "autoapply": {
                        "id": 2,
                        "title": "title 2"
                    }
                }
            }
            ...
        ]
        ```
        Example JSON response for company user:\n
        ```
        [
            {
                "id": 1,
                "data": null,
                "description": "Trial period expires 24th of February. "
                               "You will loose the access to all options. "
                               "Choose a package to continue using the platform.",  # noqa
                "timestamp": "2019-02-05T05:11:02Z",
            }
        ]
        ```
        NOTE: Because auto apply's title in notification should be clickable,
        return data for this (id and title), need to replace `clickabletitle`
        on title with link. The same with link in notifications about
        Plan deletion. `linktodashboard` should be replaced with real link to
        tha dashboard.
        !!!
        Now implemented only auto apply's short notifications for job seeker
        and end of trial for company user.
        !!!
        """

        user = request.user
        verbs = utils.get_subscribed_notif_verbs(user)
        notif_qs = (user
                    .notifications
                    .filter(verb__in=verbs)
                    .unread()
                    .order_by('-timestamp')
                    [:settings.NUMBER_SHORT_NOTIFICATIONS])
        data = self.get_serializer(notif_qs, many=True).data
        if notif_qs.exists():
            last_notif = notif_qs[0]
            (user.notifications
                 .filter(timestamp__lte=last_notif.timestamp)
                 .mark_all_as_read())
        return response.Response(data)

    @staticmethod
    def get_serializer(*args, **kwargs):
        return serializers.NotificationShortSerializer(*args, **kwargs)


class NotificationsFullView(generics.ListAPIView):

    """
    get:
        View notifications on notification page (full version)
        Example JSON response for job seeker:\n
        ```
        {
            "count": 2,
            "next": null,
            "previous": null,
            "results": [
                {
                    "id": 2,
                    "timestamp": "2019-02-05T05:11:02Z",
                    "data": {
                        "autoapply": {
                            "id": 1,
                            "title": "title 1",
                            "description": "Auto apply clickabletitle: new jobs found",  # noqa
                        }
                    }
                },
                {
                    "id": 1,
                    "timestamp": "2019-02-05T05:10:02Z",
                    "data": {
                        "autoapply": {
                            "id": 2,
                            "title": "title 2",
                            "description": "Auto apply clickabletitle: finished execution",  # noqa
                        }
                }
                ...
            ]
        }
        ```
        Example JSON response for company user:\n
        ```
        {
            "count": 1,
            "next": null,
            "previous": null,
            "results": [
                {
                    "id": 1,
                    "data": {
                        "subscription": {
                            "description": "Trial period expires "
                                           "24th of February. "
                                           "You will loose the access "
                                           " to all options. "
                                           "Choose a package to continue "
                                           "using the platform.",
                        }
                    },
                    "timestamp": "2019-02-05T05:11:02Z",
                }
            ]
        }
    """

    permission_classes = (
        drf_permissions.IsAuthenticated,
    )
    serializer_class = serializers.NotificationFullSerializer

    def get_queryset(self):
        user = self.request.user
        verbs = utils.get_subscribed_notif_verbs(user)
        return user.notifications.filter(verb__in=verbs).order_by('-timestamp')
