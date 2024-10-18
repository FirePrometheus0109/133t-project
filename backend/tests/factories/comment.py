from django.conf import settings as django_settings
from django.contrib.contenttypes import models as ct_models

from faker import Faker

from comment.models import JobSeekerComment, JobComment
from tests.factories.auth import create_company_user, create_job_seeker
from tests.factories.job import create_job


fake = Faker()


def get_base_comment_data(author, commented_object, **kwargs):
    """
    Generate base comment data

    :param commented_object: the object to which the comment is attached
    :param author: comment author
    """
    comment_data = {
        'title': fake.word(),
        'comment': fake.sentence(),
        'site_id': getattr(django_settings, 'SITE_ID'),
        'user': author.user,
        'content_type': ct_models.ContentType.objects.get_for_model(
            commented_object),
        'object_pk': commented_object.pk
    }
    comment_data.update(**kwargs)
    return comment_data


def create_job_seeker_comment(company_user=None, job_seeker=None, **kwargs):
    """
    Create job seeker comment
    """
    company_user = company_user if company_user is not None else \
        create_company_user()
    job_seeker = job_seeker if job_seeker is not None else create_job_seeker()
    data = get_base_comment_data(company_user, job_seeker, **kwargs)
    return JobSeekerComment.objects.create(**data)


def create_job_comment(company_user=None, job=None, **kwargs):
    """
    Create job seeker comment
    """
    company_user = company_user if company_user is not None else \
        create_company_user()
    job = job if job is not None else create_job(
        company_user.user.company_user.company, owner=company_user)
    data = get_base_comment_data(company_user, job, **kwargs)
    return JobComment.objects.create(**data)
