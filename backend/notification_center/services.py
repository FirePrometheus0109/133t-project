import copy

import pytz
from django.conf import settings
from notifications import signals

from leet import emaillib
from leet import utils as base_utils
from notification_center import constants
from notification_center import utils


class EventBaseNotification:

    def __init__(self, event):
        self.event = event
        self.cache = {}

    @property
    def job_details_url(self):
        return settings.JOB_DETAILS_URL.format(
            http=settings.HTTP_SCHEME,
            domain_name=settings.DOMAIN_NAME,
            id=self.event.job_id
        )

    @property
    def respond_url(self):
        return settings.NOTIFICATION_LIST_URL.format(
            http=settings.HTTP_SCHEME,
            domain_name=settings.DOMAIN_NAME
        )

    @staticmethod
    def _get_company_address_filled_fields(address):
        map_lists = (
            ['county', 'name'],
            ['city', 'name'],
            ['city', 'state', 'abbreviation'],
            ['zip', 'code'],
            ['address'],
        )
        fields = (
            base_utils.get_from_nested_structure(
                address, i, func=getattr, default=''
            ) for i in map_lists
        )
        return filter(len, fields)

    def get_base_context(self):
        if 'base_context' in self.cache:
            return copy.deepcopy(self.cache['base_context'])
        tz = pytz.timezone(self.event.timezone)
        time_from = self.event.time_from.astimezone(tz)
        time_to = self.event.time_to.astimezone(tz)
        company_address_fields = self._get_company_address_filled_fields(
            self.event.company.address)
        company_address = ', '.join(company_address_fields)
        base_context = {
            'event_description': self.event.description,
            'event_owner_full_name': self.event.owner.get_full_name(),
            'company_name': self.event.company.name,
            'company_address': company_address,
            'time_from': time_from,
            'time_to': time_to,
            'timezone': time_from.tzname(),
            'country_name': self.event.location.country.name,
            'city_name': self.event.location.city.name,
            'state_abbreviation': self.event.location.city.state.abbreviation,
            'address': self.event.location.address,
            'zip_code': self.event.location.zip.code,
            'job_details_url': self.job_details_url,
            'job_title': self.event.job.title,
        }
        self.cache['base_context'] = copy.deepcopy(base_context)
        return base_context


class EventAttendeeNotification(EventBaseNotification):

    """Service to send event notifications to attendees."""

    @property
    def subscribed_users_ids_email_notif(self):
        if 'subscribed_users' in self.cache:
            return self.cache['subscribed_users']
        notif_type = utils.get_invitation_received_email_notif_type()
        users_ids = utils.get_subscribed_users(notif_type)
        self.cache['subscribed_users'] = users_ids
        return users_ids

    def get_subject(self, prefix):
        if prefix == constants.EVENT_NOTIF_SUBJECT_PREFIX_INVITED:
            return self.event.subject
        return '{}: {}'.format(prefix, self.event.subject)

    def get_base_context(self, subject_prefix):  # noqa
        context = super().get_base_context()
        context['event_subject'] = self.get_subject(subject_prefix)
        return context

    def get_email_context(self, user, subject_prefix):
        context = self.get_base_context(subject_prefix=subject_prefix)
        context['domain_name'] = settings.DOMAIN_NAME
        context['respond_url'] = self.respond_url
        context['attendee_full_name'] = user.get_full_name()
        return context

    def get_web_context(self, attendee, subject_prefix):
        context = self.get_base_context(subject_prefix=subject_prefix)
        if subject_prefix == constants.EVENT_NOTIF_SUBJECT_PREFIX_CANCELLED:
            context['cancelled'] = True
        context['attendee_id'] = attendee.id
        return context

    def notify_attendee_by_email(self, attendee, subject_prefix):
        if attendee.user_id in self.subscribed_users_ids_email_notif:
            context = self.get_email_context(attendee.user, subject_prefix)
            subject = (
                f'[{context["domain_name"]}]: '
                f'{context["event_subject"]} from {context["company_name"]}'
            )
            emaillib.send_user_generated_email(
                subject,
                'event_invitation.html',
                attendee.user.email,
                context
            )

    def notify_attendee_by_web(self, attendee, subject_prefix):
        context = self.get_web_context(attendee, subject_prefix)
        description = (
            constants.NOTIF_DESCRIPTION_EVENT_SUBJECT_MAP[subject_prefix]
        )
        description = description.format(self.event.company)
        signals.notify.send(
            self.event,
            recipient=attendee.user,
            verb=constants.NOTIFICATION_VERB_SENT_INVITATION,
            description=description,
            data={
                'short': {
                    'event': {
                        'description': description
                    }
                },
                'full': {
                    'event': context
                }
            }
        )

    def notify_attendee(self, attendee, subject_prefix):
        self.notify_attendee_by_email(attendee, subject_prefix)
        self.notify_attendee_by_web(attendee, subject_prefix)


class EventOwnerNotification(EventBaseNotification):

    """Service to send event notifications to owner about attendee status."""

    def __init__(self, event, attendee):
        super().__init__(event)
        self.owner = event.owner
        self.attendee = attendee

    def get_base_context(self):
        context = super().get_base_context()
        context['attendee_status'] = self.attendee.status.lower()
        context['attendee_full_name'] = self.attendee.user.get_full_name()
        return context

    def notify_owner_by_email(self):
        context = self.get_base_context()
        subject = (
            f'[{settings.DOMAIN_NAME}]: {context["attendee_status"]}: '
            f'{self.event.subject} from {context["company_name"]}'
        )
        emaillib.send_user_generated_email(
            subject,
            'event_response_invitation.html',
            self.owner.email,
            context
        )

    def notify_owner_by_web(self):
        context = self.get_base_context()
        description = (
            constants.NOTIFICATION_DESCRIPTION_RESPONSE_INVITATION.format(
                self.attendee.user.get_full_name(),
                self.attendee.get_status_display().lower(),
            )
        )
        signals.notify.send(
            self.event,
            recipient=self.owner,
            verb=constants.NOTIFICATION_VERB_RESPONSE_TO_INVITATION,
            description=description,
            data={
                'short': {
                    'event': {
                        'description': description
                    }
                },
                'full': {
                    'event': context
                }
            }
        )

    def notify_owner(self):
        self.notify_owner_by_email()
        self.notify_owner_by_web()
