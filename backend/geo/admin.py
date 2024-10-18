# pylint: disable=no-self-use
from django.contrib import admin
from django.utils import html

from geo import models
from leet import admin as base_admin
from leet import mixins as base_mixins


@admin.register(models.Address, site=base_admin.base_admin_site)
class AddressAdmin(base_mixins.ForbidDeleteModelAdminMixin, admin.ModelAdmin):

    list_display = ('edit_icon', 'address', 'country', 'city', 'zip')
    raw_id_fields = ('zip', 'city')
    ordering = ('country__name',)

    def edit_icon(self, obj):  # noqa
        return html.format_html('<span class="changelink">Edit</span>')
    edit_icon.short_description = ''

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('country', 'city', 'zip')


@admin.register(models.Country, site=base_admin.base_admin_site)
class CountryAdmin(base_mixins.ForbidDeleteModelAdminMixin, admin.ModelAdmin):

    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(models.State, site=base_admin.base_admin_site)
class StateAdmin(base_mixins.ForbidDeleteModelAdminMixin, admin.ModelAdmin):

    list_display = ('name', 'abbreviation', 'county_name')
    search_fields = ('name',)
    ordering = ('name',)

    def county_name(self, obj):
        return obj.country.name
    county_name.short_description = 'Country'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('country')


@admin.register(models.City, site=base_admin.base_admin_site)
class CityAdmin(base_mixins.ForbidDeleteModelAdminMixin, admin.ModelAdmin):

    list_display = ('name', 'state')
    search_fields = ('name',)
    ordering = ('name',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('state')


@admin.register(models.Zip, site=base_admin.base_admin_site)
class ZipAdmin(base_mixins.ForbidDeleteModelAdminMixin, admin.ModelAdmin):

    list_display = ('code', 'city_name')
    raw_id_fields = ('city',)
    search_fields = ('code',)
    ordering = ('code',)

    def city_name(self, obj):
        return obj.city.name
    city_name.short_description = 'City'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('city')
