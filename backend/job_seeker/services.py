from django.db import models as orm

from job_seeker import constants
from leet import utils


def is_profile_public(job_seeker):
    map_lists = (
        ['user', 'first_name'],
        ['user', 'last_name'],
        ['user', 'email'],
        ['address', 'country'],
        ['address', 'city'],
        ['address', 'zip'],
        ['position_type'],
        ['education']
    )
    for i in map_lists:
        if not utils.get_from_nested_structure(job_seeker, i, func=getattr):
            return False
    return job_seeker.skills.count() >= 3


def set_the_rest_cover_letters_as_not_default(instance, validated_data):
    if validated_data.get('is_default'):
        instance.owner.cover_letters.filter(
            ~orm.Q(id=instance.id)
        ).update(is_default=False)


def _single_value_completion_rule(**kwargs):
    """
    Just return bool value.

    Use this rule for check completion usual fields.
    """
    return bool(kwargs['value'])


def _many_values_completion_rule(**kwargs):
    """
    If field name is not 'skills' and field has at least one value
    else return True if field 'skills' has at least 3 values.

    Use this rule for check completion 'many to many' and 'one to many' fields.
    """
    field_name = kwargs['field_name']
    value = kwargs['value']
    if field_name == 'skills':
        return value.count() >= 3
    return value.exists()


def _any_education_exists_rule(**kwargs):
    """Education and Certifications have special rule for check completion.
    A profile should be contain at least one entry in table 'Education' or
    'Certification'.
    """
    profile = kwargs['profile']
    return profile.educations.exists() or profile.certifications.exists()


def _get_result(empty_fields, filled_fields, weights):
    """
    Return a job seeker's profile completion.
    :param empty_fields: dict, keys - field names,
                               values - names to representation.
    :param filled_fields: set, names of fields which have been filled.
    :param weights: dict, key - field name, value - weight.
    :return: dict
    """
    result = {
        'total_complete': 0,
        'need_complete': [],
    }
    for name, to_repr_name in empty_fields.items():
        result['need_complete'].append({
            'field': ', '.join(to_repr_name).replace('_', ' '),
            'add_percents': weights[name]
        })
        # remove field name for filled if it is part of 'complex' field which
        # are calculated as one field for percentage.
        # 'complex' fields: first_name, last_name,
        #                   country, city, state
        if name in filled_fields:
            filled_fields.remove(name)
    for name in filled_fields:
        result['total_complete'] += weights[name]
    return result


def get_profile_completion(profile):
    """Return percentage of profile completion and fields with weights which
    should be complete.

    :param profile: instance of JobSeeker model
    Example result:
    {
        'total_compelete': 80
        'need_complete': [
            {
                'field': 'about'
                'add_percents': 10,
            },
            {
                'field': 'educations'
                'add_percents': 10,
            },
        ],
    }.
    """
    weights = constants.FILEDS_WEIGHTS_FOR_PROFILE_COMPLETION
    all_maps_lists = [
        constants.MAP_LISTS_OF_SINGLE_VALUE_FIELDS,
        constants.MAP_LISTS_OF_MANY_VALUES_FIELDS,
        constants.MAP_LISTS_SPECIAL_RULES_VALUES_FIELDS,
    ]
    rules = [
        _single_value_completion_rule,
        _many_values_completion_rule,
        _any_education_exists_rule,
    ]
    empty_fields = {}
    filled_fields = set()

    for map_lists, rule in zip(all_maps_lists, rules):
        for map_list in map_lists:
            field_name = map_list[0]
            value = utils.get_from_nested_structure(
                profile, map_list, func=getattr)

            if rule(value=value, field_name=field_name, profile=profile):
                filled_fields.add(field_name)
            else:
                to_repr_name = map_list[-1].capitalize()
                if field_name in empty_fields:
                    empty_fields[field_name].append(to_repr_name)
                else:
                    empty_fields[field_name] = [to_repr_name]
    result = _get_result(empty_fields, filled_fields, weights)
    return result


def group_views_qs_by_company(queryset):
    """
    Job seeker's profile is viewed when any company user opens
    profile only first time.
    """
    first_views = (queryset
                   .values(
                       'job_seeker_id',
                       'company_user__company__id')
                   .annotate(
                       _created_at=orm.Min('created_at')))
    return (queryset.filter(created_at__in=first_views.values('_created_at'))
                    .order_by('-created_at'))
