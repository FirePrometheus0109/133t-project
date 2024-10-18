# pylint: disable=no-self-use,no-member
from django.conf import settings
from django.contrib import admin

from leet import admin as base_admin
from leet import enums
from subscription import forms
from subscription import models
from subscription import services
from subscription import utils


# TODO(m.nizovtsova): customize form for Stripe errors handling
@admin.register(models.Plan, site=base_admin.base_admin_site)
class PlanAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'job_seekers_count',
        'jobs_count',
        'is_custom',
        'price',
        'company',
        'is_active',
        'formatted_deletion_date',
        'notes',
        'is_reporting_enabled',
        'users_number',
    )
    ordering = ('price',)
    delete_confirmation_template = (
        'admin/subscriptions/delete_plan_confirmation.html'
    )
    change_form_template = 'admin/subscriptions/change_plan_form.html'
    actions = None

    def formatted_deletion_date(self, obj):
        return (
            obj.deletion_date.strftime(settings.DEFAULT_SERVER_DATE_FORMAT)
            if obj.deletion_date else obj.deletion_date
        )
    formatted_deletion_date.admin_order_field = 'deletion_date'
    formatted_deletion_date.short_description = 'Will be deleted from'

    def notes(self, obj):
        notes = None
        if obj.new_price:
            price_apply_date_formatted = obj.price_apply_date.strftime(
                settings.DEFAULT_SERVER_DATE_FORMAT
            )
            notes = 'New price {}$ is going to be applied on {}.'.format(
                obj.new_price,
                price_apply_date_formatted
            )
        return notes
    notes.short_description = 'Notes'

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = ()
        if obj:
            readonly_fields = (
                'name',
                'job_seekers_count',
                'jobs_count',
                'is_custom',
                'company'
            )
            # only enabling of custom plans is allowed for 'is_active' flag
            if not obj.is_custom or obj.is_active:
                readonly_fields += ('is_active',)
        return readonly_fields

    def get_form(self, request, obj=None, change=False, **kwargs):
        kwargs['form'] = forms.UpdatePlanForm if obj else forms.CreatePlanForm
        return super().get_form(request, obj, change, **kwargs)

    def render_delete_form(self, request, context):
        context.update(
            {'deletion_date': utils.get_plan_change_or_delete_apply_date()}
        )
        return super().render_delete_form(request, context)

    def get_queryset(self, request):
        qs = self.model.admin_objects.exclude(is_deleted=True)
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def delete_model(self, request, obj):
        obj.deletion_date = utils.get_plan_change_or_delete_apply_date()
        obj.save()
        self._delete_scheduled_subscriptions(obj)
        utils.notify_users_about_plan_deletion(obj)

    @staticmethod
    def _delete_scheduled_subscriptions(plan):
        scheduled_subscriptions = models.Subscription.objects.filter(
            plan=plan, status=enums.SubscriptionStatusEnum.SCHEDULED.name
        )
        for subscription in scheduled_subscriptions:
            service = services.SubscribeService(subscription.owner)
            service.unsubscribe(subscription)

    def get_deleted_objects(self, objs, request):
        to_delete, model_count, perms_needed, protected = (  # noqa
            super().get_deleted_objects(objs, request)
        )
        # ignore protected because of scheduled delete,
        # replace that with empty list
        return to_delete, model_count, perms_needed, []

    def has_delete_permission(self, request, obj=None):
        if obj:
            # if deletion date was set, obj is already deleted
            # and admin can't delete this
            return not obj.deletion_date
        return True

    def has_change_permission(self, request, obj=None):
        if obj:
            # deny changes for deleted package
            return not obj.deletion_date
        return True


@admin.register(models.Subscription, site=base_admin.base_admin_site)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'company',
        'plan',
        'is_trial',
        'date_start',
        'date_end',
        'status',
        'stripe_id',
    )
    list_editable = ('date_end',)

    def company(self, obj):
        return obj.customer.company.name
    company.short_description = 'Company'

    def plan(self, obj):
        return obj.plan.name
    plan.short_description = 'Plan'

    def has_add_permission(self, request):
        return False
