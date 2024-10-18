import datetime

from django.conf import settings as dj_settings
from django.core import validators as dj_validators
from rest_framework import decorators
from rest_framework import generics
from rest_framework import mixins
from rest_framework import permissions as drf_permissions
from rest_framework import response
from rest_framework import viewsets

from auth import constants as auth_constants
from company import models as company_models
from company import serializers as company_serializers
from job import models as job_models
from job import serializers as job_serializers
from job_seeker import models as js_models
from job_seeker import serializers as js_serializers
from leet import enums
from leet import models as leet_models
from leet import serializers as leet_serializers
from leet import services
from leet import utils as leet_utils
from public_api import constants
from public_api import filters
from public_api import serializers
from public_api import utils
from public_api import permissions


@decorators.api_view()
@decorators.permission_classes((drf_permissions.AllowAny,))
def initial_settings(request):
    validators = dj_settings.VALIDATION_REGEXPS
    validators['email_validator'] = {
        'user_regex': dj_validators.EmailValidator.user_regex.pattern,
        'domain_regex': dj_validators.EmailValidator.domain_regex.pattern,
        'literal_regex': dj_validators.EmailValidator.literal_regex.pattern,
        'max_length': dj_settings.MAX_EMAIL_LENGTH,
        'ignore_case': True
    }
    version = getattr(
        dj_settings, 'APP_VERSION',
        {
            'version': 'unknown',
            'date': datetime.date.today(),
            'changelog': {},
        }
    )
    version_data = serializers.VersionSerializer(version).data
    account_deletion_reasons = auth_constants.DEFAULT_DELETION_ACCOUNT_REASONS
    settings = {
        'version': version_data,
        'validators': validators,
        'account_deletion_reasons': account_deletion_reasons,
        'max_salary_value': dj_settings.MAX_SALARY,
        'stripe_public_key': dj_settings.STRIPE_PUBLIC_KEY,
        'socials': utils.get_social_names_and_ids()
    }
    return response.Response(settings)


@decorators.api_view()
@decorators.permission_classes((drf_permissions.AllowAny,))
def enums_view(request):
    job_seeker_education_model_enum_dict = enums.EducationTypesEnum.to_dict()
    job_seeker_education_model_enum_dict.pop('CERTIFICATION')
    enums_dict = {
        'PositionTypes': enums.PositionTypesEnum.to_dict(),
        'EducationTypes': enums.EducationTypesEnum.to_dict(),
        'ClearanceTypes': enums.ClearanceTypesEnum.to_dict(),
        'ExperienceTypes': enums.ExperienceEnum.to_dict(),
        'Benefits': enums.BenefitsEnum.to_dict(),
        'TravelOpportunities': enums.TravelOpportunitiesEnum.to_dict(),
        'JobStatusEnum': enums.JobStatusEnum.to_dict(),
        'AutoapplyStatusEnum': enums.AutoapplyStatusEnum.to_dict(),
        'ApplyStatusEnum': enums.ApplyStatusEnum.to_dict(),
        'JSTravelOpportunities':
            enums.JSTravelOpportunitiesEnum.to_dict(),
        'Employment': enums.EmploymentEnum.to_dict(),
        'CompanyUserStatus': enums.CompanyUserStatusEnum.to_dict(),
        'CandidateRating': enums.RatingEnum.to_dict(),
        'CandidateTypeEnum': enums.CandidateTypeEnum.to_dict(),
        'AppliedDateFilterEnum': enums.AppliedDateFilterEnum.to_dict(),
        'CandidateStatusEnum': leet_utils.get_candidate_statuses_dict(),
        'LastUpdatedWithingDays': constants.LAST_UPDATE_WITH_DAYS_FRONT,
        'PostedDateWithingDays': constants.POSTED_DATE_WITH_DAYS_FRONT,
        'JobSeekerEducationModelEnumDict':
            job_seeker_education_model_enum_dict,
        'EventAttendeeStatus': enums.EventAttendeeStatusEnum.to_dict()
    }
    return response.Response(enums_dict)


class PublicCompanyViewSet(mixins.ListModelMixin,
                           mixins.RetrieveModelMixin,
                           viewsets.GenericViewSet):

    queryset = company_models.Company.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return company_serializers.CompanyPublicDataSerializer
        return serializers.PublicCompanyListSerializer

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        return services.get_ban_status_active_entities(queryset)


class PublicJobViewSet(mixins.ListModelMixin,
                       mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):
    """
    list:
        Return List of jobs.
        All users can see published jobs except jobs with ban status banned.
    retrieve:
        Return details of job.
    """

    queryset = job_models.Job.objects.get_published()
    serializer_class = job_serializers.JobUnauthorizedSerializer
    filter_fields = ('company_id',)


class SharedJobView(generics.RetrieveAPIView):
    queryset = job_models.Job.objects.get_published()
    serializer_class = job_serializers.JobUnauthorizedSerializer
    lookup_field = 'guid'


class IndustryListView(generics.ListAPIView):
    queryset = job_models.Industry.objects.all()
    serializer_class = job_serializers.IndustrySerializer


class SkillListView(generics.ListAPIView):
    serializer_class = job_serializers.SkillDetailSerializer
    queryset = job_models.Skill.objects.all()
    filterset_class = filters.SkillsFilterSet


class CandidateStatusView(generics.ListAPIView):

    queryset = leet_models.CandidateStatus.objects.order_by('workflow_value')
    serializer_class = leet_serializers.CandidateStatusSerializer
    pagination_class = None


class PublicJobSeekerRetrieveView(generics.RetrieveAPIView):
    queryset = js_models.JobSeeker.objects.get_all_with_relations()
    serializer_class = js_serializers.PublicJobSeekerProfileSerializer
    lookup_field = 'guid'
    permission_classes = (permissions.JobSeekerPublicProfilePermission,)
    authentication_classes = ()
