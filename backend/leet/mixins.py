# pylint: disable=no-self-use
import csv
import datetime
from operator import getitem

from dateutil import parser
from django import forms
from django import http
from django.conf import settings
from django.core import exceptions
from django.urls import path
from rest_framework import exceptions as drf_exceptions


class ValidationModelFormMixin:
    """
    Extend django form validation to handle `ValidationError` from
    `rest_framework`
    """

    def add_error(self, field_name, exc):
        exc = exc.detail[0] if hasattr(exc, 'detail') and exc.detail else exc
        super().add_error(field_name, exc)

    def _clean_fields(self):
        for name, field in self.fields.items():
            if field.disabled:
                value = self.get_initial_for_field(field, name)
            else:
                value = field.widget.value_from_datadict(
                    self.data, self.files, self.add_prefix(name))
            try:
                if isinstance(field, forms.FileField):
                    initial = self.get_initial_for_field(field, name)
                    value = field.clean(value, initial)
                else:
                    value = field.clean(value)
                self.cleaned_data[name] = value
                if hasattr(self, 'clean_%s' % name):
                    value = getattr(self, 'clean_%s' % name)()
                    self.cleaned_data[name] = value
            except (exceptions.ValidationError,
                    drf_exceptions.ValidationError) as e:
                self.add_error(name, e)

    def _clean_form(self):
        try:
            super()._clean_form()
        except drf_exceptions.ValidationError as e:
            self.add_error(None, e)


class ForbidDeleteModelAdminMixin:

    def has_delete_permission(self, request, obj=None):
        return False


class AllowReadOnlyModelAdminMixin(ForbidDeleteModelAdminMixin):

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


class CSVFileMixin:
    """Mixin return csv response."""

    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(
            request, response, *args, **kwargs)
        if response.accepted_renderer.format == 'csv':
            response['content-disposition'] = 'attachment; filename={}'.format(
                self.get_filename())
        return response

    def get_filename(self):
        date = datetime.date.today().strftime(
            settings.DEFAULT_SERVER_DATE_FORMAT)
        return self.filename_template.format(date)


class ReportAdminMixin:
    sortable_by = ()
    list_display_links = None
    change_list_template = 'admin/reports_list.html'
    csv_filename = 'Report'
    csv_fields = ()

    def get_urls(self):
        urls = super().get_urls()
        export_to_csv_url = path('export-to-scv/', self.export_to_csv)
        return [export_to_csv_url] + urls

    @staticmethod
    def get_date_filters(filters):
        date_filter_names = ('created_at__gte', 'created_at__lte')
        date_filters = {
            key: value for key, value in filters.items()
            if key in date_filter_names and value
        }
        date_filters = {
            key: parser.parse(value) for key, value in date_filters.items()
        }
        return date_filters

    def get_csv_fields(self):
        return self.csv_fields if self.csv_fields else self.list_display

    def get_data_for_csv_report(self, request):
        filters = request.GET.dict()
        name_filter = filters.get('name')
        date_filters = self.get_date_filters(filters)
        from_date = date_filters.get('created_at__gte')
        until_date = date_filters.get('created_at__lte')
        queryset = self.get_queryset(request)
        if from_date:
            queryset = queryset.filter(created_at__date__gte=from_date)
        if until_date:
            queryset = queryset.filter(created_at__date__lte=until_date)
        if name_filter:
            queryset = queryset.filter(name=name_filter)
        return queryset

    def export_to_csv(self, request):
        csv_fields = self.get_csv_fields()
        data = self.get_data_for_csv_report(request)
        date = datetime.date.today().strftime(
            settings.DEFAULT_SERVER_DATE_FORMAT)
        response = http.HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = (
            'attachment; filename={}_{}.csv'.format(self.csv_filename, date)
        )
        writer = csv.writer(response)

        headers = (' '.join(
            word.capitalize() for word in field.split('_')
        ) for field in csv_fields)
        writer.writerow(headers)
        for obj in data:
            get_method = getitem if isinstance(obj, dict) else getattr
            writer.writerow(
                [get_method(obj, field) for field in csv_fields])

        return response
