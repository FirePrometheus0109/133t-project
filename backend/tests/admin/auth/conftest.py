import pytest

from auth import forms
from auth import admin as auth_admin
from auth import models as auth_models


@pytest.fixture
def auth_model_admin(admin_site, db):
    return auth_admin.AuthUserAdmin(auth_models.ProxyUser, admin_site)


@pytest.fixture
def company_user_inline(admin_site, db):
    return auth_admin.CompanyUserInline(auth_models.ProxyUser, admin_site)


@pytest.fixture
def job_seeker_inline(admin_site, db):
    return auth_admin.JobSeekerInline(auth_models.ProxyUser, admin_site)


@pytest.fixture
def base_user_creation_form(request, db):
    return forms.CreateUserForm(request.param)


@pytest.fixture
def company_user_creation_form(request, db):
    return forms.CreateCompanyUserForm(request.param)


@pytest.fixture
def job_seeker_creation_form(request, db):
    return forms.CreateJobSeekerForm(request.param)
