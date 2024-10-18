import copy
import itertools

import pytz

from event import models
from geo import models as geo_models
from leet import constants as base_constants
from leet import enums
from log import constants as log_constants
from log import utils as log_utils
from notification_center import constants as notif_constants
from notification_center import services as notif_services


class EventNew:
    """Create event, assign attendees to event."""

    def __init__(self, validated_data, event_owner, company):
        self.colleagues = validated_data.pop('colleagues')
        self.candidates = validated_data.pop('candidates')
        self.location_data = validated_data.pop('location')
        self.event_data = validated_data
        self.event_owner = event_owner
        self.company = company
        self.event = None

    def add_attendees_to_event(self):
        users = list(itertools.chain(self.colleagues, self.candidates))
        data = [{
            'user': i,
            'event': self.event
        } for i in users]
        # event owner has already accepted.
        for i in data:
            if i['user'] == self.event.owner:
                i['status'] = enums.EventAttendeeStatusEnum.ACCEPTED.name  # noqa
        models.Attendee.objects.bulk_create(models.Attendee(**i) for i in data)

    def notify_attendees(self):
        attendees = self.event.attendees.exclude(user=self.event.owner)
        notif_service = notif_services.EventAttendeeNotification(self.event)
        prefix = notif_constants.EVENT_NOTIF_SUBJECT_PREFIX_INVITED
        for attendee in attendees:
            notif_service.notify_attendee(attendee, prefix)

    def create(self):
        location = geo_models.Address.objects.create(**self.location_data)
        self.event = models.Event.objects.create(
            owner=self.event_owner,
            location=location,
            company=self.company,
            **self.event_data
        )
        self.add_attendees_to_event()
        self.notify_attendees()
        self._create_company_user_log()
        return self.event

    def _create_company_user_log(self):
        if self.event.type.name == base_constants.EVENT_TYPES_SCREENING_NAME:
            log = log_constants.LogEnum.schedule_screening
        else:
            log = log_constants.LogEnum.schedule_interview
        tz = pytz.timezone(self.event.timezone)
        time_from = self.event.time_from.astimezone(tz)
        log_name = log.name
        log_message = log.value.format(time_from, self.event.job.title)
        for candidate in self.candidates:
            log_utils.create_log(
                self.event.owner, log_name, log_message, candidate.job_seeker
            )


class EventExisting:

    def __init__(self, event, validated_data):
        self.colleagues = validated_data.pop('colleagues')
        self.candidates = validated_data.pop('candidates')
        self.location_data = validated_data.pop('location')
        validated_data.pop('job', None)
        validated_data.pop('subject', None)
        self.event_data = validated_data
        self.event = event
        self.attendees_to_notify = []
        self.is_changed = False

    def _update(self, instance, data):
        for attr, val in data.items():
            self._check_changes(instance, attr, val)
            setattr(instance, attr, val)
        return instance

    def _check_changes(self, instance, attr_name, value):
        if not self.is_changed and getattr(instance, attr_name) != value:
            self.is_changed = True

    def add_attendees_to_notified(self, attendees, subject_prefix):
        for i in attendees:
            self.attendees_to_notify.append({
                'attendee': i,
                'subject_prefix': subject_prefix
            })

    def notify_attendees(self):
        notif_service = notif_services.EventAttendeeNotification(self.event)
        for i in self.attendees_to_notify:
            notif_service.notify_attendee(i['attendee'], i['subject_prefix'])

    def delete_outdated_attendees(self, existing_attendees, actual_users):
        """Delete not actual attendees and add they to attendees to notify
        about cancelled event.
        :param existing_attendees: QuerySet of Attendee instances.
        :param actual_users: list of instances AUTH_USER_MODEL.
        :return: None
        """
        to_delete = []
        for i in existing_attendees:
            if i.user not in actual_users:
                to_delete.append(i.id)
        attendees_to_delete = (self.event
                                   .attendees
                                   .select_related('user')
                                   .filter(id__in=to_delete))
        attendees_to_delete_copy = [
            copy.deepcopy(i) for i in attendees_to_delete
        ]
        self.add_attendees_to_notified(
            attendees_to_delete_copy,
            notif_constants.EVENT_NOTIF_SUBJECT_PREFIX_CANCELLED
        )
        attendees_to_delete.delete()

    def update_existing_attendees(self, users_ids):
        """Down all attendees statuses to 'Invited' if event was changed.
        Send notifications about updating event.
        :param users_ids: list of users' ids.
        :return: None.
        """
        if self.is_changed:
            (self.event.attendees
             .exclude(user=self.event.owner)
             .update(status=enums.EventAttendeeStatusEnum.INVITED.name))  # noqa

            attendees = list(
                self.event.attendees
                .select_related('user')
                .filter(user__id__in=users_ids)
            )
            prefix = notif_constants.EVENT_NOTIF_SUBJECT_PREFIX_UPDATED
            self.add_attendees_to_notified(attendees, prefix)

    def add_new_attendees(self, actual_users, existing_attendees_user_ids):
        """Create new attendees and add they to notified.
        :param actual_users: list of instances AUTH_USER_MODEL.
        :param existing_attendees_user_ids: list of users' ids.
        :return: None.
        """
        data = [{
            'user': i,
            'event': self.event
        } for i in actual_users if i.id not in existing_attendees_user_ids]
        models.Attendee.objects.bulk_create(models.Attendee(**i) for i in data)

        attendees = list(
            self.event
            .attendees
            .select_related('user')
            .exclude(user__id__in=existing_attendees_user_ids)
        )
        prefix = notif_constants.EVENT_NOTIF_SUBJECT_PREFIX_INVITED
        self.add_attendees_to_notified(attendees, prefix)

    def actualize_attendees(self):
        existing_attendees = self.event.attendees.all()
        actual_users = list(itertools.chain(self.colleagues, self.candidates))
        existing_attendees_user_ids = list(existing_attendees
                                           .values_list('user__id', flat=True))
        self.delete_outdated_attendees(existing_attendees, actual_users)
        self.update_existing_attendees(existing_attendees_user_ids)
        self.add_new_attendees(actual_users, existing_attendees_user_ids)

    def update(self):
        self.event = self._update(self.event, self.event_data)
        self.event.location = self._update(
            self.event.location,
            self.location_data
        )
        self.event.save()
        self.event.location.save()
        self.actualize_attendees()
        self.notify_attendees()
        return self.event


def patch_user_event_notifications_with_additional_data(
        user, event, data):
    """
    Allows to update existing user event notifications with
    additional data (status, user response, etc.)
    """
    event_notifications = user.notifications.filter(
        actor_content_type__model='event',
        actor_object_id=event.id
    )
    for notif in event_notifications:
        notif.data['data']['full']['event'].update(data)
        notif.save()
