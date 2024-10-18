from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model

import pytest

from permission import constants
from permission.models import PermissionGroup
from permission import utils
from tests.unittests.permission import expected

User = get_user_model()


@pytest.mark.parametrize(('group', 'expected'), (
    (
        'company_user',
        expected.EXPECTED_SET_COMPANY_USER_GROUP_PERMS
    ),
    (
        'job_seeker',
        expected.EXPECTED_SET_JOB_SEEKER_PERMS
    )
))
def test_user_groups_permissions(request, base_user, group, expected):
    assert not base_user.get_all_permissions()
    group = request.getfixturevalue(group)
    group.user_set.add(base_user)
    user = User.objects.get(id=base_user.id)
    assert user.get_all_permissions() == expected


@pytest.mark.parametrize(('group_name', 'expected'), (
    (
        constants.MANAGE_COMPANY_USERS_GROUP,
        {
            'change_companyuser',
            'view_companyuser',
            'add_companyuser',
            'delete_companyuser',
        }
    ),
    (
        constants.MANAGE_JOB_POSTINGS_GROUP,
        {
            'change_job',
            'add_job',
            'delete_job',
            'create_delayed_job',
            'set_job_is_cover_letter_required',
            'set_job_closing_date',
            'change_candidate',
            'delete_candidate',
            'add_candidate',
            'change_candidatestatus',
            'restore_candidate',
        }
    ),
    (
        constants.EDIT_COMPANY_PROFILE_GROUP,
        {
            'change_company',
            'change_company_logo'
        }
    ),
    (
        constants.PURCHASE_JSPROFILE_GROUP,
        {
            'purchase_js_profile',
        }
    )
))
def test_permissions_groups(db, group_name, expected):
    perms = (PermissionGroup.objects
                            .filter(name=group_name)
                            .values_list('permissions__codename', flat=True))
    assert set(perms) == expected


@pytest.mark.parametrize(('func', 'expected'), (
    (
        utils.add_permission_initial_company_user,
        'initial_company_user_perms',
    ),
))
def test_company_user_permissions(request, base_user, func, expected):
    expected = request.getfixturevalue(expected)
    func(base_user)
    user = User.objects.get(id=base_user.id)
    assert user.get_all_permissions() == expected


@pytest.mark.parametrize(('group_name', 'perms'), (
    (
        constants.MANAGE_COMPANY_USERS_GROUP,
        {
            'company.change_companyuser',
            'company.view_companyuser',
            'company.add_companyuser',
            'company.delete_companyuser',
        }
    ),
    (
        constants.MANAGE_JOB_POSTINGS_GROUP,
        {
            'job.change_job',
            'job.add_job',
            'job.delete_job',
            'candidate.change_candidate',
            'candidate.delete_candidate',
            'candidate.add_candidate',
            'candidate.restore_candidate'
        }
    ),
    (
        constants.EDIT_COMPANY_PROFILE_GROUP,
        {
            'company.change_company',
        }
    ),
    (
        constants.PURCHASE_JSPROFILE_GROUP,
        {
            'job_seeker.purchase_js_profile',
        }
    )
))
def test_remove_permissions_groups(
        group_name, perms, initial_company_user):
    all_perms = initial_company_user.get_all_permissions()
    assert perms.issubset(all_perms)

    group = PermissionGroup.objects.get(name=group_name)
    group.user_set.remove(initial_company_user)
    user = User.objects.get(id=initial_company_user.id)
    if perms:
        assert not perms.issubset(user.get_all_permissions())


def test_add_custom_permission_to_user(base_user, company_user):
    company_user.user_set.add(base_user)
    custom_perm = 'apply.start_autoapply'
    app_label, codename = custom_perm.split('.')
    perm = Permission.objects.get(
        codename=codename,
        content_type__app_label=app_label)
    utils.add_user_custom_permission(base_user, perm, 'add')
    user = User.objects.get(id=base_user.id)
    assert custom_perm in user.get_all_permissions()


def test_add_custom_permission_action_delete_to_user(base_user, company_user):
    company_user.user_set.add(base_user)
    custom_perm = 'survey.add_question'
    app_label, codename = custom_perm.split('.')
    perm = Permission.objects.get(
        codename=codename,
        content_type__app_label=app_label)
    utils.add_user_custom_permission(base_user, perm, 'delete')
    user = User.objects.get(id=base_user.id)
    assert custom_perm not in user.get_all_permissions()
