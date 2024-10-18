import coreapi
import coreschema
from django import shortcuts
from django.conf import settings
from django_filters import rest_framework as dj_filters
from rest_framework import exceptions
from rest_framework import generics
from rest_framework import permissions as drf_permissions
from rest_framework import response
from rest_framework import schemas
from rest_framework import serializers as drf_serializers
from rest_framework import status

from candidate import constants
from candidate import filters
from candidate import mixins
from candidate import models
from candidate import pagination
from candidate import permissions
from candidate import renderers
from candidate import serializers
from candidate import services
from candidate import utils
from candidate import validators
from company import models as company_models
from company import permissions as company_permissions
from job import models as job_models
from job_seeker import models as js_models
from leet import constants as base_constants
from leet import enums
from leet import mixins as base_mixins
from leet import models as base_models
from leet import serializers as base_serializers
from permission import permissions as base_permissions
from permission import utils as perm_utils
from subscription import permissions as subscription_permissions
from survey import models as survey_models
from survey import utils as survey_utils


class JobCandidatesView(mixins.CompanyCandidateViewMixin,
                        mixins.CompanyCandidateViewListMixin,
                        generics.ListAPIView):
    """
    list:
        View for filtering list of candidates for certain job.
        all filters like in main vie for list fo candidates.
    """
    permission_classes = (
        drf_permissions.IsAuthenticated,
        permissions.JobCandidatePermission,
        base_permissions.HasSubscription
    )
    serializer_class = serializers.CandidateListSerializer

    def filter_queryset(self, queryset):
        job = shortcuts.get_object_or_404(
            job_models.Job,
            pk=self.kwargs.get('pk'))
        queryset = queryset.filter(job=job)
        return super().filter_queryset(queryset)


class AnswerForJobQuestionsView(generics.GenericAPIView):

    """
    create:
        Create answers for questions in a job.
        Example request data:\n
        [
            {
                "question": 1
                "answer": {
                    "yes_no_value": "YES"
                }
            }
            ...
        ]
        Errors:
        If count of questions > 10:
            'Question list can contain only 10 questions.'
        If 'yes_no_value' in answer is not 'YES' or 'NO':
            '"invalid values" is not a valid choice.'
        If question's flag 'is_answer_required' is True and 'answer' == {} or
                'yes_no_value' is empty:
            'This field is required.'
        Permissions: Only job seeker can create answers for questions.
    """

    queryset = survey_models.AnswerJobSeeker.objects.select_related('answer')
    permission_classes = (
        drf_permissions.IsAuthenticated,
        permissions.CandidateAnswersPermission
    )
    serializer_class = serializers.JobSeekerAnswerCreateSerializer

    def post(self, request, *args, **kwargs):
        job = shortcuts.get_object_or_404(job_models.Job, pk=kwargs.get('pk'))
        js = request.user.job_seeker
        existing_answers = self.queryset.filter(job=job, owner=js)
        serializer = self.get_serializer(data=request.data)
        serializer.context.update({
            'job_seeker': js,
            'job': job,
            'existing_answers': existing_answers
        })
        serializer.is_valid(raise_exception=True)

        answers = survey_utils.create_answers(
            job,
            serializer.validated_data,
            js,
            existing_answers)
        data = serializers.JobSeekerAnswerResponseSerializer(
            answers,
            many=True).data
        return response.Response(data=data, status=status.HTTP_201_CREATED)


class CandidateAnswerView(generics.ListAPIView):

    """
    list:
        Return answers of certain job seeker on certain questions in job.
        Example response JSON for job seeker:\n
        [
            {
                "id": 1,
                "question": {
                    "id": 1,
                    "body": "string"
                },
                "answer": "NO"
            }
            ...
        ]
        Example response JSON for company user:
        [
            {
                "id": 1,
                "question": {
                    "id": 1,
                    "body": "string"
                },
                "answer": "NO",
                "is_disqualify": false
            }
            ...
        ]
        Permissions:\n
            job seeker can view only his answers,\n
            company user can view answers only for job of his company.
    """

    queryset = (survey_models.AnswerJobSeeker.objects
                             .select_related('question', 'answer')
                             .order_by('id'))
    permission_classes = (
        drf_permissions.IsAuthenticated,
        permissions.CandidateAnswersPermission,
        base_permissions.HasSubscription
    )
    pagination_class = None

    def get_serializer_class(self):
        user = self.request.user
        if perm_utils.is_company_user(user):
            return serializers.CandidateAnswersSerializer
        return serializers.JobSeekerAnswerResponseSerializer

    def filter_queryset(self, queryset):
        job = shortcuts.get_object_or_404(
            job_models.Job,
            pk=self.kwargs.get('job_id'))
        job_seeker = shortcuts.get_object_or_404(
            js_models.JobSeeker,
            pk=self.kwargs.get('job_seeker_id'))
        queryset = queryset.filter(job=job, owner=job_seeker)
        return super().filter_queryset(queryset)


class CandidateAssignView(generics.GenericAPIView):

    permission_classes = (
        drf_permissions.IsAuthenticated,
        permissions.CandidateAssignPermission,
        base_permissions.HasSubscription
    )

    serializer_class = serializers.CandidateAssignSerializer

    def post(self, request, *args, **kwargs):
        """
        View for assign job seeker to jobs.
        Example request JSON data:\n
            {
                "job_seekers": [1, 2],
                "jobs": [1, 2]
            }
        Example response JSON:\n
            "assigned": [
                {
                    "candidate": "firstname lastname",
                    "jobs": [
                        "JP1",
                        "JP2",
                    ]
                }
            ],
            "already_assigned": [
                {
                    "candidate" "firstname2 lastname2",
                    "jobs": [
                        "JP1",
                        "JP2",
                    ]
                }
            ]
        Errors:
            Job seeker is not purchased or is not applied
                for any job of company.
            Count of job seeker > 50.
            Count of jobs > 50.
            Job has status NEW or CLOSED.
        """
        serializer = self.get_serializer(data=request.data)
        company_user = request.user.company_user
        serializer.context['company'] = company_user.company
        serializer.is_valid(raise_exception=True)
        result = utils.assign_candidates(
            company_user,
            serializer.validated_data)
        return response.Response(data=result, status=status.HTTP_201_CREATED)


class CandidateDetailsView(mixins.CompanyCandidateViewMixin,
                           generics.RetrieveAPIView):
    """
    retrieve:
        View candidate details.
    """

    serializer_class = serializers.CandidateDetailsSerializer
    permission_classes = (
        base_permissions.BaseModelPermissions,
        base_permissions.HasSubscription
    )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        if (instance.job_seeker.ban_status ==
                enums.BanStatusEnum.BANNED.name): # noqa
            emsg = constants.CANDIDATE_BANNED_ERROR.format(
                instance.job_seeker.user.get_full_name())
            raise exceptions.PermissionDenied(emsg)

        js = instance.job_seeker
        company_user = request.user.company_user
        company_user.viewed_job_seekers.create(job_seeker=js)

        serializer = self.get_serializer(instance)
        return response.Response(serializer.data)


class CandidateRatingView(mixins.CompanyCandidateViewMixin,
                          generics.GenericAPIView):

    serializer_class = serializers.CandidateRatingCreateUpdateSerializer
    permission_classes = (
        drf_permissions.IsAuthenticated,
        permissions.CandidateRatingPermission,
        base_permissions.HasSubscription
    )

    def put(self, request, *args, **kwargs):
        """View for creating or updating rating of candidate."""
        serializer = self.get_serializer(data=request.data)
        candidate = self.get_object()
        serializer.is_valid(raise_exception=True)
        rating = utils.update_or_create_rating(
            candidate,
            request.user.company_user,
            serializer.validated_data['rating'])
        data = {
            'owner': rating.owner.user.get_full_name(),
            'rating': rating.rating
        }
        return response.Response(data=data, status=status.HTTP_200_OK)


class CandidatesList(mixins.CompanyCandidateViewMixin,
                     mixins.CompanyCandidateViewListMixin,
                     generics.ListAPIView):
    """
    get:
        Returns list of company candidates (assigned and applied JS)
        Response example:\n
        {
            "count": 17,
            "next": null,
            "previous": null,
            "results":
                [
                    {
                        "id": 1,
                        "job_seeker":
                            {
                            "id": 1,
                            "modified_at": "2018-11-15T14:54:58Z",
                            "is_deleted": false,
                            "user": {
                                    "id": 1,
                                    "name": "John Lenon"
                                    },

                            "location": {
                                "id": 5992,
                                "name": "Barneveld",
                                "state": {
                                    "id": 32,
                                    "name": "New York",
                                    "abbreviation": "NY"
                                }
                            }
                        },
                        "job": {
                            "id": 2,
                            "title": "Scientist, research (life sciences)"
                        },
                        "created_at": "2018-11-19T09:11:05Z",
                        "applied_date": "2018-11-19T09:11:05Z",
                        "is_applied_after_assignment": false,
                        "is_disqualified_for_questionnaire": false,
                        "is_disqualified_for_skills": true
                    },
                    ...
                ]
        }
        NOTE: use `created_at` as assignment date for
        applied after assignment candidates

        ordering:
        api/v1/job/?ordering=job_seeker__user__first_name
        api/v1/job/?ordering=job_seeker__user__last_name
        api/v1/job/?ordering=job__title
        api/v1/job/?ordering=-applied_date

        Permissions:
            job seeker has no access to candidates,
            company user can view candidates only for job of his company.
    """
    serializer_class = serializers.CandidateListSerializer


class CandidateQuickView(mixins.CompanyCandidateViewMixin,
                         generics.ListAPIView):
    """
    View for retrieve candidate details for certain job.
    This view extended with a links to retrieve `next` or `previous`
    candidate for passed job id.
    """
    serializer_class = serializers.CandidateQuickViewSerializer
    pagination_class = pagination.CandidateQuickViewPagination

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page:
            js = page[0].job_seeker
            company_user = request.user.company_user
            company_user.viewed_job_seekers.create(job_seeker=js)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        return queryset.filter(
            job_seeker__ban_status=enums.BanStatusEnum.ACTIVE.name)  # noqa


class CandidateStatusView(mixins.CompanyCandidateViewMixin,
                          generics.GenericAPIView):

    permission_classes = (
        base_permissions.BaseModelPermissions,
        base_permissions.HasSubscription
    )
    serializer_class = serializers.CandidateStatusSerializer

    def patch(self, request, *args, **kwargs):
        candidate = self.get_object()
        serializer = serializers.CandidateStatusSerializer(
            candidate, data=request.data)
        serializer.is_valid(raise_exception=True)
        candidate.status = serializer.validated_data['status']
        candidate.save()
        company_user = request.user.company_user
        last_step = utils.update_workflow_steps(
            company_user,
            candidate,
            candidate.status)
        data = base_serializers.CandidateStatusSerializer(
            last_step.status).data
        return response.Response(data=data)


class RestoreCandidateView(mixins.CompanyCandidateViewMixin,
                           generics.GenericAPIView):

    permission_classes = (
        drf_permissions.IsAuthenticated,
        permissions.CandidateRestorePermission,
        base_permissions.HasSubscription
    )

    def get_serializer_class(self):
        """Swagger schema requires serializer for rendering."""
        return drf_serializers.Serializer

    def post(self, request, *args, **kwargs):
        """View for restore rejected candidate."""
        candidate = self.get_object()
        validators.CandidateRestoreValidator(candidate).validate()
        candidate.workflow_steps.last().delete()
        last_step = candidate.workflow_steps.last()
        candidate.status = last_step.status
        candidate.save()
        data = base_serializers.CandidateStatusSerializer(
            candidate.workflow_steps.last().status).data
        return response.Response(data=data)


class WorkflowStepsCompanyStatView(generics.GenericAPIView):

    queryset = models.WorkflowStep.objects.all()
    filter_backends = (dj_filters.DjangoFilterBackend,)
    filterset_class = filters.WorkflowStepsFilterSet
    pagination_class = None
    schema = schemas.AutoSchema(
        manual_fields=[
            coreapi.Field(
                'all',
                required=False,
                location='query',
                schema=coreschema.String(),
                description=(
                    'Force return candidates workflow stats for each status. '
                    'Available value for True: {}'.format(
                        settings.REQUEST_QUERY_PARAMETERS_TRUE_VALUES))
            ),
        ]
    )

    def get(self, request, *args, **kwargs):
        """
        View count candidates on each step in workflow
        that company user wants see.
        permissions: Only company users
        Example Response JSON:\n
        ```
        [
            {
                "id": 1,
                "name": "Applied",
                "n_candidates": 100
            },
            {
                "id": 2,
                "name": "Screened",
                "n_candidates": 2
            },
            {
                "id": 5,
                "name": "Hired",
                "n_candidates": 20
            },
            {
                "id": 6,
                "name": "Rejected",
                "n_candidates": 22
            }
        ]
        endpoint for stats by company for all statues:\n
            api/v1/candidates-workflow-stats/?all=true
        ```
        """
        statuses = self.request.user.company_user.candidate_statuses.all()
        _all = request.query_params.get('all', False)

        if _all and _all in settings.REQUEST_QUERY_PARAMETERS_TRUE_VALUES:
            statuses = None

        qs = self.filter_queryset(self.get_queryset())
        stats = utils.get_candidate_workflow_steps_stats(qs, statuses)
        return response.Response(data=stats)

    def filter_queryset(self, queryset):
        company = self.request.user.company_user.company
        queryset = super().filter_queryset(queryset)
        queryset = queryset.filter(candidate__job__company=company)
        return queryset

    def get_permissions(self):
        self.permission_classes = [
            drf_permissions.IsAuthenticated,
            permissions.WorkflowStepsCompanyStatsPermission,
            base_permissions.HasSubscription
        ]
        # Check query params for now instead of using separate endpoinds
        # for workflow stats for reporting and dashboard.
        # If query params is not empty it means that the user tries to
        # obtain report data and it's needed to check permissions for this.
        if self.request.query_params:
            self.permission_classes.append(
                company_permissions.CompanyReportPermission
            )
        return super().get_permissions()


class CompanyReportView(generics.GenericAPIView):
    """
    get:
        Return company report in range `from_date` - `to_date` with `basis`.
        Response example:\n
        [
            {
                "name": "APPLIED",
                "series": [
                    {
                        "date": "2019-01-08T00:00:00Z",
                        "count": 1
                    },
                    {
                        "date": "2019-01-10T00:00:00Z",
                        "count": 1
                    }
                ]
            },
            {
                "name": "SCREENED",
                "series": [
                    {
                        "date": "2019-01-08T00:00:00Z",
                        "count": 1
                    },
                    {
                        "date": "2019-01-09T00:00:00Z",
                        "count": 2
                    },
                    {
                        "date": "2019-01-10T00:00:00Z",
                        "count": 1
                    }
                ]
            },
            {
                "name": "INTERVIEWED",
                "series": [
                    {
                        "date": "2019-01-10T00:00:00Z",
                        "count": 1
                    }
                ]
            },
            {
                "name": "OFFERED",
                "series": []
            },
            {
                "name": "HIRED",
                "series": []
            },
            {
                "name": "REJECTED",
                "series": []
            }
        ]
    """
    queryset = models.WorkflowStep.objects.all()
    permission_classes = (
        drf_permissions.IsAuthenticated,
        company_permissions.CompanyReportPermission,
        base_permissions.HasSubscription,
        subscription_permissions.SubscriptionHasReportingPermission
    )

    filter_backends = (dj_filters.DjangoFilterBackend,)
    filterset_class = filters.CompanyReportFilterSet

    pagination_class = None

    schema = schemas.AutoSchema(
        manual_fields=[
            coreapi.Field(
                'basis',
                required=True,
                location='query',
                schema=coreschema.String(),
                description=('Date aggregation basis. Available choices: {}'
                             .format(constants.SUPPORTED_TIME_SERIES_BASES))
            ),
        ]
    )

    def get(self, request, *args, **kwargs):
        basis = self.request.query_params.get('basis')
        validators.validate_time_series_basis(basis)
        queryset = self.filter_queryset(self.get_queryset())
        return response.Response(data=self._get_report_data(queryset, basis))

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        company = self.request.user.company_user.company
        return queryset.filter(candidate__job__company=company)

    @staticmethod
    def _get_report_data(queryset, basis):
        statuses = (base_models.CandidateStatus.objects.values_list(
            'name', flat=True))

        return [{
            'name': status,
            'series': utils.get_candidate_status_time_series(
                queryset, status, basis)
        } for status in statuses]


class CandidateActivityView(generics.ListAPIView):

    """
    get:
        View candidates activities for company dashboard.
        Example JSON response:\n
        ```
            {
                "count": 2,
                "next": null,
                "previous": null,
                "results": [
                    {
                    "candidate": {
                        "id": 18,
                        "name": "jsfirstname jslastname"
                    },
                    "activity": "Applied",
                    "job": {
                        "id": 18,
                        "title": "JP1"
                    },
                    "created_at": "2019-01-30T12:33:08Z"
                    }
                    ...
                ]
            }
        ```
    """

    serializer_class = serializers.CandidateActivitySerializer
    permission_classes = (
        drf_permissions.IsAuthenticated,
        permissions.CandidatesActivityPermission,
        base_permissions.HasSubscription
    )

    def get_queryset(self):
        """
        For dashboard's for candidate's activity use workflow stes queryset.
        Name of activity usual is equal name of status of workflow step.
        Only applied status can have two activities: 'Applied' and 'Assigned'.
        """
        company = self.request.user.company_user.company
        return (models.WorkflowStep
                      .objects
                      .filter(candidate__job__company=company)
                      .select_related(
                          'candidate',
                          'status')
                      .prefetch_related(
                          'candidate__job_seeker__user',
                          'candidate__job')
                      .order_by('-created_at'))


class CandidateQuickListView(mixins.CompanyCandidateViewMixin,
                             generics.GenericAPIView):

    """
    get:
        View list of candidates with which worked company user
        during 5 days.
    """

    permission_classes = (
        drf_permissions.IsAuthenticated,
        permissions.CandidateQuickListPermission,
        base_permissions.HasSubscription
    )
    filter_fields = (
        'status',
    )
    search_fields = (
        'job_seeker__user__first_name',
        'job_seeker__user__last_name',
        'job__title'
    )
    pagination_class = None

    def get_serializer(self, *args, **kwargs):
        # swagger fix
        return None

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        service = services.QuickListService(queryset, request.user)
        return response.Response(data=service.get_data_for_quick_list())


# NOTE (m.nizovtsova): located in candidate module to avoid of circular
# dependencies between company and candidate modules
class CompanyUsersActivityView(generics.ListAPIView):

    queryset = (company_models.CompanyUser
                              .objects
                              .select_related(
                                  'user')
                              .prefetch_related(
                                  'jobs',
                                  'savedjobseeker_set',
                                  'workflowstep_set',
                                  'workflowstep_set__status')
                              .order_by('id'))
    serializer_class = serializers.CompanyUserCandidatesActivitySerializer
    permission_classes = (
        drf_permissions.IsAuthenticated,
        company_permissions.CompanyReportPermission,
        base_permissions.HasSubscription,
        subscription_permissions.SubscriptionHasReportingPermission,
    )

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        return queryset.filter(company_id=self.kwargs.get('pk'))


class CandidateListCSVExportView(base_mixins.CSVFileMixin,
                                 generics.ListAPIView):

    renderer_classes = (renderers.CandidateCsvRenderer, )
    permission_classes = (
        drf_permissions.IsAuthenticated,
        permissions.ExportCandidateToCSVPermission,
        base_permissions.HasSubscription
    )
    pagination_class = None
    serializer_class = serializers.CandidateExportToCSVSerializer
    queryset = (models.Candidate.objects
                      .select_related(
                          'job',
                          'job_seeker',
                          'apply')
                      .prefetch_related(
                          'rating',
                          'workflow_steps',
                          'job_seeker__industries',
                          'job_seeker__user',
                          'job_seeker__skills',
                          'job_seeker__address',
                          'job_seeker__address__city',
                          'job_seeker__address__city__state',
                          'job_seeker__educations',
                          'job_seeker__certifications',
                          'job_seeker__job_experience',
                      ))
    schema = schemas.ManualSchema(fields=[
        coreapi.Field(
            'candidates',
            required=True,
            location='query',
            schema=coreschema.String(
                description=(
                    'candidate ids separated by commas.'
                )
            )
        ),
    ])

    filename_template = 'Candidates_{}.csv'

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        candidate_ids = self.request.query_params.get('candidates').split(',')
        company = self.request.user.company_user.company
        queryset = queryset.filter(job__company=company, id__in=candidate_ids)
        queryset = utils.annotate_candidate_with_applied_date(queryset)
        return queryset


class CandidateEnumView(generics.ListAPIView):

    """get:
        Return list of candidates id and names
        can search by user first and last name
        NOTE (i.bogretsov): Only NOT rejected candidates.
    """

    queryset = (models.Candidate.objects
                                .select_related(
                                    'job_seeker',
                                    'job_seeker__user'))
    permission_classes = (
        drf_permissions.IsAuthenticated,
        permissions.CandidateEnumPermission,
        base_permissions.HasSubscription
    )
    serializer_class = serializers.CandidateEnumSerializer
    filter_fields = (
        'job',
    )
    search_fields = (
        'job_seeker__user__first_name',
        'job_seeker__user__last_name'
    )
    pagination_class = None
    schema = schemas.AutoSchema(
        manual_fields=[
            coreapi.Field(
                'job',
                required=True,
                location='query',
                schema=coreschema.String(),
                description='return candidates for certain job.'
            ),
        ]
    )

    def get_queryset(self):
        return (
            self
            .queryset
            .filter(job__company=self.request.user.company_user.company)
            .exclude(status__name=base_constants.CANDIDATE_STATUS_REJECTED)
        )
