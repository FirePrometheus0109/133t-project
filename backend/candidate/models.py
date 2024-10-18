from django.db import models

from leet import enums
from leet import models as base_models


class Candidate(base_models.BaseModel):

    job_seeker = models.ForeignKey(
        'job_seeker.JobSeeker',
        on_delete=models.CASCADE
    )
    job = models.ForeignKey(
        'job.Job',
        on_delete=models.CASCADE,
        related_name='candidates'
    )
    apply = models.ForeignKey(
        'apply.Apply',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    status = models.ForeignKey(
        'leet.CandidateStatus',
        on_delete=models.CASCADE,
        related_name='candidates'
    )
    previous_applied_date = models.DateTimeField(
        'previous_applied_date',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.job_seeker.user.get_full_name()  # noqa


class Rating(base_models.BaseModel):

    rating = models.CharField(
        'rating',
        max_length=16,
        choices=enums.RatingEnum.choices,
        default=enums.RatingEnum.NO_RATING.name  # noqa
    )
    owner = models.ForeignKey(
        'company.CompanyUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    candidate = models.OneToOneField(
        Candidate,
        on_delete=models.CASCADE,
        related_name='rating'
    )


class WorkflowStep(base_models.BaseModel):

    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
        related_name='workflow_steps'
    )
    status = models.ForeignKey(
        'leet.CandidateStatus',
        on_delete=models.CASCADE
    )
    owner = models.ForeignKey(
        'company.CompanyUser',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    class Meta:
        ordering = ('status__workflow_value',)
