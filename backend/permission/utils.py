# pylint: disable=no-member
from itertools import groupby

from django.contrib.auth import models as auth_models
from django.contrib.contenttypes import models as ct_models

from leet import enums
from permission import models


def get_permission_object(apps, app_label, model_name, perm_names):
    """
    Use this function only for creating new permissions.
    Only in migrations.
    :param model_name: model's name, str
    :param perm_names: for example: ('add_job', 'Can add job')
    :return: permission object
    """
    try:
        model = apps.get_model(app_label, model_name)
        content_type = ct_models.ContentType.objects.get_for_model(model)
    except LookupError:
        content_type, _ = ct_models.ContentType.objects.get_or_create(
            app_label=app_label,
            model=model_name)
    perm, _ = auth_models.Permission.objects.get_or_create(
        codename=perm_names[0],
        name=perm_names[1],
        content_type=content_type
    )
    return perm


def get_set_from_perms(perms):
    """
    Return set of permissions.
    :param perms: Iterator of Permission instances
    :return: set of perms. {'job.add_job', 'job.view_job'}
    """
    return {'%s.%s' % (ct, name) for (ct, name) in perms}


def is_job_seeker(user):
    return hasattr(user, 'job_seeker')


def is_company_user(user):
    return hasattr(user, 'company_user')


def add_user_to_company_user_group(user):
    """Add to company user default company user permissions."""
    company_user = auth_models.Group.objects.get(name='company_user')
    company_user.user_set.add(user)
    company_user.save()


def add_permission_initial_company_user(user):
    """Add initial company user in all company groups."""
    add_user_to_company_user_group(user)
    groups = models.PermissionGroup.objects.all()
    user.groups.add(*groups)
    user.save()
    return user


def add_permission_company_user(user, permissions_groups):
    """Add company user selected permissionsgroups."""
    user.groups.clear()
    add_user_to_company_user_group(user)
    user.groups.add(*permissions_groups)
    user.save()
    return user


def get_custom_perms_by_action(user, action):
    """
    Get custom user permissions.
    This permissions are added to directly to user.
    :param user: User instance.
    :param action: 'add' ot 'delete', str.
    """
    perms = (
        models.UserCustomPermission.objects
                                   .filter(action=action,
                                           user=user)
                                   .values_list(
                                       'permission__content_type__app_label',
                                       'permission__codename')
                                   .order_by('id')
    )
    return perms


def get_user_custom_permissions(user):
    """Return custom user permissions grouped by action."""
    add_perms = get_custom_perms_by_action(user, enums.ActionEnum.ADD.value)
    remove_perms = get_custom_perms_by_action(
        user, enums.ActionEnum.DELETE.value)
    return {
        enums.ActionEnum.ADD.value: get_set_from_perms(add_perms),
        enums.ActionEnum.DELETE.value: get_set_from_perms(remove_perms)
    }


def add_user_custom_permission(user, perm, action, reason=None):
    """
    Add custom permission with action to user.
    :param user: User instance.
    :param perm: Permission instance.
    :param action: 'add' ot 'delete', str.
    :param reason: Reason why this permission is added or deleted, str.
    :return: UserCustomPermission instance.
    """
    custom_perm, _ = (models.UserCustomPermission.objects
                            .update_or_create(
                                user=user,
                                permission=perm,
                                defaults={'action': action,
                                          'reason': reason}))
    return custom_perm


def delete_permissions_for_user_list(users, permissions_list, reason):
    for user in users:
        for permission_name in permissions_list:
            app_label, codename = permission_name.split('.')
            perm = auth_models.Permission.objects.get(
                codename=codename,
                content_type__app_label=app_label)
            add_user_custom_permission(
                user=user, perm=perm,
                action=enums.ActionEnum.DELETE.value,  # noqa
                reason=reason
            )


def union_user_perms_with_custom_perms(perms, custom_perms):
    """Return user permissions after adding and removing custom permissions."""
    perms |= custom_perms[enums.ActionEnum.ADD.value]
    perms -= custom_perms[enums.ActionEnum.DELETE.value]
    return perms


def get_all_user_permissions_qs(user):
    """
    Return queryset of all actual certain user permissions on leet project.
    """
    perms = user.get_all_permissions()
    filter_data = {
        'content_type__app_label__in': [i.split('.')[0] for i in perms],
        'codename__in': [i.split('.')[1] for i in perms],
    }
    perms_qs = auth_models.Permission.objects.filter(**filter_data)
    return perms_qs


def group_perms_groups_for_response(permissions_groups):
    result = []
    for title, groups in groupby(permissions_groups, key=lambda i: i['title']):
        group = {
            'title': title,
            'permissions': [{
                'id': g['id'],
                'name': g['name'],
                'description': g['description']
            } for g in groups]
        }
        result.append(group)
    return result
