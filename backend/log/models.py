from django.conf import settings
from django.contrib.contenttypes import fields as ct_fields
from django.contrib.contenttypes import models as ct_models
from django.db import models


class Log(models.Model):

    time = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    type = models.CharField(max_length=64)
    message = models.CharField(max_length=255)
    # NOTE (i.bogretsov) it will be better to use JsonField
    other_info = models.TextField(
        blank=True,
        null=True)
    job_company = models.ForeignKey(
        'company.Company',
        on_delete=models.CASCADE,
        null=True
    )
    content_type = models.ForeignKey(
        ct_models.ContentType,
        verbose_name='content type',
        on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField()
    content_object = ct_fields.GenericForeignKey(
        'content_type',
        'object_id'
    )

    class Meta:
        ordering = ('-time',)
