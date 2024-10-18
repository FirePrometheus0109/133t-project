import pytest

from comment import admin, models, forms


@pytest.fixture
def job_comments_admin(admin_site):
    return admin.JobCommentAdmin(models.JobComment, admin_site)


@pytest.fixture
def job_seeker_comments_admin(admin_site):
    return admin.JobSeekerCommentAdmin(models.JobSeekerComment, admin_site)


@pytest.fixture
def job_comment_creation_form():
    return forms.JobCommentCreationForm


@pytest.fixture
def job_comment_change_form():
    return forms.JobCommentChangeForm


@pytest.fixture
def job_seeker_comment_creation_form():
    return forms.JobSeekerCommentCreationForm


@pytest.fixture
def job_seeker_comment_change_form():
    return forms.JobSeekerCommentChangeForm
