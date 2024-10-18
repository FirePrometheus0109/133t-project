# pylint: disable=abstract-method
from django import http
from rest_framework import serializers

from apply import constants
from apply import models
from apply import services
from apply import validators
from geo import models as geo_models
from geo import serializers as geo_serializers
from job import models as job_models
from job import serializers as job_serializers
from job_seeker import models as js_models
from leet import enums
from leet import services as base_services


class AutoapplyJobListSerializer(serializers.ModelSerializer):
    location = job_serializers.LocationSerializer()
    matching_percent = serializers.DecimalField(max_digits=5, decimal_places=2)
    all_required_skills_count = serializers.IntegerField()
    matched_required_skills_count = serializers.IntegerField()
    is_clearance_match = serializers.BooleanField()
    is_questionnaire_answered = serializers.BooleanField()
    is_required_skills_match = serializers.BooleanField()
    is_education_match = serializers.BooleanField()
    applied_at = serializers.DateTimeField(required=False)
    apply_job_status = serializers.CharField(required=False)
    is_cover_letter_provided = serializers.BooleanField()

    class Meta:
        model = job_models.Job
        fields = (
            'id',
            'created_at',
            'title',
            'location',
            'position_type',
            'education',
            'clearance',
            'experience',
            'salary_min',
            'salary_max',
            'salary_negotiable',
            'benefits',
            'travel',
            'company',
            'matching_percent',
            'all_required_skills_count',
            'matched_required_skills_count',
            'is_clearance_match',
            'is_questionnaire_answered',
            'is_required_skills_match',
            'is_education_match',
            'applied_at',
            'apply_job_status',
            'is_cover_letter_required',
            'is_cover_letter_provided',
        )

    def to_representation(self, instance):
        if not base_services.is_job_active(instance):
            return base_services.get_inactive_job_representation(instance)
        ret = super().to_representation(instance)
        if instance.salary_negotiable:
            ret.pop('salary_min', None)
            ret.pop('salary_max', None)
        ret['company'] = {'id': instance.company.id,
                          'name': instance.company.name}
        return ret


class AutoapplyJobDetailsSerializer(AutoapplyJobListSerializer):

    required_skills = serializers.SerializerMethodField()
    optional_skills = serializers.SerializerMethodField()

    class Meta(AutoapplyJobListSerializer.Meta):
        fields = AutoapplyJobListSerializer.Meta.fields + (
            'required_skills', 'optional_skills', 'description')

    def get_required_skills(self, job):
        return job_serializers.SkillDetailWithMatchingSerializer(
            job.required_skills, many=True, context=self.context
        ).data

    def get_optional_skills(self, job):
        return job_serializers.SkillDetailWithMatchingSerializer(
            job.optional_skills, many=True, context=self.context
        ).data


class AutoapplySerializer(serializers.ModelSerializer):

    stopped_jobs = serializers.PrimaryKeyRelatedField(
        queryset=job_models.Job.objects.get_published(),
        many=True
    )
    deleted_jobs = serializers.PrimaryKeyRelatedField(
        queryset=job_models.Job.objects.get_published(),
        many=True
    )
    new_jobs_count = serializers.SerializerMethodField(required=False)
    days_to_completion = serializers.SerializerMethodField(required=False)
    location = serializers.SerializerMethodField()

    class Meta:
        model = models.Autoapply
        fields = (
            'id',
            'title',
            'status',
            'query_params',
            'stopped_jobs',
            'deleted_jobs',
            'number',
            'owner',
            'new_jobs_count',
            'days_to_completion',
            'location',
        )
        read_only_fields = (
            'status',
            'owner',
            'new_jobs_count',
            'days_to_completion',
            'location',
        )

    def create(self, validated_data):
        stopped_jobs = validated_data.pop('stopped_jobs', None)
        deleted_jobs = validated_data.pop('deleted_jobs', None)
        validated_data.update({'status': enums.AutoapplyStatusEnum.SAVED.name,  # noqa
                               'owner': self.context['job_seeker']})
        instance = super().create(validated_data)
        self.update_jobs_list(stopped_jobs, deleted_jobs, instance)
        return instance

    def update(self, instance, validated_data):
        stopped_jobs = validated_data.pop('stopped_jobs', None)
        deleted_jobs = validated_data.pop('deleted_jobs', None)
        instance = super().update(instance, validated_data)
        self.update_jobs_list(stopped_jobs, deleted_jobs, instance)
        return instance

    @staticmethod
    def get_days_to_completion(autoapply):
        return services.get_autoapply_days_to_completion(autoapply)

    @staticmethod
    def get_new_jobs_count(autoapply):
        return services.get_autoapply_new_jobs_count(autoapply)

    @staticmethod
    def update_jobs_list(stopped_jobs, deleted_jobs, instance):
        instance.stopped_jobs.clear()
        instance.deleted_jobs.clear()
        if stopped_jobs:
            instance.stopped_jobs.add(*stopped_jobs)
        if deleted_jobs:
            instance.deleted_jobs.add(*deleted_jobs)

    def validate_title(self, title):
        validators.validate_autoapply_title_uniqueness(
            self.context['job_seeker'], title, self.instance)
        return title

    @staticmethod
    def validate_query_params(query_params):
        """
        Front-end send searching query_params as string in request body.
        It is need validation this params.
        """
        validators.validate_auto_apply_query_params(query_params)
        return query_params

    @staticmethod
    def validate_number(number):
        validators.validate_autoapply_jobs_number(number)
        return number

    @staticmethod
    def get_location(instance):
        params = http.QueryDict(query_string=instance.query_params)
        state_id = params.get('state_id')
        city_id = params.get('city_id')
        location = None
        if state_id:
            state = geo_models.State.objects.get(id=state_id)
            location = geo_serializers.StateSerializer(state).data
        if city_id:
            city = geo_models.City.objects.get(id=city_id)
            location = geo_serializers.CitySerializer(city).data
        return location


class StartAutoapplySerializer(serializers.ModelSerializer):

    applied_jobs = serializers.PrimaryKeyRelatedField(
        queryset=job_models.Job.objects.get_published(),
        many=True, write_only=True
    )

    class Meta:
        model = models.Autoapply
        fields = (
            'id',
            'status',
            'applied_jobs',
        )
        read_only_fields = (
            'status',
        )

    def update(self, instance, validated_data):
        if instance.status == enums.AutoapplyStatusEnum.IN_PROGRESS.name:  # noqa
            raise serializers.ValidationError(
                constants.IMPOSSIBLE_TO_START_ALREADY_STARTED_AUTOAPPLY_ERROR
            )
        instance = services.AutoapplyService(
            self.context['job_seeker'], instance).start_autoapply(
            validated_data['applied_jobs']
        )
        return instance

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        autoapply_result = services.AutoapplyService(
            self.context['job_seeker'], instance).get_autoapply_jobs()
        ret.update({
            'applied_jobs': AutoapplyJobListSerializer(
                autoapply_result, many=True
            ).data
        })
        return ret

    def validate_applied_jobs(self, applied_jobs):
        validators.validate_applied_jobs(
            self.context['job_seeker'], applied_jobs)
        return applied_jobs


class ApplySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Apply
        fields = (
            'owner',
            'job',
            'status',
            'applied_at',
            'cover_letter'
        )
        read_only_fields = (
            'owner',
            'status',
            'applied_at',
        )

    def validate_job(self, job):
        validators.validate_job_is_active(job)
        validators.validate_job_is_already_applied(
            job, self.context['job_seeker'])
        return job

    def validate(self, attrs):
        validators.validate_matching_for_manual_apply(
            attrs['job'],
            self.context['job_seeker'],
            attrs.get('cover_letter'))
        return attrs

    def create(self, validated_data):
        job = validated_data['job']
        cover_letter = validated_data.get('cover_letter')
        service = services.ManualApplyService(
            self.context['job_seeker'], job, cover_letter)
        return service.apply_to_job()


class AppliedJobSerializer(job_serializers.JobUnauthorizedSerializer):
    """Serializer for AppliedJobsViewSet.
    Added applied_at timestamp and ban_status for response data"""

    applied_at = serializers.DateTimeField()

    class Meta(job_serializers.JobUnauthorizedSerializer.Meta):
        fields = job_serializers.JobUnauthorizedSerializer.Meta.fields + (
            'applied_at',
            'ban_status'
        )


class AutoapplyListSerializer(serializers.ModelSerializer):

    jobs_count = serializers.SerializerMethodField()
    new_jobs_count = serializers.SerializerMethodField(required=False)
    days_to_completion = serializers.SerializerMethodField(required=False)

    class Meta:
        model = models.Autoapply
        fields = (
            'id',
            'title',
            'status',
            'jobs_count',
            'new_jobs_count',
            'days_to_completion'
        )

    def get_jobs_count(self, autoapply):
        job_seeker = self.context['request'].user.job_seeker
        jobs_qs = services.AutoapplyService(
            job_seeker, autoapply
        ).get_autoapply_jobs()

        return jobs_qs.count()

    @staticmethod
    def get_days_to_completion(autoapply):
        return services.get_autoapply_days_to_completion(autoapply)

    @staticmethod
    def get_new_jobs_count(autoapply):
        return services.get_autoapply_new_jobs_count(autoapply)


class UpdateApplyCoverLetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Apply
        fields = (
            'owner',
            'job',
            'status',
            'cover_letter',
            'autoapply',
        )
        read_only_fields = (
            'owner',
            'status',
            'job',
            'autoapply'
        )


class CoverLetterforReApplySerializer(serializers.Serializer):

    cover_letter = serializers.PrimaryKeyRelatedField(
        queryset=js_models.CoverLetter.objects.all(),
        required=False
    )
