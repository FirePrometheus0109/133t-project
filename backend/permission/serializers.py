from rest_framework import serializers

from permission import models


class PermissionGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PermissionGroup
        fields = (
            'id',
            'name',
            'title',
            'description'
        )
