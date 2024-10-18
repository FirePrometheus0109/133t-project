from candidate import models
from leet import models as base_models
from tests.factories.auth import create_job_seeker, create_company_user
from tests.factories.job import create_job


def create_candidate(**kwargs):
    job_seeker = kwargs.pop('job_seeker', None) or create_job_seeker()
    company_user = kwargs.pop('company_user', None) or create_company_user()
    job = kwargs.pop('job', None) or create_job(
        company_user.company, owner=company_user)

    candidate = models.Candidate.objects.create(
        job=job,
        job_seeker=job_seeker,
        status=base_models.CandidateStatus.get_applied_status(),
        **kwargs)
    candidate.workflow_steps.create(status=candidate.status)
    return candidate


def create_workflow_step(**kwargs):
    candidate = kwargs.pop('candidate', None) or create_candidate()
    status = (kwargs.pop('status', None) or
              base_models.CandidateStatus.get_applied_status())
    workflow_step = models.WorkflowStep.objects.create(
        candidate=candidate,
        status=status,
        **kwargs)
    return workflow_step
