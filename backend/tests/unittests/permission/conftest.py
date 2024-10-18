import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from permission import utils
from permission.models import PermissionGroup

User = get_user_model()


@pytest.fixture
def company_user(db):
    return Group.objects.get(name='company_user')


@pytest.fixture
def job_seeker(db):
    return Group.objects.get(name='job_seeker')


@pytest.fixture
def company_user_perms(company_user):
    perms = (company_user
             .permissions
             .values_list(
                 'content_type__app_label',
                 'codename'))
    return utils.get_set_from_perms(perms)


@pytest.fixture
def all_grouped_perms(db):
    perms = (PermissionGroup
             .objects
             .filter(permissions__content_type__isnull=False)
             .values_list(
                 'permissions__content_type__app_label',
                 'permissions__codename'))
    return utils.get_set_from_perms(perms)


@pytest.fixture
def initial_company_user_perms(company_user_perms, all_grouped_perms):
    return company_user_perms | all_grouped_perms


@pytest.fixture
def initial_company_user(base_user):
    utils.add_permission_initial_company_user(base_user)
    user = User.objects.get(id=base_user.id)
    return user
