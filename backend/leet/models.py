from django.db import models

from leet.enums import BanStatusEnum
from leet import constants


class BaseManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class BaseModel(models.Model):
    """Inherit all project models from this one"""

    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    objects = BaseManager()


class BanStatusModel(models.Model):

    class Meta:
        abstract = True

    ban_status = models.CharField(
        'ban_status',
        max_length=16,
        choices=BanStatusEnum.choices,
        default=BanStatusEnum.ACTIVE.name  # noqa
    )


class CandidateStatus(models.Model):

    name = models.CharField(
        'name',
        max_length=16
    )
    workflow_value = models.PositiveSmallIntegerField(
        'workflow_value'
    )

    @classmethod
    def get_applied_status(cls):
        return cls.objects.get(name=constants.CANDIDATE_STATUS_APPLIED)

    @classmethod
    def get_rejected_status(cls):
        return cls.objects.get(name=constants.CANDIDATE_STATUS_REJECTED)

    def __str__(self):
        return self.name or ''


class EventType(models.Model):

    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name
