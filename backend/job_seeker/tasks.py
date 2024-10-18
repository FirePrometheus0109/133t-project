import itertools

from django.conf import settings
from django.db import models as orm

from job_seeker import constants
from job_seeker import models
from job_seeker import services
from leet import emaillib
from leet.taskapp.celery import app
from notification_center import constants as notif_constants
from notification_center import models as notif_models


def get_company_details_url(domain_name, company_id):
    return settings.COMPANY_PROFILE_DETAILS_URL.format(
        http=settings.HTTP_SCHEME,
        domain_name=domain_name,
        id=company_id
    )


@app.task(name='send-profile-views')
def send_profile_views():
    """
    Send notifications about views job seeker's profile.
    Job seeker should be subscribed for 'Profile viewes' notification.
    """

    def key(item):
        return (item['email'], item['first_name'], item['last_name'])

    notif = notif_models.NotificationType.objects.filter(
        name=notif_constants.NOTIFICATION_TYPE_PROFILE_VIEWS,
        format=notif_constants.NOTIFICATION_FORMAT_EMAIL)
    views_qs = (models.ViewJobSeeker
                .objects
                .filter(
                    job_seeker__user__subscribed_notifications__id__in=notif)
                .annotate(
                    first_name=orm.F('job_seeker__user__first_name'),
                    last_name=orm.F('job_seeker__user__last_name'),
                    email=orm.F('job_seeker__user__email'),
                    company_name=orm.F('company_user__company__name'),
                    _company_id=orm.F('company_user__company__id'))
                .values(
                    'first_name',
                    'last_name',
                    'email',
                    'company_name',
                    '_company_id'))
    views_qs = services.group_views_qs_by_company(views_qs)
    groups = itertools.groupby(views_qs, key=key)
    for user, companies in groups:
        companies = [
            (
                c['company_name'],
                get_company_details_url(settings.DOMAIN_NAME, c['_company_id'])
            ) for c in companies]
        context = {
            'first_name': user[1],
            'last_name': user[2],
            'companies': companies,
            'domain_name': settings.DOMAIN_NAME
        }
        emaillib.send_email(
            constants.VIEW_PROFILES_TEMPLATE_NAME,
            user[0],
            context)
