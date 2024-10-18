# pylint: disable=unused-argument
from django.db.models.signals import post_save
from django.dispatch import receiver

from job_seeker import models


def _update_owner_document(instance):
    owner = models.JobSeeker.objects.with_documents().get(id=instance.owner.id)
    owner.search_vector = owner.document
    owner.save(update_fields=['search_vector', 'location_search_vector'])


@receiver(post_save, sender=models.Education)
def education_changed(sender, instance, **kwargs):
    _update_owner_document(instance)


@receiver(post_save, sender=models.Certification)
def certification_changed(sender, instance, **kwargs):
    _update_owner_document(instance)


@receiver(post_save, sender=models.JobExperience)
def experience_changed(sender, instance, **kwargs):
    _update_owner_document(instance)
