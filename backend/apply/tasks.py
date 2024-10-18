# pylint: disable=no-member
import datetime
import itertools

from django.conf import settings
from django.db import models as orm
from django.utils import timezone
from notifications import signals
from constance import config

from apply import constants
from apply import models
from apply import services
from leet import emaillib
from leet import enums
from leet.taskapp.celery import app
from notification_center import utils as notif_utils
from notification_center import constants as notif_constants


@app.task(name='find-autoapply-jobs')
def find_autoapply_jobs():
    """Actualize autoapply jobs list."""
    models.Autoapply.objects.filter(
        status=enums.AutoapplyStatusEnum.IN_PROGRESS.name,
        started_at__lte=timezone.now() - datetime.timedelta(
            days=config.AUTOAPPLY_PERIOD_LENGTH
        )
    ).update(
        status=enums.AutoapplyStatusEnum.FINISHED.name,
        finished_at=timezone.now()
    )
    in_progress_autoapplies = models.Autoapply.objects.filter(
        status=enums.AutoapplyStatusEnum.IN_PROGRESS.name
    )
    for autoapply in in_progress_autoapplies:
        aa_service = services.AutoapplyService(
            autoapply.owner, autoapply
        )
        # ToDo: try to replace actualize_autoapply_jobs_list
        # ToDo: with get_autoapply_jobs
        jobs_to_apply = aa_service.actualize_autoapply_jobs_list()
        aa_service.autoapply_to_jobs(jobs_to_apply)
    models.Autoapply.objects.annotate(jobs_count=orm.Count('jobs')).filter(
        pk__in=in_progress_autoapplies,
        jobs_count__gte=orm.F('number')
    ).update(
        status=enums.AutoapplyStatusEnum.FINISHED.name,
        finished_at=timezone.now()
    )


@app.task(name='send-autoapply-web-notifications')
def send_autoapply_web_notifications():
    """Sends daily autoapply notifications"""
    aa_notif_web = notif_utils.get_autoapply_web_notif_type()
    timedelta = timezone.now() - datetime.timedelta(minutes=10)
    autoapplies = services.get_autoapplies_for_notification(
        aa_notif_web, timedelta
    )
    for aa in autoapplies:
        finished = enums.AutoapplyStatusEnum.FINISHED.name
        if aa.status == finished:
            notify_about_finished_autoapply(aa)


@app.task(name='send-autoapply-email-notifications')
def send_autoapply_email_notifications():
    """Sends daily autoapply notifications"""
    aa_notif_email = notif_utils.get_autoapply_email_notif_type()
    timedelta = timezone.now() - datetime.timedelta(days=1)
    autoapplies = services.get_autoapplies_for_notification(
        aa_notif_email, timedelta
    )
    user_contexts = []
    for aa in autoapplies:
        status_update = (
            aa.started_at
            if aa.status == enums.AutoapplyStatusEnum.IN_PROGRESS.name
            else aa.finished_at
        )
        details_url = settings.AUTOAPPLY_DETAILS_URL.format(
            http=settings.HTTP_SCHEME,
            domain_name=settings.DOMAIN_NAME,
            id=aa.id)
        context = {
            'user': aa.owner.user,
            'title': aa.title,
            'autoapply_details_url': details_url,
            'number': aa.number,
            'status': aa.get_status_display(),
            'status_update': status_update,
            'applied_count': aa.applied_job_cnt,
            # 'new_count': aa.new_job_cnt,
            'need_review_count': aa.need_review_job_cnt,
            'viewed_count': aa.viewed_job_cnt,
        }
        user_contexts.append(context)
    user_contexts = _group_by_user(user_contexts)
    emaillib.send_emails(
        constants.AUTOAPPLY_NOTIFICATION_TEMPLATE_NAME,
        user_contexts)


def _group_by_user(contexts):
    domain_name = settings.DOMAIN_NAME
    users_autoapplies = []
    grouped_autoapplies = itertools.groupby(contexts, key=lambda x: x['user'])
    for user, autoapplies in grouped_autoapplies:
        users_autoapplies.append({
            'user': user,
            'autoapplies': list(autoapplies),
            'domain_name': domain_name,
        })
    return users_autoapplies


def notify_about_new_jobs(autoapply):
    # Now we auto apply new jobs instead of notifying about it
    description = (
        notif_constants.NOTIFICATION_DESCRIPTION_FIND_NEW_JOB_AUTOAPPLY
    )
    verb = notif_constants.NOTIFICATION_VERB_FIND_NEW_JOB_AUTOAPPLY
    _notify(autoapply, verb, description)


def notify_about_finished_autoapply(autoapply):
    description = (
        notif_constants.NOTIFICATION_DESCRIPTION_FINISHED_AUTOAPPLY
    )
    verb = notif_constants.NOTIFICATION_VERB_FINISHED_AUTOAPPLY
    _notify(autoapply, verb, description)


def _notify(autoapply, verb, description):
    signals.notify.send(
        autoapply,
        recipient=autoapply.owner.user,
        verb=verb,
        description=description,
        data={
            'short': {
                'autoapply': {
                    'id': autoapply.id,
                    'title': autoapply.title
                }
            },
            'full': {
                'autoapply': {
                    'id': autoapply.id,
                    'title': autoapply.title,
                    'description': description
                }
            }
        })
