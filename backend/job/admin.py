# pylint: disable=no-self-use
from django.contrib import admin
from import_export import admin as import_export_admin

from job import formats
from job import forms
from job import models
from job import resources
from leet import admin as base_admin
from leet import mixins as base_mixins


class InlineSkills(admin.TabularInline):
    model = models.JobSkill
    formset = forms.JobSkillInlineForm
    extra = 0
    raw_id_fields = ('skill',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('job', 'skill')


@admin.register(models.Job, site=base_admin.base_admin_site)
class JobAdmin(base_admin.BaseModelAdmin):
    form = forms.JobForm
    inlines = (InlineSkills,)
    list_display = (
        'company_name',
        'title',
        'address_address',
        'created_at',
        'industry_name',
        'position_type',
        'education',
        'clearance',
        'experience',
        'salary_min',
        'salary_max',
        'salary_negotiable',
        'benefits',
        'travel',
        'status',
        'education_strict',
        'publish_date',
        'company_owner',
        'is_deleted',
        'deleted_at',
        'is_cover_letter_required',
        'closing_date',
    )
    list_filter = (
        'company',
        'created_at',
    )
    readonly_fields = ('deleted_at',)
    search_fields = (
        'title',
        'created_at',
        'location__address',
        'location__city__name',
        'location__country__name',
        'location__zip__code',
    )
    exclude = ('search_vector', 'location_search_vector')

    def company_name(self, obj):
        return obj.company.name
    company_name.admin_order_field = 'company'
    company_name.short_description = 'Company name'

    def address_address(self, obj):
        return obj.location.country.name
    address_address.short_description = 'Address'

    def industry_name(self, obj):
        return obj.industry.name
    industry_name.short_description = 'Industry'

    def company_owner(self, obj):
        return obj.owner.user.username if obj.owner is not None else ''
    company_owner.short_description = 'Owner'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related(
            'company',
            'owner__user',
            'industry',
            'location__country')


@admin.register(models.Industry, site=base_admin.base_admin_site)
class IndustryAdmin(base_mixins.ForbidDeleteModelAdminMixin, admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(models.Skill, site=base_admin.base_admin_site)
class SkillAdmin(import_export_admin.ImportExportMixin, admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'type'
    )
    list_filter = ('type',)
    search_fields = ('name', 'description')
    formats = (formats.CSVSemicolonDelimiter,)
    resource_class = resources.SkillResource
