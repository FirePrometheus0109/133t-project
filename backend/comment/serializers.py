from rest_framework import serializers

from comment import mixins
from comment import models
from job import models as job_models
from job_seeker import models as js_models


class BaseCommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id',
            'title',
            'comment',
            'user',
            'submit_date'
        )
        read_only_fields = (
            'user',
            'submit_date'
        )

    @staticmethod
    def get_user(obj):
        if obj.user is not None:
            return {
                'id': obj.user.id, 'name': obj.user.get_full_name()
            }
        return obj.user


class JobSeekerCommentSerializer(BaseCommentSerializer):
    class Meta(BaseCommentSerializer.Meta):
        model = models.JobSeekerComment


class CreateJobSeekerCommentSerializer(mixins.CreateCommentSerializerMixin,
                                       JobSeekerCommentSerializer):
    source = serializers.PrimaryKeyRelatedField(
        queryset=js_models.JobSeeker.objects.all(),
        write_only=True)

    class Meta(JobSeekerCommentSerializer.Meta):
        fields = JobSeekerCommentSerializer.Meta.fields + ('source',)


class JobCommentSerializer(BaseCommentSerializer):
    class Meta(BaseCommentSerializer.Meta):
        model = models.JobComment


class CreateJobCommentSerializer(mixins.CreateCommentSerializerMixin,
                                 JobCommentSerializer):
    source = serializers.PrimaryKeyRelatedField(
        queryset=job_models.Job.objects.all(),
        write_only=True)

    class Meta(JobCommentSerializer.Meta):
        fields = JobCommentSerializer.Meta.fields + ('source',)
