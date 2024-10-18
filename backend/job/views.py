import coreapi
import coreschema
from django import shortcuts
from django_filters import rest_framework as dj_filters
from rest_framework import filters as drf_filters
from rest_framework import generics
from rest_framework import permissions as drf_permissions
from rest_framework import response
from rest_framework import schemas
from rest_framework import status
from rest_framework import views as drf_views
from rest_framework import viewsets
from rest_framework.response import Response

from job import constants
from job import filters
from job import models
from job import permissions as job_permissions
from job import renderers
from job import serializers
from job import services
from job import validators
from leet import enums
from leet import mixins
from leet import services as core_services
from permission import permissions
from permission import utils


def get_company(request):
    return request.user.company_user.company



class DummyJobView(generics.CreateAPIView):
    """Endpoint for test purposes to create a lot of dummy jobs."""
    permission_classes = (
        drf_permissions.IsAuthenticated,
        job_permissions.JobPermission,
        job_permissions.CreateJobWithDelayedStatusPermission,
        job_permissions.CreateJobWithCoverLetterRequiredPermission,
        job_permissions.CreateJobWithClosingDatePermission,
        permissions.HasSubscription
    )
    serializer_class = serializers.JobDummySerializer
    queryset = models.Job.objects.all()

    def create(self, request, *args, **kwargs):
        if utils.is_company_user(self.request.user):
            company = get_company(self.request)
        else:
            return Response({'error': 'Only company can create jobs.'})
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        location_data =  {'country_id': 1, 'address': None, 'city_id': 31832, 'zip_id': 47544}
        location_serializer = serializers.LocationSerializer()
        jobs_data = []
        for n in range(data['amount']):
            title = f'{data["title"]} {n}'
            location = location_serializer.create(location_data)
            job_data = {
                'company': company,
                'description': "Created in test purposes",
                'title': title,
                'location': location,
                'position_type': enums.PositionTypesEnum.FULL_TIME.name,
                'industry': models.Industry.objects.first(),
                'owner': request.user.company_user,
                'status': enums.JobStatusEnum.ACTIVE.name
            }
            jobs_data.append(job_data)
        models.Job.objects.bulk_create(models.Job(**obj) for obj in jobs_data)
        return Response({}, status=status.HTTP_201_CREATED)


class JobViewSet(viewsets.ModelViewSet):
    """
    list:
        View company list Jobs.

        default filters:
        api/v1/job/?status=ACTIVE

        filter by status:
        api/v1/job/?status=ACTIVE
        api/v1/job/?status=DELAYED
        api/v1/job/?status=DRAFT
        api/v1/job/?status=CLOSED

        filter by author:
        api/v1/job/
        api/v1/job/?owner=1&owner=2

        filter by company_id:
        api/v1/job/?company_id=1

        For company user job list contains only company's jobs.

        Can combine filters

        ordering:
        api/v1/job/?ordering=publish_date
        api/v1/job/?ordering=-created_at
        api/v1/job/?ordering=-matching_percent
        api/v1/job/?ordering=title
        api/v1/job/?ordering=status
        api/v1/job/?ordering=owner__user__first_name
        api/v1/job/?ordering=-modified_at

        maintain search by job title, company name, skills and location
        api/v1/job/?search=weird_input

    destroy:
        Errors:
        If user tries to delete already deleted job:
            'You can not delete already deleted job.'
    """
    permission_classes = (
        drf_permissions.IsAuthenticated,
        job_permissions.JobPermission,
        job_permissions.CreateJobWithDelayedStatusPermission,
        job_permissions.CreateJobWithCoverLetterRequiredPermission,
        job_permissions.CreateJobWithClosingDatePermission,
        permissions.HasSubscription
    )
    ordering_fields = (
        'rank',
        'matching_percent',
        'publish_date',
        'created_at',
        'title',
        'status',
        'owner__user__first_name',
        'modified_at'
    )
    search_fields = (
        'title',
    )
    filterset_class = filters.JobFilterSet

    def set_filter_backends(self):
        if utils.is_job_seeker(self.request.user):
            self.filter_backends = (
                dj_filters.DjangoFilterBackend,
                filters.FullTextSearchBackend,
                filters.JobListOrderingFilterBackend
            )
        else:
            self.filter_backends = (
                dj_filters.DjangoFilterBackend,
                filters.FullTextSearchBackend,
                filters.CompanyUserJobListOrderingFilterBackend,
                drf_filters.OrderingFilter,
            )

    def get_queryset(self):
        if utils.is_company_user(self.request.user):
            company = get_company(self.request)
            return company.jobs.get_all_with_relations()
        job_seeker = self.request.user.job_seeker
        qs = models.Job.objects.get_published()
        qs = core_services.annotate_jobs_with_matching_percent(job_seeker, qs)
        return qs

    def get_serializer_class(self):
        if utils.is_job_seeker(self.request.user):
            if self.action == 'list':
                return serializers.JobListJobSeekerSerializer
            return serializers.JobDetailsJobSeekerSerializer
        return serializers.JobCompanyUserSerializer

    def retrieve(self, request, *args, **kwargs):
        """View jobs details.

            If job seeker views job, create entry about view.
        """
        job = self.get_object()
        if utils.is_job_seeker(request.user):
            if job.ban_status == enums.BanStatusEnum.BANNED.name:  # noqa
                return response.Response(
                    data=constants.JOB_BANNED_ERROR,
                    status=status.HTTP_403_FORBIDDEN)

            request.user.job_seeker.viewjob_set.create(job=job)
        serializer = self.get_serializer(job)
        return response.Response(serializer.data)

    def list(self, request, *args, **kwargs):
        """
        View jobs list.
        Save JobSearch on each job seeker request
        """
        list_response = super().list(request, args, kwargs)
        if utils.is_job_seeker(request.user):
            services.save_job_search(
                request.user.job_seeker, request.query_params

            )
        return list_response

    def partial_update(self, request, *args, **kwargs):
        """
        Job can have questions, that's the reason why it's needed to disable
        PATCH method.
        For example:
            job has 4 questions
            and front-end send data for partial update one question.
            On back-end it's difficult to check that its only update one
            question or three questions should be deleted and one question
            should be changed.
        Only PUT method is available for updating of job.
        """
        return self.http_method_not_allowed(request, *args, **kwargs)

    def get_serializer_context(self):
        context = super().get_serializer_context()

        if utils.is_job_seeker(self.request.user):
            context['js_skills'] = self.request.user.job_seeker.skills.all()
        if utils.is_company_user(self.request.user):
            context['company'] = get_company(self.request)

        return context

    def perform_destroy(self, instance):
        validators.validate_job_is_not_already_deleted(instance)
        services.soft_delete_job(instance, self.request.user)

    def filter_queryset(self, queryset):
        if self.action == 'list':
            self.set_filter_backends()
        return super().filter_queryset(queryset)


class JobViewersView(generics.ListAPIView):

    """
    list:
        Return list of job seeker that viewed certain job
    """

    queryset = (models.ViewJob.objects
                .select_related(
                    'owner',
                    'owner__user')
                .order_by('created_at'))
    permission_classes = (
        permissions.BaseModelPermissions,
        permissions.HasSubscription
    )
    serializer_class = serializers.JobViewerSerializer

    def filter_queryset(self, queryset):
        company = get_company(self.request)
        job = shortcuts.get_object_or_404(
            company.jobs, pk=self.kwargs.get('pk'))
        queryset = queryset.filter(job=job)
        return super().filter_queryset(queryset)


class JobListSoftDeleteView(generics.GenericAPIView):
    """
    View for deletion of multiple jobs
    Request example:
    {\n
        "jobs": [1, 2, 3] # Job ids that user wants to delete
    }
    """
    permission_classes = (
        drf_permissions.IsAuthenticated,
        job_permissions.BulkJobsDeletePermissions,
        permissions.HasSubscription
    )
    serializer_class = serializers.JobIdsSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        services.soft_delete_job_list(
            serializer.validated_data['jobs'], request.user
        )
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class JobRestoreView(drf_views.APIView):
    """
    View for restoring of deleted job.
    Errors:
    If user tries to restore non-deleted job:
        'You can not restore non-deleted job.'
    """
    permission_classes = (
        drf_permissions.IsAuthenticated,
        job_permissions.RestoreJobPermission,
        permissions.HasSubscription
    )

    def get_object(self):
        job_id = self.kwargs.get('pk')
        company = get_company(self.request)
        return shortcuts.get_object_or_404(company.jobs, id=job_id)

    def put(self, request, *args, **kwargs):
        job = self.get_object()
        validators.validate_job_is_deleted(job)
        job = services.restore_job(job)
        data = serializers.JobCompanyUserSerializer(job).data
        return response.Response(
            data=data,
            status=status.HTTP_200_OK
        )


class JobListCSVExportView(mixins.CSVFileMixin, generics.ListAPIView):

    renderer_classes = (renderers.JobCsvRenderer, )
    permission_classes = (
        drf_permissions.IsAuthenticated,
        job_permissions.DownloadJobCSVPermissions,
        permissions.HasSubscription
    )
    queryset = models.Job.objects.get_all_with_relations()
    serializer_class = serializers.JobExportCSVSerializer
    pagination_class = None

    schema = schemas.ManualSchema(fields=[
        coreapi.Field(
            'jobs',
            required=True,
            location='query',
            schema=coreschema.String(
                description=(
                    'string of job ids separated by commas.'
                )
            )
        ),
    ])
    filename_template = 'Job_postings_{}.csv'

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        job_ids = self.request.query_params.get('jobs').split(',')
        company = get_company(self.request)
        queryset = queryset.filter(id__in=job_ids, company=company)
        queryset = core_services.get_ban_status_active_entities(queryset)
        return queryset


class JobShareView(generics.GenericAPIView):
    """
    View for sharing job by email
    """
    permission_classes = (
        job_permissions.ShareJobPermission,
    )
    serializer_class = serializers.ShareJobSerializer
    queryset = models.Job.objects.get_published()

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        job = self.get_object()
        job_seeker = request.user.job_seeker
        services.share_job_by_email(
            job_seeker=job_seeker, job=job, **serializer.validated_data
        )
        return response.Response(status=status.HTTP_200_OK)


class JobActiveEnumView(generics.ListAPIView):

    """get:
        Return list of active (published) jobs id and titles.
        Can search by job title.
    """

    queryset = models.Job.objects.get_published()
    permission_classes = (
        drf_permissions.IsAuthenticated,
        job_permissions.JobEnumPermission,
        permissions.HasSubscription
    )
    serializer_class = serializers.JobEnumSerializer
    search_fields = (
        'title',
    )
    pagination_class = None

    def get_queryset(self):
        company = get_company(self.request)
        return self.queryset.filter(company=company)
