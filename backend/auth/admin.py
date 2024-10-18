# pylint: disable=no-member,no-self-use
from allauth.account import admin as allauth_admin
from allauth.account import models as allauth_models
from django.contrib import admin
from django.contrib.auth import admin as django_auth_admin

from auth import filters
from auth import forms
from auth import models
from auth import ordering
from auth import services
from company import models as company_models
from company import utils as company_utils
from job_seeker import models as js_models
from leet import admin as base_admin
from leet import enums
from leet import mixins
from permission import utils


class CompanyUserInline(admin.StackedInline):
    model = company_models.CompanyUser
    formset = forms.CompanyUserInlineFormset


class JobSeekerInline(admin.StackedInline):
    model = js_models.JobSeeker
    formset = forms.JobSeekerInlineFormset
    readonly_fields = ('deleted_at',)
    exclude = ('search_vector', 'location_search_vector', 'is_password_set')


@admin.register(models.ProxyUser, site=base_admin.base_admin_site)
class AuthUserAdmin(django_auth_admin.UserAdmin):
    add_form = None
    user_creation_forms = {
        'default': forms.CreateUserForm,
        enums.AuthGroupsEnum.JOB_SEEKER.value: forms.CreateJobSeekerForm,
        enums.AuthGroupsEnum.COMPANY_USER.value: forms.CreateCompanyUserForm
    }
    form = forms.ChangeUserForm

    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'date_joined',
        'user_status',
    )
    readonly_fields = (
        'date_joined',
        'last_login',
    )

    list_filter = (
        filters.UserFilter,
        'is_superuser',
        'is_active',
        'date_joined',
    )
    sortable_by = (
        'username',
        'date_joined',
        'user_status'
    )
    search_fields = (
        'username',
        'date_joined',
        'first_name',
        'last_name',
        'email'
    )
    inlines = []

    def user_status(self, obj):
        if utils.is_company_user(obj):
            return enums.UserTypeEnum.COMPANY_USER.value
        if utils.is_job_seeker(obj):
            return enums.UserTypeEnum.JOB_SEEKER.value
        return enums.UserTypeEnum.ADMIN.value

    user_status.short_description = 'Status'
    user_status.admin_order_field = ordering.USER_LIST_ORDERING

    def get_fieldsets(self, request, obj=None):
        if not obj:
            fieldsets = {
                'classes': ('wide',),
                'fields': ['username', 'password1', 'password2'],
            }
            if (self.add_form == self.user_creation_forms[
                    enums.AuthGroupsEnum.COMPANY_USER.value]):
                fieldsets['fields'].append(('company', 'is_owner'))
            return ((None, fieldsets),)
        return super().get_fieldsets(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        self.update_inlines(obj)
        if obj is None:
            user_type = request.GET.get('type', 'default')
            self.add_form = self.user_creation_forms[user_type]
        return super().get_form(request, obj, **kwargs)

    def update_inlines(self, obj):
        self.inlines.clear()
        if utils.is_job_seeker(obj):
            self.inlines.append(JobSeekerInline)
        elif utils.is_company_user(obj):
            self.inlines.append(CompanyUserInline)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_active=True).select_related(
            'auth_token',
            'deletion_reason',
            'company_user',
            'job_seeker',
        )

    def delete_model(self, request, obj):
        if utils.is_job_seeker(obj):
            js_service = services.UserAccountService(obj)
            js_service.soft_delete_user_account()
        elif utils.is_company_user(obj):
            company_utils.soft_delete_company_user(obj.company_user)
        else:
            obj.is_active = False
            obj.save()

    def delete_queryset(self, request, queryset):
        for user in queryset:
            self.delete_model(request, user)


@admin.register(allauth_models.EmailAddress, site=base_admin.base_admin_site)
class EmailAddressAdmin(allauth_admin.EmailAddressAdmin):
    pass


@admin.register(models.DeletionReason, site=base_admin.base_admin_site)
class DeletionReasonAdmin(mixins.AllowReadOnlyModelAdminMixin,
                          admin.ModelAdmin):
    pass
