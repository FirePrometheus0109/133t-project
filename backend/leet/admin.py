# pylint: disable=too-many-arguments
import django.contrib.auth.models as auth_models
import django.contrib.sites.models as site_models
from django.contrib import admin
import allauth.socialaccount.models as all_auth_models
import rest_framework.authtoken.models as authtoken_models
import threadedcomments.models as threadedcomments_models
import notifications.models as notification_models
from rangefilter import filter as range_filter
from constance.admin import ConstanceAdmin, Config


class BaseAdminSite(admin.AdminSite):
    """Base class for admin site"""

    site_header = '133T Administration'


class BaseModelAdmin(admin.ModelAdmin):

    def delete_model(self, request, obj):
        obj.is_active = False
        obj.save()

    def delete_queryset(self, request, queryset):
        queryset.update(is_active=False)


base_admin_site = BaseAdminSite()


class AggregationsFilter(range_filter.DateRangeFilter):
    """
    Filter for Admin Reports. Should be used in reports
    with aggregation/annotation. It doesn't filter base instance
    (that's why just queryset is returned), but used in filters in
    Count, Sum, etc. functions
    """
    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(
            field, request, params, model, model_admin, field_path
        )
        self.title = 'Date'

    def queryset(self, request, queryset):
        return queryset


admin.site.unregister([Config])
admin.site.unregister(auth_models.User)
admin.site.unregister(auth_models.Group)
admin.site.unregister(site_models.Site)
admin.site.unregister(all_auth_models.SocialToken)
admin.site.unregister(all_auth_models.SocialAccount)
admin.site.unregister(all_auth_models.SocialApp)
admin.site.unregister(authtoken_models.Token)
admin.site.unregister(threadedcomments_models.ThreadedComment)
admin.site.unregister(notification_models.Notification)


@admin.register(Config, site=base_admin_site)
class _ConstanceAdmin(ConstanceAdmin):
    pass
