import copy

import coreapi
import coreschema
from django.conf import settings
from django.db import models as orm
from rest_framework import mixins
from rest_framework import permissions as drf_permissions
from rest_framework import response
from rest_framework import schemas
from rest_framework import views
from rest_framework import viewsets

from event import constants
from event import filters
from event import models
from event import permissions
from event import serializers
from event import services
from event import validators
from leet import models as base_models
from leet import serializers as base_serializers
from notification_center import constants as notif_constants
from notification_center import services as notif_services
from permission import permissions as base_permission


class EventTypeViewSet(mixins.ListModelMixin,
                       viewsets.GenericViewSet):

    """
    list:
        return list of letter templates categories
    """
    queryset = base_models.EventType.objects.all()
    serializer_class = base_serializers.EventTypeSerializer
    permission_classes = (
        base_permission.BaseModelPermissions,
        base_permission.HasSubscription,
    )
    pagination_class = None


class EventViewSet(viewsets.ModelViewSet):

    """
    list:
        Return list of events for certain month, day.
        Can filter by owner and event type.
        If there is no 'date' or 'month' in query parameters return
        events only for certain month.
    retrieve:
        Return event details.
    create:
        Create event.
        NOTE (i.bogretsov) candidates and colleagues should be User model ids.
    update:
        Update event.
    partial_update:
        Not allowed.
    destroy:
        Delete event and send notifications about canceled event.
    """
    http_method_names = [
        'get', 'post', 'put', 'delete', 'head', 'options', 'trace'
    ]

    queryset = models.Event.get_queryset().order_by('time_from', 'time_to')
    permission_classes = (
        drf_permissions.IsAuthenticated,
        permissions.EventPermission,
        base_permission.HasSubscription,
    )
    filterset_class = filters.EventFilterSet
    pagination_class = None
    schema = schemas.AutoSchema(
        manual_fields=[
            coreapi.Field(
                'type',
                required=False,
                location='query',
                schema=coreschema.Integer(),
                description='Filter event by event\'s type. Id'
            ),
            coreapi.Field(
                'day',
                required=False,
                location='query',
                schema=coreschema.String(),
                description='Filter events by certain day. '
                            'For example: day=2019-02-26'
            ),
            coreapi.Field(
                'is_owner',
                required=False,
                location='query',
                schema=coreschema.Boolean(),
                description='If true return events '
                            'which are events of request company user. '
                            'Available true values are: {}. '
                            'Available false values are: {}.'.format(
                                settings.REQUEST_QUERY_PARAMETERS_TRUE_VALUES,
                                settings.REQUEST_QUERY_PARAMETERS_FALSE_VALUE)
            ),
            coreapi.Field(
                'month',
                required=False,
                location='query',
                schema=coreschema.String(),
                description='Filter events by certain month. '
                            'Value of parameter is equal `date`.'
            ),
            coreapi.Field(
                'tz',
                required=False,
                location='query',
                schema=coreschema.String(),
                description='TimeZone name to filter events by local request'
                            'user timezone.'
            ),
        ]
    )

    def list(self, request, *args, **kwargs):
        validators.validate_query_params_for_list_of_events(
            request.query_params)
        return super().list(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == 'list':  # noqa
            return serializers.EventListSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return serializers.EventUpdateSerializer
        return serializers.EventSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['company'] = self.request.user.company_user.company
        return context

    def perform_destroy(self, instance):
        event_copy = copy.deepcopy(instance)
        event_attendees_copy = [
            copy.deepcopy(i) for i in instance.attendees.all()
        ]
        notif_service = notif_services.EventAttendeeNotification(event_copy)
        instance.attendees.all().delete()
        instance.delete()
        for attendee in event_attendees_copy:
            services.patch_user_event_notifications_with_additional_data(
                attendee.user, attendee.event, {'cancelled': True})
            notif_service.notify_attendee(
                attendee,
                notif_constants.EVENT_NOTIF_SUBJECT_PREFIX_CANCELLED
            )

    def filter_queryset(self, queryset):
        company = self.request.user.company_user.company
        queryset = queryset.filter(company=company)
        return super().filter_queryset(queryset)


class AnotherEventView(views.APIView):

    permission_classes = (
        drf_permissions.IsAuthenticated,
        permissions.AnotherEventPermission,
        base_permission.HasSubscription
    )
    schema = schemas.AutoSchema(
        manual_fields=[
            coreapi.Field(
                'id',
                required=False,
                location='query',
                schema=coreschema.Integer(),
                description='current event id, used in case of event update'
            ),
            coreapi.Field(
                'time_from',
                required=True,
                location='query',
                schema=coreschema.String(),
                description=''
            ),
            coreapi.Field(
                'time_to',
                required=True,
                location='query',
                schema=coreschema.String(),
                description=''
            ),
        ]
    )

    def get(self, request, *args, **kwargs):
        """Return message about if there is another event
        at the same time for certain (request) user
        or empty string if there is no.
        Example url with query parameters:\n
        /api/v1/another-events/?time_from=datetime(iso-8601)&time_to=datetime(iso-8601)&id=2  # noqa
        All query parameters are required.
        """
        event_id = request.query_params.get('id')
        serializer = serializers.EventDateTimeBaseSerializer(
            data=request.query_params)
        serializer.is_valid(raise_exception=True)
        time_from = serializer.validated_data['time_from']
        time_to = serializer.validated_data['time_to']
        event = (models.Event
                       .objects
                       .filter(
                           orm.Q(owner=request.user)
                           &
                           (
                               (orm.Q(time_from__range=[time_from, time_to])
                                |
                                orm.Q(time_to__range=[time_from, time_to]))
                               &
                               (~orm.Q(time_from=time_to)
                                & ~orm.Q(time_to=time_from))
                           )
                       ))
        if event_id:
            event = event.exclude(id=event_id)
        msg = ''
        if event.exists():
            msg = constants.ANOTHER_EVENT_AT_THE_SAME_TIME_MESSAGE
        return response.Response(data={'message': msg})


class AttendeeEventStatusViewSet(mixins.UpdateModelMixin,
                                 viewsets.GenericViewSet):

    """
    update:
        Accept or reject event. Send email to event owner about
        Accepted/Rejected event.
        Example JSON request:\n
        ```
            {
                "status": "ACCEPTED"
            }
        ```
    """

    queryset = models.Attendee.get_queryset()
    serializer_class = serializers.AttendeeChangeStatusSerializer
    permission_classes = (
        drf_permissions.IsAuthenticated,
    )

    def update(self, request, *args, **kwargs):
        attendee = self.get_object()
        old_status = attendee.status
        serializer = self.get_serializer(attendee, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        services.patch_user_event_notifications_with_additional_data(
            attendee.user, attendee.event, {'status': attendee.status}
        )
        if old_status != attendee.status:
            notif_service = notif_services.EventOwnerNotification(
                attendee.event,
                attendee
            )
            notif_service.notify_owner()
        return response.Response(data=serializer.data)

    def get_queryset(self):
        return self.queryset.filter(user_id=self.request.user.id)
