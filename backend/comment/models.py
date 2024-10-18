from django.contrib.contenttypes import fields as ct_fields
from django.contrib.contenttypes import models as ct_models
from django.db import models
from threadedcomments import models as tc_models

from leet import models as base_models


class JobSeekerComment(tc_models.ThreadedComment, base_models.BanStatusModel):

    def __str__(self):
        return f'{self.name}:{self.id}, created:{self.submit_date}'

    class Meta:
        verbose_name = 'Job seeker comment'


class JobComment(tc_models.ThreadedComment, base_models.BanStatusModel):

    def __str__(self):
        return f'{self.name}:{self.id}, created:{self.submit_date}'

    class Meta:
        verbose_name = 'Job comment'


class ViewComment(base_models.BaseModel):
    user = models.ForeignKey(
        'leet_auth.ProxyUser',
        on_delete=models.CASCADE,
        related_name='comment_viewer',
        verbose_name='User',
    )
    content_type = models.ForeignKey(
        ct_models.ContentType,
        verbose_name='content type',
        on_delete=models.CASCADE
    )
    object_pk = models.TextField(
        'object ID'
    )
    content_object = ct_fields.GenericForeignKey(
        ct_field='content_type',
        fk_field='object_pk'
    )
