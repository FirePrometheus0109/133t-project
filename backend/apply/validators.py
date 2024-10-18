from django import http
from django.db import models as orm
from rest_framework import exceptions

from apply import constants
from apply import exceptions as apply_exceptions
from apply import services
from geo import models as geo_models
from job import services as job_services
from leet import enums
from leet import services as base_services


def validate_applied_jobs(job_seeker, applied_jobs):
    # if not applied_jobs:
    #     raise exceptions.ValidationError(constants.EMPTY_JOB_LIST_ERROR)
    if len(applied_jobs) > constants.MAX_NUMBER_OF_JOBS_TO_AUTOAPPLY:
        raise exceptions.ValidationError(constants.MORE_THAN_30_JOBS_ERROR)
    applies = job_seeker.applies.filter(
        job_id__in=applied_jobs,
        status=enums.ApplyStatusEnum.APPLIED.name  # noqa
    )
    if applies.exists():
        raise exceptions.ValidationError(
            constants.YOU_CANT_APPLY_FOR_ALREADY_APPLIED_JOB_ERROR
        )


def validate_autoapply_title_uniqueness(job_seeker, title, autoapply):
    autoapply_id = autoapply.id if autoapply else None
    if job_seeker.autoapplies.filter(
            ~orm.Q(id=autoapply_id), title=title, owner=job_seeker).exists():
        raise exceptions.ValidationError(
            constants.AUTOAPPLY_TITLE_SHOULD_BE_UNIQUE_ERROR
        )


def validate_autoapply_jobs_number(number):
    if number > constants.MAX_NUMBER_OF_JOBS_TO_AUTOAPPLY:
        raise exceptions.ValidationError(constants.MORE_THAN_30_JOBS_ERROR)


def validate_job_is_already_applied(job, job_seeker):
    apply = job.applies.filter(
        owner=job_seeker,
        status__in=constants.APPLIED_OR_NEED_REVIEW)
    if apply.exists():
        raise apply_exceptions.ApplyException(
            [constants.YOU_CANT_APPLY_FOR_ALREADY_APPLIED_JOB_ERROR])


def validate_matching_for_manual_apply(job, job_seeker, cover_letter):
    errors = []
    if not job_services.is_clearance_match(job, job_seeker):
        errors.append(constants.CLEARANCE_DOESNT_MATCH_ERROR)
    if not job_services.is_questionnaire_answered(job, job_seeker):
        errors.append(constants.ANSWER_QUESTIONNAIRE_BEFORE_APPLYING_ERROR)
    if not job_services.is_cover_letter_provided(job, cover_letter):
        errors.append(constants.COVER_LETTER_IS_REQUIRED_FOR_APPLY)
    if not job_services.is_required_skills_match(job, job_seeker):
        errors.append(constants.REQUIRED_SKILLS_MATCH_ERROR)
    if errors:
        raise apply_exceptions.ApplyException(errors)


def validate_job_is_active(job):
    if not base_services.is_job_active(job):
        raise exceptions.ValidationError(
            constants.IMPOSSIBLE_TO_APPLY_FOR_NOT_ACTIVE_JOB_ERROR)


def validate_js_required_skills(job_seeker, job):
    if not services.are_js_required_skills_matched(job_seeker, job):
        raise apply_exceptions.ApplyException(
            constants.REQUIRED_SKILLS_MATCH_ERROR)


def validate_job_seeker_can_reapply(job_seeker, job, apply, cover_letter):
    if apply.autoapply is not None:
        validate_js_required_skills(job_seeker, job)
    validate_job_is_active(job)
    validate_matching_for_manual_apply(job, job_seeker, cover_letter)


def validate_auto_apply_query_params(query_params):
    params = http.QueryDict(query_string=query_params)
    state_id = params.get('state_id', None)
    city_id = params.get('city_id', None)
    if state_id:
        if not geo_models.State.objects.filter(id=state_id).exists():
            raise exceptions.ValidationError(
                constants.INVALID_STATE_ID_IN_QUERY_PARAMS_ERROR)
    if city_id:
        if not geo_models.City.objects.filter(id=city_id).exists():
            raise exceptions.ValidationError(
                constants.INVALID_CITY_ID_IN_QUERY_PARAMS_ERROR)


def validate_apply_wont_exceed_autoapply_number(autoapply, job):
    currently_applied_count = (
        autoapply.apply_set
        .exclude(job=job)
        .filter(status=enums.ApplyStatusEnum.APPLIED.name).count()
    )
    if currently_applied_count >= autoapply.number:
        raise exceptions.ValidationError(
            constants.AUTOAPPLY_NUMBER_EXCEED_ERROR)
