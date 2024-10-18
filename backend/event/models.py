from django.conf import settings
from django.db import models

from leet import enums


class Event(models.Model):

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='events'
    )
    company = models.ForeignKey(
        'company.Company',
        on_delete=models.PROTECT,
        related_name='events'
    )
    job = models.ForeignKey(
        'job.Job',
        on_delete=models.PROTECT
    )
    type = models.ForeignKey(
        'leet.EventType',
        on_delete=models.PROTECT,
    )
    location = models.ForeignKey(
        'geo.Address',
        on_delete=models.PROTECT,
    )
    timezone = models.CharField(
        'timezone',
        max_length=255,
        default='UTC'
    )
    subject = models.CharField(max_length=255)
    description = models.TextField(max_length=4000)
    time_from = models.DateTimeField()
    time_to = models.DateTimeField()

    @classmethod
    def get_queryset(cls):
        return (cls.objects
                   .select_related(
                       'owner',
                       'company',
                       'job',
                       'type',
                       'location',
                       'location__city',
                       'location__city__state',
                       'location__zip',
                       'location__country')
                   .prefetch_related(
                       'attendees',
                       'attendees__user'))


class Attendee(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.PROTECT,
        related_name='attendees'
    )
    status = models.CharField(
        max_length=32,
        choices=enums.EventAttendeeStatusEnum.choices,
        default=enums.EventAttendeeStatusEnum.INVITED.name  # noqa
    )

    @classmethod
    def get_queryset(cls):
        return (cls.objects
                   .select_related(
                       'user',
                       'event',
                       'event__company',
                       'event__job',
                       'event__type',
                       'event__location',
                       'event__location__city',
                       'event__location__city__state',
                       'event__location__zip',
                       'event__location__country'))
