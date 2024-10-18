from django.db import models

from leet import enums
from leet import models as base_models


class Autoapply(base_models.BaseModel):
    title = models.CharField(max_length=256)
    status = models.CharField(
        choices=enums.AutoapplyStatusEnum.choices, max_length=40,
        default=enums.AutoapplyStatusEnum.SAVED.name)  # noqa
    query_params = models.CharField(blank=True, max_length=256)
    stopped_jobs = models.ManyToManyField(
        'job.Job',
        related_name='autoapply_sj')
    deleted_jobs = models.ManyToManyField(
        'job.Job',
        related_name='autoapply_dj')
    number = models.IntegerField()
    owner = models.ForeignKey(
        'job_seeker.JobSeeker',
        on_delete=models.CASCADE,
        related_name='autoapplies'
    )
    jobs = models.ManyToManyField(
        'job.Job',
        through='Apply'
    )
    started_at = models.DateTimeField(blank=True, null=True)
    finished_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ('title', 'owner')

    @classmethod
    def get_queryset(cls):
        return (cls.objects
                   .prefetch_related(
                       'stopped_jobs',
                       'deleted_jobs',
                       'jobs')
                   .select_related(
                       'owner',
                       'owner__user'))


class Apply(base_models.BaseModel):
    autoapply = models.ForeignKey(
        Autoapply,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    job = models.ForeignKey(
        'job.Job',
        on_delete=models.CASCADE,
        related_name='applies'
    )
    owner = models.ForeignKey(
        'job_seeker.JobSeeker',
        on_delete=models.CASCADE,
        related_name='applies'
    )
    status = models.CharField(
        choices=enums.ApplyStatusEnum.choices,
        max_length=40,
        default=enums.ApplyStatusEnum.APPLIED.name  # noqa
    )
    applied_at = models.DateTimeField(
        null=True,
        blank=True
    )
    cover_letter = models.ForeignKey(
        'job_seeker.CoverLetter',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        unique_together = ('job', 'owner', 'autoapply')
