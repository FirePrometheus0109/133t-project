from django.db import models as orm

from django_filters.rest_framework import filters

from job import models as job_models
from job import filters as job_filters
from apply import services


class AutoapplyJobFilter(job_filters.BaseJobFilterSet):
    exclude = filters.BaseInFilter(method='exclude_jobs')
    salary = filters.NumberFilter(method='filter_salary')
    include_company_names = filters.BaseInFilter(
        method='annotate_fav_companies'
    )
    exclude_company_names = filters.BaseInFilter(method='exclude_companies')

    def exclude_jobs(self, queryset, name, value):  # noqa
        value = self.data.getlist(name)
        return services.exclude_jobs(queryset, value)

    def annotate_fav_companies(self, queryset, name, value):
        value = self.data.getlist(name)

        # The company__name__in lookup didn't work in annotation.
        # So it's a workaround to annotate favorite companies.
        cases = [orm.When(orm.Q(company__name=company_name), then=True)
                 for company_name in value]
        is_fav_company = orm.Case(
            *cases,
            default=False, output_field=orm.BooleanField()
        )

        # Maybe it's worth to move ordering in other place
        return queryset.annotate(is_fav_company=is_fav_company)\
            .order_by('-is_fav_company')

    def exclude_companies(self, queryset, name, value):
        value = self.data.getlist(name)
        return queryset.exclude(company__name__in=value)

    def filter_salary(self, queryset, name, value):  # noqa
        qs = queryset.filter(
            orm.Q(salary_max__gte=value, salary_min__lte=value) |
            orm.Q(salary_max__isnull=True, salary_min__gte=value) |
            orm.Q(salary_max__gte=value, salary_min__isnull=True)
        )
        return qs

    class Meta:
        model = job_models.Job
        fields = (
            'state_id', 'city_id', 'exclude',
            'clearance', 'education', 'benefits',
            'exclude', 'salary', 'include_company_names',
            'exclude_company_names', 'state_id', 'city_id'
        )
