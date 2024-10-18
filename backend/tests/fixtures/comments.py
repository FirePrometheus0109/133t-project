import pytest

from tests import factories


@pytest.fixture
def job_comment(job_obj, company_user):
    return factories.create_job_comment(company_user, job_obj)


@pytest.fixture
def job_seeker_comment(job_seeker, company_user):
    return factories.create_job_seeker_comment(company_user, job_seeker)
