from django.db import models

from leet import enums
from leet import models as base_models


class Survey(base_models.BaseModel):
    title = models.CharField(
        'title',
        max_length=256
    )
    company = models.ForeignKey(
        'company.Company',
        on_delete=models.CASCADE,
        related_name='surveys'
    )

    class Meta:
        unique_together = ('title', 'company')


class Question(base_models.BaseModel):
    body = models.CharField(
        'body',
        max_length=256,
    )
    is_answer_required = models.BooleanField(
        'is_answer_reqired',
        default=False
    )
    answer_type = models.CharField(
        'answer_type',
        max_length=64,
        choices=enums.AnswerTypeEnum.choices,
        default=enums.AnswerTypeEnum.YES_NO.name  # noqa
    )
    disqualifying_answer = models.CharField(
        'disqualifying_answer',
        max_length=256,
        blank=True,
        null=True
    )
    is_default = models.BooleanField(
        'is_default',
        default=False
    )
    surveys = models.ManyToManyField(
        Survey,
        related_name='questions',
        blank=True,
    )
    # Need for saved questions
    company = models.ForeignKey(
        'company.Company',
        on_delete=models.CASCADE,
        related_name='saved_questions',
        blank=True,
        null=True
    )
    job = models.ForeignKey(
        'job.Job',
        on_delete=models.CASCADE,
        related_name='questions',
        blank=True,
        null=True
    )


class Answer(base_models.BaseModel):
    yes_no_value = models.CharField(
        'yes_no_value',
        max_length=8,
        choices=enums.YesNoAnswerEnum.choices,
        blank=True,
        null=True
    )
    plain_text_value = models.TextField(
        'plain_text_value',
        blank=True,
        null=True
    )


class AnswerJobSeeker(base_models.BaseModel):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )
    answer = models.ForeignKey(
        'answer',
        on_delete=models.CASCADE,
        related_name='job_seeker_answers'
    )
    job = models.ForeignKey(
        'job.Job',
        on_delete=models.CASCADE,
        related_name='answers'
    )
    owner = models.ForeignKey(
        'job_seeker.JobSeeker',
        on_delete=models.CASCADE,
        related_name='answers'
    )
    answer_type = models.CharField(
        'answer_type',
        max_length=64,
        choices=enums.AnswerTypeEnum.choices,
        default=enums.AnswerTypeEnum.YES_NO.name  # noqa
    )

    class Meta:
        unique_together = ('job', 'owner', 'question')
