from json import dumps as json_dumps

from rest_framework import serializers

from company import models as company_models


class PublicCompanyListSerializer(serializers.ModelSerializer):
    job_count = serializers.SerializerMethodField()

    class Meta:
        model = company_models.Company
        fields = (
            'id',
            'name',
            'job_count'
        )

    @staticmethod
    def get_job_count(company):
        return company.jobs.count()


class VersionSerializer(serializers.Serializer):
    version = serializers.CharField()
    date = serializers.DateField()
    changelog = serializers.SerializerMethodField()

    @staticmethod
    def get_changelog(version):
        result = '{}'
        try:
            result = json_dumps(version['changelog'])
        except TypeError:
            pass
        return result

    def update(self, instance, validated_data):
        raise NotImplementedError('`update()` not allowed.')

    def create(self, validated_data):
        raise NotImplementedError('`create()` not allowed.')
