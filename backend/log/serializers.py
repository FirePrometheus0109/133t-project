import json

from rest_framework import serializers

from log import constants
from log import models


class LogSerializer(serializers.ModelSerializer):

    owner = serializers.SerializerMethodField()
    other_info = serializers.SerializerMethodField()

    class Meta:
        model = models.Log
        fields = (
            'id',
            'owner',
            'message',
            'time',
            'other_info'
        )

    @staticmethod
    def get_owner(log):
        if log.type == constants.LogEnum.candidate_apply.name:
            return {}
        return {
            'id': log.owner.id,
            'name': log.owner.get_full_name()
        }

    @staticmethod
    def get_other_info(log):
        if log.other_info:
            return json.loads(log.other_info)
        return {}
