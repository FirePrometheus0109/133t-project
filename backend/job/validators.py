from django.conf import settings
from django.utils import timezone
from rest_framework import exceptions

from job import constants
from job import services
from subscription import models
from leet import enums


def _validate_date_is_not_in_past(date, error):
    today = timezone.now().date()
    if date.date() < today:
        raise exceptions.ValidationError(error)


def validate_publish_date(job, date):
    """Publish date can not be in the past."""
    if (job is None or not job.publish_date
            or job.publish_date.date() != date.date()):
        _validate_date_is_not_in_past(
            date, constants.PUBLISH_DATE_IN_PAST_ERROR)


def validate_closing_date(date):
    """Closing date can not be in the past."""
    _validate_date_is_not_in_past(
        date, constants.CLOSING_DATE_IN_THE_PAST_ERROR)


def validate_publish_and_closing_dates(publish_date, closing_date):
    if not publish_date:
        publish_date = timezone.now()
    if closing_date and publish_date.date() >= closing_date.date():
        raise exceptions.ValidationError(
            constants.PUBLISH_DATE_GREAT_THAN_CLOSING_DATE_ERROR)


def validate_count_of_skills(skills):
    """Max count of required or optional skills per job is 20."""
    if len(skills) > constants.MAX_COUNT_OF_SKILLS:
        raise exceptions.ValidationError(constants.MORE_20_SKILLS_ERROR)


def validate_salary(salary_min, salary_max):
    if all((salary_min, salary_max)) and salary_min > salary_max:
        raise exceptions.ValidationError(
            constants.MIN_SALARY_MORE_THAN_MAX_SALARY_ERROR)


def validate_skills(required_skills, optional_skills, is_obj=True):
    if is_obj:
        set_req_skills = set(s.id for s in required_skills)
        set_opt_skills = set(s.id for s in optional_skills)
    else:
        set_req_skills = set(s.get('id') for s in required_skills)
        set_opt_skills = set(s.get('id') for s in optional_skills)

    if set_req_skills & set_opt_skills:
        raise exceptions.ValidationError(constants.SKILLS_INTERSECT_ERROR)


def validate_education(education, education_strict, emsg):
    if education_strict and not education:
        raise exceptions.ValidationError({'education': emsg})


def validate_job_is_not_already_deleted(job):
    if job.is_deleted:
        raise exceptions.ValidationError(constants.JOB_ALREADY_DELETED)


def validate_job_is_deleted(job):
    if not job.is_deleted:
        raise exceptions.ValidationError(constants.JOB_IS_NOT_DELETED)


def validate_job_can_be_closed(job, status):
    active = enums.JobStatusEnum.ACTIVE.name  # noqa
    closed = enums.JobStatusEnum.CLOSED.name  # noqa
    if status == closed and job.status != active:
        raise exceptions.ValidationError(
            constants.NOT_VALID_STATUS_TO_CLOSING_JOB)


def validate_status_for_creating_job(status):
    if status == enums.JobStatusEnum.CLOSED.name:  # noqa
        raise exceptions.ValidationError(
            constants.NOT_VALID_STATUS_FOR_CREATING_JOB)


def validate_company_jobs_balance(status, customer, job=None):
    if services.is_job_going_to_became_active(job=job, new_status=status):
        balance = (models.Balance.objects
                   .select_for_update()
                   .get(customer=customer))
        if balance.jobs_remain == 0:
            raise exceptions.ValidationError(constants.OUT_OF_JOB_ERROR)


class SalaryValueValidatorMixin:

    @staticmethod
    def validate_salary_value(salary):
        if salary and salary > settings.MAX_SALARY:
            raise exceptions.ValidationError(constants.MAX_SALARY_VALUE_ERROR)

    def validate_salary_max(self, salary):
        self.validate_salary_value(salary)
        return salary

    def validate_salary_min(self, salary):
        self.validate_salary_value(salary)
        return salary
