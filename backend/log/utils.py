from django.db import models as orm

from log import models


def get_company_logs(company, **kwargs):
    """
    Return all logs that belong certain company.
    Filter by owner if log was created by company user
    or filter by job_company for logs which owner is job seeker.
    """
    qs = (models.Log
                .objects
                .select_related('owner')
                .filter(
                    orm.Q(owner__company_user__company=company)
                    |
                    orm.Q(job_company=company)))
    if kwargs:
        qs = qs.filter(**kwargs)
    return qs


def create_log(owner, log_type, log_message, content_object, **kwargs):
    data = {
        'owner': owner,
        'type': log_type,
        'message': log_message,
        'content_object': content_object,
        'job_company': kwargs.get('job_company'),
        'other_info': kwargs.get('other_info')
    }
    return models.Log.objects.create(**data)
