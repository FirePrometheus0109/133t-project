from django.conf import settings
from rest_framework import exceptions

from letter_template import constants


def validate_name_letter_template(instance, company, name):
    template = company.letter_templates.filter(name=name)
    if instance is None:
        if template.exists():
            raise exceptions.ValidationError(
                constants.LETTER_TEMPLATE_NAME_NOT_UNIQUE_ERROR)
    elif instance.name != name and template.exclude(id=instance.id).exists():
        raise exceptions.ValidationError(
            constants.LETTER_TEMPLATE_NAME_NOT_UNIQUE_ERROR)


def validate_count_of_existing_templates(company):
    max_count = settings.MAX_COUNT_OF_LETTER_TEMPLATES_FOR_COMPANY
    if company.letter_templates.count() >= max_count:
        raise exceptions.ValidationError(
            constants.MAXIMUM_OF_LETTER_TEMPLATES_ERROR)


def validate_count_of_existing_templates_admin(company):
    # NOTE: (i.bogretsov) we can not use because in admin page
    # object has already been created and we should check
    # count of existing templates + new template
    max_count = settings.MAX_COUNT_OF_LETTER_TEMPLATES_FOR_COMPANY
    if company.letter_templates.count() > max_count:
        raise exceptions.ValidationError(
            constants.MAXIMUM_OF_LETTER_TEMPLATES_ERROR)
