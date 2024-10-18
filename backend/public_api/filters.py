from django_filters.rest_framework import FilterSet, filters

from job.models import Skill


class SkillsFilterSet(FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Skill
        fields = ['name']
