from django.db import models

from leet import models as base_models


class LetterTemplate(base_models.BaseModel):

    name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    body = models.TextField(max_length=4000)
    company = models.ForeignKey(
        'company.Company',
        on_delete=models.CASCADE,
        related_name='letter_templates'
    )
    event_type = models.ForeignKey(
        'leet.EventType',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name
