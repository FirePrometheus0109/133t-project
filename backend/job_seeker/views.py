from django import shortcuts
from django.conf import settings
from django_filters import rest_framework as drf_filters
from rest_framework import generics
from rest_framework import permissions as drf_permissions
from rest_framework import response
from rest_framework import status
from rest_framework import views
from rest_framework import viewsets

from company import services as company_services
from job import models as job_models
from job import serializers as job_serializers
from job_seeker import filters as js_filters
from job_seeker import models
from job_seeker import permissions
from job_seeker import serializers
from job_seeker import services
from job_seeker import validators
from log import constants as log_constants
from log import utils as log_utils
from permission import permissions as base_permissions
from permission import utils as permission_utils


class SavedMixin:
    """
    SavedJobView and SavedJobSeekerView have the same logic
    for adding/removing jobs and job seekers' profiles.
    """

    @staticmethod
    def complete_action(add, model, **kwargs):
        if add:
            instance, _ = model.objects.get_or_create(**kwargs)
            data = {'saved_at': instance.created_at.strftime(
                    settings.DEFAULT_SERVER_DATETIME_FORMAT)}
            return response.Response(data=data, status=status.HTTP_200_OK)

        model.objects.filter(**kwargs).delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class JobSeekerViewSet(viewsets.ModelViewSet):
    """
    list:
        Return list of job seekers.
        Filtering:
            Multiple choices:
            api/v1/job-seeker/?position_type=FULL_TIME&position_type=PART_TIME
            api/v1/job-seeker/?clearance=SECRET&clearance=TOP_SECRET
            api/v1/job-seeker/?skills=1&skills=2
            api/v1/job-seeker/?location=10001&location=NY&location=Washington

            Single choices:
            api/v1/job-seeker/?profile_updated_within_days=5
            api/v1/job-seeker/?education=HIGH_SCHOOL
            api/v1/job-seeker/?experience=NO_EXPERIENCE
            api/v1/job-seeker/?travel=NO_TRAVEL

        Search (Full Text Search):
        api/v1/job-seeker/?search=somestring

        Ordering:
        api/v1/job-seeker/?ordering=rank
        api/v1/job-seeker/?ordering=modified_at
        api/v1/job-seeker/?ordering=first_name
        api/v1/job-seeker/?ordering=last_name
    """
    queryset = models.JobSeeker.objects.get_all_with_relations()
    permission_classes = (
        drf_permissions.IsAuthenticated,
        permissions.JobSeekerProfilePermission,
        base_permissions.HasSubscription
    )
    filter_backends = (
        drf_filters.DjangoFilterBackend,
        js_filters.FullTextSearchBackend,
        js_filters.JobSeekerListOrderingFilterBackend,
    )
    filterset_class = js_filters.JobSeekerFilterSet

    def get_serializer_class(self):
        if permission_utils.is_company_user(self.request.user):
            return serializers.JobSeekerForCompanyUserSerializer
        return serializers.JobSeekerSerializer

    def filter_queryset(self, queryset):
        if self.action == 'list':
            queryset = queryset.filter(is_public=True)
        queryset = super().filter_queryset(queryset)
        return queryset

    def retrieve(self, request, *args, **kwargs):
        job_seeker = self.get_object()
        if permission_utils.is_company_user(request.user):
            company_user = request.user.company_user
            company_user.viewed_job_seekers.create(job_seeker=job_seeker)
        serializer = self.get_serializer(job_seeker)
        return response.Response(data=serializer.data)


class JobSeekerPhotoView(generics.UpdateAPIView):
    queryset = models.JobSeeker.objects.all()
    serializer_class = serializers.PhotoSerializer
    permission_classes = (
        drf_permissions.IsAuthenticated,
        permissions.PhotoPermission
    )


class JobSeekerResourceBaseViewSet(viewsets.ModelViewSet):
    """
    Base ViewSet for subresources of a JobSeeker resource.
    Used for JobExperience, Educations, Certifications, Cover Letter ViewSets.
    """

    def filter_queryset(self, queryset):
        js = shortcuts.get_object_or_404(
            models.JobSeeker,
            id=self.kwargs.get('job_seeker_id'))
        queryset = queryset.filter(owner=js)
        return super().filter_queryset(queryset)

    def get_serializer_context(self):
        """
        Add job_seeker instance to serializer's context.
        It is need for validation."""
        context = super().get_serializer_context()
        # NOTE (i.bogretsov) this check is used for swagger
        if self.kwargs:
            context['job_seeker'] = shortcuts.get_object_or_404(
                models.JobSeeker,
                id=self.kwargs.get('job_seeker_id'))
        return context

    def perform_create(self, serializer):
        serializer.save(owner=serializer.context['job_seeker'])


class JobExperienceViewSet(JobSeekerResourceBaseViewSet):
    """View for adding job experience to job_seeker profile."""

    queryset = models.JobExperience.objects.all()
    serializer_class = serializers.JobExperienceSerializer
    permission_classes = (
        drf_permissions.IsAuthenticated,
        permissions.JobExperiencePermission,
        base_permissions.HasSubscription
    )


class EducationViewSet(JobSeekerResourceBaseViewSet):
    """View for adding education of job seeker to profile."""

    queryset = models.Education.objects.order_by(
        '-is_current',
        '-created_at',
        'institution'
    )
    serializer_class = serializers.EducationSerializer
    permission_classes = (
        drf_permissions.IsAuthenticated,
        permissions.EducationPermission,
        base_permissions.HasSubscription
    )


class CertificationViewSet(JobSeekerResourceBaseViewSet):
    """View for adding certification of job seeker to profile."""

    queryset = models.Certification.objects.order_by(
        '-is_current',
        '-created_at',
        'institution'
    )
    serializer_class = serializers.CertificationSerializer
    permission_classes = (
        drf_permissions.IsAuthenticated,
        permissions.CertificationPermission,
        base_permissions.HasSubscription
    )

class DocumentViewSet(JobSeekerResourceBaseViewSet):
    queryset = models.Document.objects.all()
    serializer_class = serializers.DocumentSerializer
    permission_classes = (
        drf_permissions.IsAuthenticated,
        permissions.DocumentPermission,
        # base_permissions.HasSubscription
    )

class SavedJobView(generics.ListAPIView, SavedMixin):
    """
    ViewSet for adding/removing of job to/from saved and obtaining of
    saved jobs.
    post:
        Add or remove job to/from saved\n
        Permissions:\n
            User should be authenticated,
            User should be job seeker
        Example request data:\n
            {
                "job": 1
                "add": true
            }
        Only one action can send - add or remove.\n
        Example response data action add:
            {
                "saved_at": timestamp
            }
        There is no response data for action remove.
    """

    queryset = (job_models.Job.objects
                          .get_all_with_relations()
                          .order_by('-savedjob_set__created_at'))
    permission_classes = (
        drf_permissions.IsAuthenticated,
        permissions.SavedJobsPermission
    )

    def filter_queryset(self, queryset):
        js = self.request.user.job_seeker
        queryset = queryset.filter(savedjob_set__job_seeker=js)
        return super().filter_queryset(queryset)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return job_serializers.JobListJobSeekerSerializer
        return serializers.SavedJobSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        add = serializer.validated_data.get('add', False)
        job = serializer.validated_data['job']
        js = request.user.job_seeker
        return self.complete_action(
            add,
            models.SavedJob,
            job=job,
            job_seeker=js)


class CoverLetterViewSet(JobSeekerResourceBaseViewSet):
    """View for cover letters managing."""

    queryset = models.CoverLetter.objects.order_by('-created_at')
    serializer_class = serializers.CoverLetterSerializer
    permission_classes = (
        drf_permissions.IsAuthenticated,
        permissions.CoverLetterPermission,
        base_permissions.HasSubscription
    )


class JobSeekerProfilePurchaseView(generics.GenericAPIView):

    queryset = models.JobSeeker.objects.get_all_with_relations()
    permission_classes = (
        drf_permissions.IsAuthenticated,
        permissions.JobSeekerProfilePurchasePermission,
        base_permissions.HasSubscription
    )
    serializer_class = serializers.JobSeekerForCompanyUserSerializer

    def put(self, request, *args, **kwargs):
        """
        View for purchasing a job seekers.\n
        Errors:\n
            Company user try to purchase applied job seeker.
            Company user try to purchase purchases job seeker.
        """
        job_seeker = self.get_object()
        company = request.user.company_user.company
        service = company_services.CompanyService(company)
        service.purchase_job_seeker(request.user.company_user, job_seeker)
        return response.Response(data=self.get_serializer(job_seeker).data)


class JobSeekerViewerList(generics.ListAPIView):
    """Return list of `job_seeker` profile views.
    """

    queryset = (models.ViewJobSeeker.objects
                                    .select_related(
                                        'job_seeker',
                                        'company_user',
                                        'company_user__company'))
    permission_classes = (
        drf_permissions.IsAuthenticated,
        permissions.JobSeekerViewerListPermission,
    )
    serializer_class = serializers.JobSeekerViewerListSerializer

    def filter_queryset(self, queryset):
        qs = super().filter_queryset(queryset)
        qs = services.group_views_qs_by_company(qs)
        return qs.filter(job_seeker_id=self.kwargs.get('pk'))


class SavedJobSeekerView(views.APIView, SavedMixin):
    """
    ViewSet for adding/removing of job seeker to/from saved and obtaining of
    saved job seekers.
    create:
        Add or remove job seeker to/from saved\n
        Permissions:\n
            User should be authenticated,
            User should be company user
        Example request data:\n
            {
                "add": true
            }
        Only one action can send - add or remove.\n
        Example response data action add:
            {
                "saved_at": timestamp
            }
        There is no response data for action remove.
    """
    permission_classes = (
        drf_permissions.IsAuthenticated,
        permissions.SavedJobSeekerPermission,
        base_permissions.HasSubscription
    )

    def post(self, request, *args, **kwargs):
        job_seeker = shortcuts.get_object_or_404(
            models.JobSeeker,
            pk=kwargs.get('pk'))
        company_user = request.user.company_user
        validators.validate_can_save_job_seeker_profile(
            job_seeker,
            company_user.company)
        serializer = serializers.SaveRemoveBaseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        add = serializer.validated_data.get('add', False)
        resp = self.complete_action(add, models.SavedJobSeeker,
                                    job_seeker=job_seeker,
                                    company_user=company_user)
        if add:
            log_utils.create_log(
                company_user.user,
                log_constants.LogEnum.profile_save.name,
                log_constants.LogEnum.profile_save.value,
                job_seeker
            )
        return resp
