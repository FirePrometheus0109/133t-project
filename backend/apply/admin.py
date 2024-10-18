from django.contrib import admin

from apply import models
from leet import admin as base_admin
from leet import mixins


@admin.register(models.Apply, site=base_admin.base_admin_site)
class ApplyAdmin(mixins.AllowReadOnlyModelAdminMixin,
                 base_admin.BaseModelAdmin):
    pass


@admin.register(models.Autoapply, site=base_admin.base_admin_site)
class AutoApplyAdmin(mixins.AllowReadOnlyModelAdminMixin,
                     base_admin.BaseModelAdmin):
    pass
