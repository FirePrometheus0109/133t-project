import datetime
import itertools

from django.conf import settings
from django.db import transaction
from django.utils import timezone

from job import constants
from job import models
from job import services
from leet import emaillib, enums
from leet.taskapp.celery import app


@app.task(name='publish-jobs')
def publish_jobs():
    """Publish all delayed jobs at scheduled time.
    DELAYED -> ACTIVE"""
    delayed = enums.JobStatusEnum.DELAYED.name  # noqa
    active = enums.JobStatusEnum.ACTIVE.name  # noqa
    date = timezone.now().date()
    (models.Job
           .objects
           .filter(publish_date__date=date, status=delayed)
           .update(status=active))


@app.task(name='hard-delete-jobs')
def hard_delete_jobs():
    """
    Mark all soft deleted jobs as not active if 6 month passed after deletion.
    """
    hard_delete_period_length = getattr(
        settings,
        'HARD_DELETE_JOBS_INTERVAL_LENGTH'
    )
    (models.Job
        .objects
        .filter(is_deleted=True,
                deleted_at__lte=timezone.now() - datetime.timedelta(
                    days=hard_delete_period_length
                ),
                status='')
        .update(is_active=False))


@app.task(name='close-expired-jobs')
def close_expired_jobs():
    """
    Set status close for all jobs that should be closed on certain day.
    Move all candidates to rejected.
    """
    with transaction.atomic():
        closing_date = timezone.now().date()
        jobs = models.Job.objects.filter(
            status=enums.JobStatusEnum.ACTIVE.name,  # noqa
            closing_date__date=closing_date)
        for j in jobs:
            services.move_job_candidates_to_rejected(j)
        jobs.update(status=enums.JobStatusEnum.CLOSED.name)  # noqa


@app.task(name='notify-job-owners-about-closing-date')
def notify_job_owners_about_closing_date():
    """Send notifications about soon closing date for jobs"""

    def group_by_user_data(item):
        return item['email'], item['f_name'], item['l_name']

    def build_url(job_id):
        return settings.JOB_DETAILS_URL.format(
            http=settings.HTTP_SCHEME,
            domain_name=settings.DOMAIN_NAME,
            id=job_id)

    interval = settings.COUNT_OF_DAYS_FOR_SENDING_EMAIL_BEFORE_CLOSING_JOBS
    closing_date = timezone.now().date() + datetime.timedelta(days=interval)
    jobs = services.get_jobs_for_notification_about_closing_date(closing_date)

    closing_date = closing_date.strftime(
        settings.DATE_FORMAT_FOR_CLOSING_JOBS_EMAIL_TEMPLATE)
    grouped_jobs = itertools.groupby(jobs, key=group_by_user_data)

    for user, jobs in grouped_jobs:
        urls_and_titles = [(build_url(j['id']), j['title']) for j in jobs]
        context = {
            'domain_name': settings.DOMAIN_NAME,
            'closing_date': closing_date,
            'urls_and_titles': urls_and_titles,
            'first_name': user[1],
            'last_name': user[2],
            'interval': interval
        }
        emaillib.send_email(
            constants.CLOSE_JOBS_EMAIL_TEMPLATE, user[0], context)
