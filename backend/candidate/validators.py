from rest_framework import exceptions

from candidate import constants
from leet import constants as base_constants
from leet import enums


def validate_jobs_statuses_for_assigning(jobs):
    errors = []
    for j in jobs:
        if j['status'] not in constants.JOB_STATUSES_FOR_ASSIGNING_CANDIDATES:
            emsg = constants.NOT_VALID_JOB_STATUS_FOR_ASSIGNING.format(
                j['title'],
                j['status'])
            errors.append(emsg)
    if errors:
        raise exceptions.ValidationError(errors)


def validate_jobs_count(jobs):
    if len(jobs) > constants.MAX_COUNT_OF_JOBS:
        raise exceptions.ValidationError(constants.MAX_COUNT_OF_JOBS_ERROR)


def validate_job_seekers_count(job_seekers):
    if len(job_seekers) > constants.MAX_COUNT_OF_JOB_SEEKERS:
        raise exceptions.ValidationError(
            constants.MAX_COUNT_OF_JOB_SEEKERS_ERROR)


def validate_can_assign_job_seeker(job_seekers, company):
    """Only purchased or applied job seekers can be candidates."""
    purchased_job_seekers = set(company.purchased_job_seekers
                                       .values_list('id', flat=True))
    applied_job_seekers = set(company
                              .jobs
                              .filter(
                                  applies__applied_at__isnull=False)
                              .values_list('applies__owner__id', flat=True))
    errors = []
    for js in job_seekers:
        if (js['id'] not in purchased_job_seekers
                and js['id'] not in applied_job_seekers):
            emsg = constants.NOT_VALID_JOB_SEEKER_FOR_ASSIGNING.format(
                js['user__first_name'], js['user__last_name'])
            errors.append(emsg)
    if errors:
        raise exceptions.ValidationError(errors)


def validate_can_change_status_on_workflow(candidate):
    if candidate.status.name == base_constants.CANDIDATE_STATUS_REJECTED:
        raise exceptions.ValidationError(
            constants.NOT_VALID_CANDIDATE_FOR_CHANGE_STATUS)


def validate_job_seeker_can_create_answers(job_seeker, job, existing_answers):
    apply = job_seeker.applies.filter(job=job, applied_at__isnull=False)
    if existing_answers.exists() and not apply.exists():
        raise exceptions.ValidationError(constants.ANSWERS_CREATE_ERROR)


def validate_time_series_basis(basis):
    if basis not in constants.SUPPORTED_TIME_SERIES_BASES:
        raise exceptions.ValidationError({
            'none_field_errors': [
                constants.INVALID_TIME_SERIES_BASIS_ERROR_MESSAGE.format(
                    constants.SUPPORTED_TIME_SERIES_BASES)
            ]
        })


def validate_questions_for_answers(questions, job):
    errors = []
    required_job_questions = job.questions.filter(is_answer_required=True)
    answered_required_questions = list(filter(
        lambda x: x.is_answer_required, questions
    ))
    if required_job_questions.count() != len(answered_required_questions):
        emsg = constants.INVALID_COUNT_QUESTIONS_FOR_ANSWERS.format(job.title)
        errors.append(emsg)
    questions_ids = {i.id for i in required_job_questions}
    questions_j_ids = {i.id for i in answered_required_questions}
    if questions_ids != questions_j_ids:
        emsg = constants.INVALID_QUESTIONS_FOR_ANSWERS.format(job.title)
        errors.append(emsg)
    if errors:
        raise exceptions.ValidationError(errors)


class CandidateRestoreValidator:

    def __init__(self, candidate):
        self.candidate = candidate
        self.job = candidate.job
        self.errors = []

    def _validate_rejected_candidate_status(self):
        status_name = self.candidate.status.name
        if status_name != base_constants.CANDIDATE_STATUS_REJECTED:
            self.errors.append(constants.RESTORE_CANDIDATE_ERROR)

    def _validate_rejected_candidate_doesnt_reapplied(self):
        job_seeker = self.candidate.job_seeker
        c_set = job_seeker.candidate_set.filter(job=self.job)
        rejected_status = self.candidate.workflow_steps.last().status
        if c_set.exclude(workflow_steps__status=rejected_status).exists():
            self.errors.append(
                constants.REJECTED_CANDIDATE_ALREADY_REAPPLIED_ERROR)

    def _validate_candidate_job(self):
        if self.job.status == enums.JobStatusEnum.CLOSED.name:  # noqa
            self.errors.append(
                constants.REJECTED_CANDIDATE_JOB_IS_CLOSED_ERROR)
        if self.job.is_deleted:
            self.errors.append(
                constants.REJECTED_CANDIDATE_JOB_IS_DELETED_ERROR)

    def validate(self):
        validators = (
            self._validate_rejected_candidate_status,
            self._validate_rejected_candidate_doesnt_reapplied,
            self._validate_candidate_job
        )
        for v in validators:
            v()
        if self.errors:
            raise exceptions.ValidationError(self.errors)
