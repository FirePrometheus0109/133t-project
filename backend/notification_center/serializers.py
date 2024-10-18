# pylint: disable=abstract-method
from rest_framework import serializers
from notifications import models as dj_notif_models

from notification_center import models


class NotificationTypeManageSerializer(serializers.Serializer):

    notification_types = serializers.PrimaryKeyRelatedField(
        queryset=models.NotificationType.objects.all(),
        many=True
    )


class NotificationFullSerializer(serializers.ModelSerializer):

    data = serializers.SerializerMethodField()

    class Meta:
        model = dj_notif_models.Notification
        fields = (
            'id',
            'data',
            'timestamp'
        )

    @staticmethod
    def get_data(instance):
        return instance.data['data']['full']


class NotificationShortSerializer(NotificationFullSerializer):

    class Meta(NotificationFullSerializer.Meta):
        fields = NotificationFullSerializer.Meta.fields + ('description',)

    @staticmethod
    def get_data(instance):
        return instance.data['data'].get('short')
