import re

from django.conf import settings
from django.db.models import Q
from django.utils import timezone
from rest_framework import exceptions

from job_seeker import constants
from job_seeker import models
from job_seeker import services
from leet import enums
from leet import validators as base_valdiators


def validate_count_educations_and_certifications(job_seeker):
    """Job seeker can have maximum 30 education entries in him profile"""
    education_all = (models.JobSeeker
                     .objects
                     .filter(id=job_seeker.id)
                     .values_list(
                         'educations__id',
                         'certifications__id'))
    if len(education_all) == constants.MAX_COUNT_OF_EDUCATION:
        raise exceptions.ValidationError(
            constants.MAXIMUM_OF_EDUCATION_ENTRIES_ERROR)


def validate_date(date):
    """All dates of job experience should not be from future"""
    today = timezone.now()
    if date is not None and today < date:
        raise exceptions.ValidationError(
            constants.DATES_FROM_FUTURE_ERROR)
    return date


def validate_dates_period(date_from, date_to, is_current):
    """Default validator for JobExperience and Education serializers

    User should select correct dates for date_from and date_to fields
    If request data contains date_to:
        'is_current' should be False
        'date_from' should be less than date_to
    If request data does not contains 'date_to':
        'is_current' should be True"""
    if (date_from is not None
            and date_to is not None
            and date_from > date_to):
        raise exceptions.ValidationError(
            constants.DATE_FROM_GREATER_DATE_TO_ERROR)

    if date_to is not None and is_current:
        raise exceptions.ValidationError(
            constants.DATE_TO_AND_IS_CURRENT_ERROR)

    if date_to is None and not is_current:
        raise exceptions.ValidationError(
            constants.NO_DATE_TO_AND_NOT_IS_CURRENT_ERROR)


def validate_save_remove_actions(action_add, action_remove):
    """Only one action can be in request data for save/remove"""
    if action_add and action_remove:
        raise exceptions.ValidationError(
            constants.TWO_ACTIONS_FOR_ADDING_TO_SAVED_ERROR)
    if not action_add and not action_remove:
        raise exceptions.ValidationError(
            constants.NO_ACTIONS_FOR_ADDING_TO_SAVED_ERROR)


def validate_can_add_one_more_experience(job_seeker):
    """Job Seeker can have only 10 job experiences."""
    count = job_seeker.job_experience.count()
    if count == constants.MAX_COUNT_OF_JOB_EXPERIENCE:
        raise exceptions.ValidationError(
            constants.MAXIMUM_OF_JOB_EXPERIENCE_ERROR)


def validate_certification(graduated, is_current, licence_number):
    """Validator for certification.
        A current certification can not be with graduated date
            and with licence_number.
        If certification is not current it must have date of graduated
            and licence_number."""
    if ((graduated is not None or licence_number is not None)
            and is_current):
        raise exceptions.ValidationError(
            constants.CERTIFICATION_IS_CURRENT_ERROR)

    if (graduated is None or licence_number is None) and not is_current:
        raise exceptions.ValidationError(
            constants.CERTIFICATION_IS_NOT_CURRENT_ERROR)


def validate_can_add_one_more_document(job_seeker):
    count = job_seeker.documents.count()
    if count == constants.MAX_COUNT_OF_DOCUMENTS:
        raise exceptions.ValidationError(
            constants.MAXIMUM_OF_DOCUMENTS_ERROR)


def validate_document(job_seeker, document_file, extension):
    max_size_mb = constants.DOCUMENT_MAX_FILE_SIZE_MB
    base_valdiators.validate_file_size(document_file.size, max_size_mb,
                       constants.DOCUMENT_FILE_SIZE_ERROR)
    base_valdiators.validate_file_extension(
        extension, constants.VALID_DOCUMENT_EXTENSIONS,
        constants.NOT_VALID_DOCUMENT_EXTENSION_ERROR)
    validate_can_add_one_more_document(job_seeker)


def validate_salary(job_seeker, salary_min, salary_max):
    if salary_min is None:
        salary_min = job_seeker.salary_min
    if salary_max is None:
        salary_max = job_seeker.salary_max
    if all((salary_min, salary_max)) and salary_min > salary_max:
        raise exceptions.ValidationError(
            constants.MIN_SALARY_SHOULD_NOT_BE_GREATER_THAN_MAX
        )


def validate_can_public(job_seeker, is_public):
    if (is_public and not services.is_profile_public(job_seeker)):
        raise exceptions.ValidationError(
            constants.PROFILE_CANT_BE_PUBLIC_ERROR
        )


def validate_cover_letter_title_uniqueness(job_seeker, title, cover_letter):
    cover_letter_id = cover_letter.id if cover_letter else None
    if job_seeker.cover_letters.filter(
            ~Q(id=cover_letter_id), title=title).exists():
        raise exceptions.ValidationError(
            constants.COVER_LETTER_TITLE_SHOULD_BE_UNIQUE
        )


def validate_max_cover_letter_count(job_seeker):
    count = job_seeker.cover_letters.count()
    if count == constants.MAX_COUNT_OF_COVER_LETTERS:
        raise exceptions.ValidationError(
            constants.MAXIMUM_OF_COVER_LETTER_ENTRIES_ERROR
        )


def validate_phone(phone):
    if phone is not None:
        regexps = settings.VALIDATION_REGEXPS['phone_number_validator']
        if not re.match(regexps, phone):
            raise exceptions.ValidationError(
                constants.INVALID_PHONE_NUMBER_ERROR
            )


def validate_can_save_job_seeker_profile(job_seeker, company):
    errors = []
    full_name = job_seeker.user.get_full_name()
    if job_seeker.candidate_set.filter(job__company=company).exists():
        emsg = constants.SAVED_JOB_SEEKER_ALREADY_CANDIDATE_ERROR.format(
            full_name)
        errors.append(emsg)
    if company.purchased_job_seekers.filter(id=job_seeker.id).exists():
        emsg = constants.SAVED_JOB_SEEKER_ALREADY_PURCHASED_ERROR.format(
            full_name)
        errors.append(emsg)
    if job_seeker.ban_status == enums.BanStatusEnum.BANNED.name:  # noqa
        emsg = constants.SAVED_JOB_SEEKER_BANNED_ERROR.format(full_name)
        errors.append(emsg)
    if errors:
        raise exceptions.ValidationError(errors)


def validate_count_of_industries(industries):
    if len(industries) > constants.MAX_COUNT_OF_INDUSTRIES:
        raise exceptions.ValidationError(constants.MAXIMUM_OF_INDUSTRIES_ERROR)


def validate_count_of_skills(skills):
    if len(skills) > constants.MAX_COUNT_OF_SKILLS:
        raise exceptions.ValidationError(constants.MAXIMUM_OF_SKILLS_ERROR)
