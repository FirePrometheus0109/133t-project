# pylint: disable=no-self-use
from django.contrib import admin
from comment import forms
from comment import models
from leet import admin as base_admin


class BaseCommentAdmin(admin.ModelAdmin):

    add_form = None
    search_fields = ('title', 'comment')
    list_filter = ('submit_date',)
    ordering = ('-submit_date',)
    readonly_fields = ('submit_date',)
    view_on_site = False

    def get_form(self, request, obj=None, change=False, **kwargs):
        # use special form during comment creation
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)

    def save_form(self, request, form, change):
        # extend form save method to pass user as argument, since django forms
        # don't have access to current user
        if change:
            return form.save(commit=False)
        return form.save(user=request.user, commit=False)

    def get_queryset(self, request):
        return (super()
                .get_queryset(request)
                .filter(is_removed=False)
                .select_related(
                    'content_type',
                    'user'))

    def delete_model(self, request, obj):
        obj.is_removed = True
        obj.save()

    def delete_queryset(self, request, queryset):
        queryset.update(is_removed=True)


@admin.register(models.JobComment, site=base_admin.base_admin_site)
class JobCommentAdmin(BaseCommentAdmin):

    add_form = forms.JobCommentCreationForm
    form = forms.JobCommentChangeForm

    list_display = (
        'user',
        'title',
        'comment',
        'job_title',
        'ban_status',
        'submit_date'
    )

    def job_title(self, obj):
        return obj.content_object.title
    job_title.short_description = 'Job'


@admin.register(models.JobSeekerComment, site=base_admin.base_admin_site)
class JobSeekerCommentAdmin(BaseCommentAdmin):

    add_form = forms.JobSeekerCommentCreationForm
    form = forms.JobSeekerCommentChangeForm

    list_display = (
        'user',
        'title',
        'comment',
        'job_seeker_name',
        'ban_status'
    )

    def job_seeker_name(self, obj):
        return obj.content_object.user.get_full_name()
    job_seeker_name.short_description = 'Job seeker'
