# pylint: disable=no-self-use
from django.conf import settings
from django.contrib import admin
from django.db import models as orm
from django.db.models import functions
from rangefilter import filter as range_filter

from company import models
from company import services
from leet import admin as base_admin
from leet import constants
from leet import enums
from leet import mixins


@admin.register(models.Company, site=base_admin.base_admin_site)
class CompanyAdmin(base_admin.BaseModelAdmin):
    fields = (
        'name',
        'photo',
        'industry',
        'description',
        'address',
        'phone',
        'fax',
        'website',
        'email',
        'ban_status',
        'purchased_job_seekers'
    )
    readonly_fields = ('purchased_job_seekers',)
    list_display = (
        'name',
        'photo',
        'industry',
        'description',
        'address',
        'phone',
        'fax',
        'website',
        'email',
        'ban_status'
    )
    list_filter = ('industry',)
    search_fields = ('name',)
    ordering = ('-created_at',)

    def save_form(self, request, form, change):
        if 'ban_status' in form.changed_data:
            ban_status = form.cleaned_data.get('ban_status')
            company_service = services.CompanyService(form.instance)
            if ban_status == enums.BanStatusEnum.BANNED.name:  # noqa
                company_service.ban_company_entities()
                # TODO: (a.finsky) here is the only point for the company ban,
                # this is
                # where the subscription should stop
            elif ban_status == enums.BanStatusEnum.ACTIVE.name:  # noqa
                # TODO: (a.finsky) same entry, but for unban company,
                # unban description:
                # When Company is un-banned, then Company should select
                # subscription once again. Billing cycle will start at the
                # beginning.
                company_service.unban_company_entities()

        return super().save_form(request, form, change)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related(
            'industry',
            'address',
            'customer'
        )


@admin.register(models.CompanyActivityReport, site=base_admin.base_admin_site)
class CompanyActivityReportsAdmin(
        mixins.ReportAdminMixin,
        mixins.AllowReadOnlyModelAdminMixin,
        admin.ModelAdmin):
    list_display = ('name', 'created_jobs_count', 'sent_offers_count')
    list_filter = (
        (
            'created_at', base_admin.AggregationsFilter,
        ),
        'name',
    )
    csv_filename = 'CompanyActivityReport'

    def created_jobs_count(self, company):
        return company.created_jobs_count
    created_jobs_count.short_description = 'Created jobs count'

    def sent_offers_count(self, company):
        return company.sent_offers_count
    sent_offers_count.short_description = 'Sent offers count'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        date_filters = self.get_date_filters(request.GET.dict())
        jobs_count_filter = {}
        offers_count_filter = {
            'job__candidates__workflow_steps__status__name': constants.CANDIDATE_STATUS_OFFERED  # noqa
        }
        from_date = date_filters.get('created_at__gte')
        until_date = date_filters.get('created_at__lte')
        if from_date:
            jobs_count_filter.update({'job__created_at__date__gte': from_date})
            offers_count_filter.update(
                {'job__candidates__workflow_steps__created_at__date__gte': from_date}  # noqa
            )
        if until_date:
            jobs_count_filter.update({'job__created_at__date__lte': until_date})  # noqa
            offers_count_filter.update(
                {'job__candidates__workflow_steps__created_at__date__lte': until_date}  # noqa
            )
        annotations = {
            'created_jobs_count': orm.Count(
                'job',
                filter=orm.Q(**jobs_count_filter),
                distinct=True
            ),
            'sent_offers_count': orm.Count(
                'job__candidates',
                filter=orm.Q(**offers_count_filter),
                distinct=True
            )
        }
        qs = qs.annotate(
            **annotations
        ).order_by('-created_jobs_count')
        return qs

    def get_data_for_csv_report(self, request):
        filters = request.GET.dict()
        name_filter = filters.get('name')
        queryset = self.get_queryset(request)
        if name_filter:
            queryset = queryset.filter(name=name_filter)
        return queryset


@admin.register(models.CompanyRegistrationReport,
                site=base_admin.base_admin_site)
class CompanyRegistrationReportsAdmin(
        mixins.ReportAdminMixin,
        mixins.AllowReadOnlyModelAdminMixin,
        admin.ModelAdmin):
    list_display = (
        'name',
        'created_at'
    )
    list_filter = (('created_at', range_filter.DateRangeFilter),)
    csv_filename = 'CompanyRegistrationReport'


@admin.register(models.CompanyTransactionsReport,
                site=base_admin.base_admin_site)
class CompanyTransactionReportsAdmin(
        mixins.ReportAdminMixin,
        mixins.AllowReadOnlyModelAdminMixin,
        admin.ModelAdmin):
    list_filter = (
        ('created_at', base_admin.AggregationsFilter),
        'name',
    )
    change_list_template = 'admin/company/company_transactions_list.html'

    csv_fields = ('name', 'amount', 'description', 'date')
    csv_filename = 'CompanyTransactionsReport'

    def get_data_for_csv_report(self, request):
        filters = request.GET.dict()
        name_filter = filters.get('name')
        queryset = self.get_queryset(request)
        if name_filter:
            queryset = queryset.filter(name=name_filter)
        report = self._generate_report(queryset, filters)
        data_for_export = []
        for company_report in report:
            for invoice in company_report['invoices']:
                data_for_export.append({
                    'name': company_report['company'].name,
                    'amount': invoice.amount,
                    'description': invoice.description,
                    'date': invoice.datetime_of_payment.strftime(
                        settings.DEFAULT_SERVER_DATETIME_FORMAT)
                })
        return data_for_export

    def _generate_report(self, queryset, filters):
        data = []
        invoice_filters = self._get_invoice_filters(filters)
        for company in queryset:
            invoices = []
            if hasattr(company, 'customer'):
                invoices = company.customer.invoices.filter(**invoice_filters)
            data.append({
                'company': company,
                'invoices': invoices
            })
        return data

    def _get_invoice_filters(self, filters):
        filters = self.get_date_filters(filters)
        invoice_filters = {}
        from_date = filters.get('created_at__gte')
        until_date = filters.get('created_at__lte')
        if from_date:
            invoice_filters.update({
                'datetime_of_payment__date__gte': from_date
            })
        if until_date:
            invoice_filters.update({
                'datetime_of_payment__date__lte': until_date  # noqa
            })
        return invoice_filters

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        invoice_filters = self._get_invoice_filters(request.GET.dict())
        invoice_filters = {
            'customer__invoices__{}'.format(key): value
            for key, value in invoice_filters.items()
        }
        total = functions.Coalesce(orm.Sum('customer__invoices__amount',
                                           filter=orm.Q(**invoice_filters)), 0)
        qs = (qs
              .select_related('customer')
              .annotate(total=total)
              .order_by('-total'))
        return qs

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)
        try:
            result_list = response.context_data['cl'].result_list
        except (AttributeError, KeyError):
            return response
        response.context_data['report'] = self._generate_report(
            result_list, request.GET.dict()
        )
        return response
