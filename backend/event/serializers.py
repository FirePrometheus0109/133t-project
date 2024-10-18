import pytz
from django.contrib import auth
from rest_framework import serializers

from event import models
from event import services
from event import validators
from geo import serializers as geo_serializers
from job import models as job_models
from job import serializers as job_serializers
from leet import serializers as base_serializers


User = auth.get_user_model()


class AttendeeChangeStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Attendee
        fields = (
            'status',
        )

    def validate_status(self, status):
        validators.validate_attendee_event_status(self.instance, status)
        return status


class AttendeeSerializer(AttendeeChangeStatusSerializer):

    user = base_serializers.UserEnumSerializer()
    status = serializers.SerializerMethodField()

    class Meta(AttendeeChangeStatusSerializer.Meta):
        fields = AttendeeChangeStatusSerializer.Meta.fields + (
            'id',
            'user',
        )

    @staticmethod
    def get_status(attendee):
        return attendee.get_status_display()


class EventDateTimeBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Event
        fields = (
            'time_from',
            'time_to'
        )

    @staticmethod
    def validate_time_from(time_from):
        validators.validate_event_time(time_from)
        return time_from

    @staticmethod
    def validate_time_to(time_to):
        validators.validate_event_time(time_to)
        return time_to

    def validate(self, attrs):
        validators.validate_event_from_to_time(
            attrs['time_from'],
            attrs['time_to']
        )
        return attrs

    def to_representation(self, event):  # noqa
        ret = super().to_representation(event)
        tz = pytz.timezone(event.timezone)
        ret = self.normalize_time(tz, event, ret)
        return ret

    @staticmethod
    def normalize_time(tz, event, result):
        result['time_from'] = event.time_from.astimezone(tz).isoformat()
        result['time_to'] = event.time_to.astimezone(tz).isoformat()
        return result


class EventDateTimeSerializer(EventDateTimeBaseSerializer):

    def validate(self, attrs):
        attrs = super().validate(attrs)
        validators.validate_timezone_utcoffset_time_utcoffset(
            attrs['timezone'],
            self.initial_data['time_from'],
            self.initial_data['time_to']
        )
        return attrs


class EventBaseSerializer(EventDateTimeSerializer):

    class Meta(EventDateTimeSerializer.Meta):
        fields = EventDateTimeSerializer.Meta.fields + (
            'id',
            'type',
            'subject',
        )

    def to_representation(self, event):
        ret = super().to_representation(event)
        ret['type'] = base_serializers.EventTypeSerializer(event.type).data
        colleagues = event.attendees.select_related('user').filter(
            user__company_user__isnull=False)
        candidates = event.attendees.select_related('user').filter(
            user__company_user__isnull=True)
        ret['colleagues'] = AttendeeSerializer(colleagues, many=True).data
        ret['candidates'] = AttendeeSerializer(candidates, many=True).data
        return ret


class EventListSerializer(EventBaseSerializer):

    attendees = AttendeeSerializer(many=True)

    class Meta(EventBaseSerializer.Meta):
        fields = EventBaseSerializer.Meta.fields + (
            'attendees',
        )

    def to_representation(self, event):  # noqa
        ret = super().to_representation(event)
        query_params = self.context['request'].query_params
        tz_name = query_params.get('tz', event.timezone)
        tz = pytz.timezone(tz_name)
        ret = self.normalize_time(tz, event, ret)
        return ret


class EventOwnerSerializer(base_serializers.UserEnumSerializer):
    company_user = serializers.SerializerMethodField()

    class Meta(base_serializers.UserEnumSerializer.Meta):
        fields = base_serializers.UserEnumSerializer.Meta.fields + (
            'company_user',)

    @staticmethod
    def get_company_user(user):
        return {'id': user.company_user.id}


class EventSerializer(EventBaseSerializer):

    colleagues = serializers.PrimaryKeyRelatedField(
        queryset=(User.objects
                      .filter(company_user__isnull=False)
                      .prefetch_related(
                          'company_user',
                          'company_user__company')),
        many=True,
        write_only=True
    )
    candidates = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(company_user__isnull=True),
        many=True,
        write_only=True
    )
    location = geo_serializers.AddressWithCityTimezoneSerializer()
    job = serializers.PrimaryKeyRelatedField(
        queryset=(job_models.Job
                            .objects
                            .select_related('company')
                            .prefetch_related('candidates'))
    )

    class Meta(EventBaseSerializer.Meta):
        fields = EventBaseSerializer.Meta.fields + (
            'owner',
            'location',
            'timezone',
            'description',
            'colleagues',
            'candidates',
            'job'
        )
        read_only_fields = (
            'owner',
        )

    @staticmethod
    def validate_candidates(candidates):
        validators.validate_count_candidates(candidates)
        return candidates

    @staticmethod
    def validate_colleagues(colleagues):
        validators.validate_count_colleagues(colleagues)
        return colleagues

    def validate_job(self, job):
        validators.validate_job(self.context['company'], job)
        return job

    def validate(self, attrs):
        attrs = super().validate(attrs)
        company = self.context['company']
        job = attrs['job']
        user = (getattr(self.instance, 'owner', None)
                or self.context['request'].user)
        validators.validate_candidates(job, attrs['candidates'])
        validators.validate_colleagues(company, attrs['colleagues'], user)
        return attrs

    def create(self, validated_data):
        company = self.context['company']
        user = self.context['request'].user
        return services.EventNew(validated_data, user, company).create()

    def update(self, instance, validated_data):
        return services.EventExisting(instance, validated_data).update()

    def to_representation(self, event):
        ret = super().to_representation(event)
        ret['job'] = job_serializers.JobEnumSerializer(event.job).data
        ret['owner'] = EventOwnerSerializer(event.owner).data
        return ret


class EventUpdateSerializer(EventSerializer):

    class Meta(EventSerializer.Meta):
        read_only_fields = EventSerializer.Meta.read_only_fields + (
            'subject',
            'job'
        )
