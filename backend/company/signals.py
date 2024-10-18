# pylint: disable=unused-argument
from django.db.models.signals import post_save
from django.dispatch import receiver

from company import models


@receiver(post_save, sender=models.Company)
def company_changed(sender, instance, **kwargs):
    for job in instance.jobs.with_documents():
        job.search_vector = job.document
        job.save(update_fields=['search_vector', 'location_search_vector'])
