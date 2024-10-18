from django import shortcuts
from django_filters.rest_framework import backends as drf_backends
from rest_framework import filters as drf_filters
from rest_framework import generics
from rest_framework import permissions as drf_permissions
from rest_framework import response
from rest_framework import views
from rest_framework import viewsets

from apply import filters
from apply import models
from apply import permissions
from apply import serializers
from apply import services
from apply import validators
from job import models as job_models
from leet import enums
from permission import permissions as base_permissions


class AutoapplyJobList(generics.ListAPIView):
    """
    View for obtaining of Job list for the new or specific Autoapply.

    Response example:

    {\n
        "count": 1,
        "next": null,
        "previous": null,
        "results":
        [
            {
                "id": 3,
                "created_at": "2018-09-24T11:03:59.912864Z",
                "title": "IT specialist",
                "location": {
                    "id": 1,
                    "city": {
                        "id": 23,
                        "name": "New York",
                        "state": {
                            "id": 45,
                            "name": "New York",
                            "abbreviation": "NY"
                        }
                    },
                    "country": {
                        "id": 1,
                        "name": "USA"
                    },
                    "zip": {
                        "id": 3,
                        "code": 25869
                    }
                },
                "position_type": "CONTRACT",
                "education": "PHD",
                "clearance": "TOP_SECRET_SCI",
                "experience": "MORE_THAN_10",
                "salary_min": 7000,
                "salary_max": 8000,
                "salary_negotiable": false,
                "benefits": "VISION",
                "travel": "REQUIRED",
                "company": {
                    "id": 1,
                    "name": "Itransition"
                },
                "matching_percent": "75.00",
                "is_clearance_match": true,
                "is_required_skills_match": true,
                "is_education_match": false,
                "applied_at": null,  # for applied jobs
                "apply_job_status": "VIEWED",
                "is_cover_letter_required": false,
                "is_cover_letter_provided": false
            }
        ]
    }
    """
    filter_backends = (
        drf_backends.DjangoFilterBackend,
        drf_filters.OrderingFilter,
        drf_filters.SearchFilter
    )
    permission_classes = (
        drf_permissions.IsAuthenticated,
        permissions.AutoApplyJobListPermission,
    )
    serializer_class = serializers.AutoapplyJobListSerializer
    search_fields = ('company__name', 'title')
    filterset_class = filters.AutoapplyJobFilter

    def get_queryset(self):
        js = self.request.user.job_seeker
        autoapply = self._get_autoapply()
        return services.AutoapplyService(js, autoapply).get_autoapply_jobs()

    def _get_autoapply(self):
        js = self.request.user.job_seeker
        autoapply_id = self.kwargs.get('pk')
        if autoapply_id is not None:
            return shortcuts.get_object_or_404(
                models.Autoapply,
                id=autoapply_id,
                owner=js)
        return None

    def list(self, request, *args, **kwargs):
        job_seeker = self.request.user.job_seeker
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            resp = self.get_paginated_response(serializer.data)
        else:
            serializer = self.get_serializer(queryset, many=True)
            resp = response.Response(serializer.data)
        models.Apply.objects.filter(
            job__in=queryset,
            owner=job_seeker,
            status=enums.ApplyStatusEnum.NEW.name  # noqa
        ).update(
            status=enums.ApplyStatusEnum.VIEWED.name  # noqa
        )
        return resp


class AutoapplyJobDetails(generics.RetrieveAPIView):
    """
    View for obtaining of a single Job with additional Job
    attributes.

    Response example:

    {\n
        "id": 6,
        "created_at": "2018-09-24T11:04:35.996294Z",
        "title": "IT specialist",
        "location":
        {
            "id": 1,
            "city": {
                "id": 23,
                "name": "New York",
                "state": {
                    "id": 45,
                    "name": "New York",
                    "abbreviation": "NY"
                }
            },
            "country": {
                "id": 1,
                "name": "USA"
            },
            "zip": {
                "id": 3,
                "code": 25869
            }
        },
        "position_type": "INTERNSHIP",
        "education": "ASSOCIATES_DEGREE",
        "clearance": "CONFIDENTIAL",
        "experience": "FROM_3_TO_5",
        "salary_negotiable": true,
        "benefits": "FULL_BENEFITS",
        "travel": "REQUIRED",
        "company": {
            "id": 1,
            "name": "Super company"
        },
        "matching_percent": "50.00",
        "is_clearance_match": true,
        "is_questionnaire_answered": true,
        "is_required_skills_match": false,
        "is_education_match": true,
        "is_cover_letter_required": true,
        "is_cover_letter_provided": false,
        "required_skills": [
        {
          "id": 2,
          "name": "Java",
          "match": false
        },
        {
          "id": 3,
          "name": "Django",
          "match": false
        },
        {
          "id": 4,
          "name": "Flask",
          "match": true
        },
        {
          "id": 5,
          "name": "Django REST Framework",
          "match": true
        },
        {
          "id": 6,
          "name": "Tornado",
          "match": false
        }
        ],
        "optional_skills": [],
        "description": "Lorem Ipsum"
    }
    """
    serializer_class = serializers.AutoapplyJobDetailsSerializer
    permission_classes = (
        drf_permissions.IsAuthenticated,
        permissions.AutoApplyJobDetailPermission,
    )

    def get_queryset(self):
        js = self.request.user.job_seeker
        qs = job_models.Job.objects.get_all_with_relations()
        service = services.AutoapplyService(js)
        return service.annotate_jobs_with_matching_criteria(qs)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['js_skills'] = self.request.user.job_seeker.skills.all()
        return context

    def retrieve(self, request, *args, **kwargs):
        job = self.get_object()
        request.user.job_seeker.viewjob_set.create(job=job)
        serializer = self.get_serializer(job)
        return response.Response(serializer.data)


class AutoapplyModelViewSet(viewsets.ModelViewSet):
    """
    Viewset for obtaining, saving  and destroying of Autoapply data.

    list:
    Returns a list of all Autoapplies that belongs to user.
    Response example:
    {\n
        "count": 1,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 2,
                "title": "My Autoapply",
                "status": "SAVED",
                "jobs_count": 3,
                "new_jobs_count": 2,
                "days_to_completion": 1  # for in progress autoapply
            },
        ]
    }

    create:
    Used for Autoapply creation, Autoapply will be created with status SAVED.

    retrieve:
    Returns single Autoapply.
    Response example:
    {\n
        "id": 1,
        "title": "title",
        "status": "IN_PROGRESS",
        "query_params": "",
        "number": 6,
        "owner": 1,
        "stopped_jobs": [],
        "deleted_jobs": [],
        "new_jobs_count": 2,
        "days_to_completion": 3,  # for in progress autoapply
    }
    """
    queryset = models.Autoapply.get_queryset()
    permission_classes = (
        base_permissions.BaseModelPermissions,
        base_permissions.BaseOwnerPermission
    )

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.AutoapplyListSerializer
        return serializers.AutoapplySerializer

    def get_queryset(self):
        return self.queryset.filter(owner__user=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['job_seeker'] = self.request.user.job_seeker
        return context

    def perform_destroy(self, instance):
        job_seeker = self.request.user.job_seeker
        services.AutoapplyService(job_seeker, instance).delete_autoapply()


class StartAutoapplyView(generics.UpdateAPIView):
    """
    Used for Autoapply starting.
    Request example:
    {\n
        "applied_jobs": [1, 2, 3] # Job ids that user wants to apply for
    }
    """
    permission_classes = (
        drf_permissions.IsAuthenticated,
        permissions.StartAutoApplyPermission
    )
    serializer_class = serializers.StartAutoapplySerializer

    def get_queryset(self):
        return models.Autoapply.objects.filter(
            owner=self.request.user.job_seeker)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['job_seeker'] = self.request.user.job_seeker
        return context


class StopAutoapplyView(views.APIView):
    """
    View that allow to stop IN_PROGRESS Autoapply. In response
    returns Autoapply with new status.
    """
    permission_classes = (
        drf_permissions.IsAuthenticated,
        permissions.StopAutoApplyPermission
    )

    def get_object(self, pk):
        job_seeker = self.request.user.job_seeker
        return shortcuts.get_object_or_404(
            models.Autoapply, id=pk, owner=job_seeker)

    def put(self, request, *args, **kwargs):  # noqa
        autoapply_id = self.kwargs.get('pk')
        autoapply = self.get_object(autoapply_id)
        job_seeker = self.request.user.job_seeker
        service = services.AutoapplyService(job_seeker, autoapply)
        result = service.stop_autoapply()
        data = serializers.AutoapplySerializer(result).data
        return response.Response(data)


class RestartAutoapplyView(views.APIView):
    """
    View that allow to restart STOPPED or FINISHED Autoapply. Autoapply can
    be restarted only in case when required jobs count wasn't found
    during the previous iteration. In response
    returns Autoapply with new status.
    """
    permission_classes = (
        drf_permissions.IsAuthenticated,
        permissions.RestartAutoApplyPermission
    )

    def get_object(self):
        autoapply_id = self.kwargs.get('pk')
        job_seeker = self.request.user.job_seeker
        return shortcuts.get_object_or_404(
            models.Autoapply, id=autoapply_id, owner=job_seeker
        )

    def put(self, request, *args, **kwargs):  # noqa
        autoapply = self.get_object()
        job_seeker = self.request.user.job_seeker
        service = services.AutoapplyService(job_seeker, autoapply)
        result = service.restart_autoapply()
        data = serializers.AutoapplySerializer(result).data
        return response.Response(data)


class AutoapplyToJobView(views.APIView):
    """
    View for applying of single job within the autoapply process.
    """
    permission_classes = (
        drf_permissions.IsAuthenticated,
        permissions.AutoApplyToJobPermission
    )

    def get_autoapply(self, autoapply_id):
        job_seeker = self.request.user.job_seeker
        return shortcuts.get_object_or_404(
            models.Autoapply, id=autoapply_id, owner=job_seeker
        )

    @staticmethod
    def get_job(job_id):
        return shortcuts.get_object_or_404(job_models.Job, id=job_id)

    def put(self, request, *args, **kwargs):  # noqa
        autoapply_id = self.kwargs.get('autoapply_pk')
        job_id = self.kwargs.get('job_pk')
        autoapply = self.get_autoapply(autoapply_id)
        job = self.get_job(job_id)
        validators.validate_apply_wont_exceed_autoapply_number(autoapply, job)
        job_seeker = self.request.user.job_seeker
        result = services.AutoapplyService(
            job_seeker, autoapply).autoapply_to_job(job)
        data = serializers.ApplySerializer(result).data
        return response.Response(data)


class ApplyCoverLetterUpdateView(generics.UpdateAPIView):
    """
    View for setting of apply cover letter.
    """
    permission_classes = (
        drf_permissions.IsAuthenticated,
        permissions.AutoApplyToJobPermission
    )
    serializer_class = serializers.UpdateApplyCoverLetterSerializer
    queryset = models.Apply.objects.all()

    def get_object(self):
        autoapply_pk = self.kwargs.get('autoapply_pk')
        job_pk = self.kwargs.get('job_pk')
        job_seeker = self.request.user.job_seeker
        obj = shortcuts.get_object_or_404(
            self.get_queryset(),
            autoapply_id=autoapply_pk,
            job_id=job_pk,
            owner=job_seeker
        )
        return obj


class AppliedJobsView(generics.ListAPIView):
    """View for watching applied jobs."""
    serializer_class = serializers.AppliedJobSerializer
    permission_classes = (
        drf_permissions.IsAuthenticated,
        permissions.AppliedJobsPermission
    )

    def get_queryset(self):
        qs = services.get_job_seeker_applied_jobs(self.request.user.job_seeker)
        qs = qs.order_by('-applied_at')
        return qs


class ApplyCreateView(generics.CreateAPIView):
    """
    View for creation of manual apply to the job.
    Request example:
    {\n
        "job": 1
    }

    Response example:
    {\n
        "job": 1,
        "owner": 1,
        "status": "APPLIED",
        "applied_at": "2018-09-24T11:03:59.912864Z"
    }
    """
    queryset = models.Apply.objects.all()
    permission_classes = (
        drf_permissions.IsAuthenticated,
        permissions.ApplyPermission
    )
    serializer_class = serializers.ApplySerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['job_seeker'] = self.request.user.job_seeker
        return context


class ReApplyJobView(generics.GenericAPIView):

    permission_classes = (
        drf_permissions.IsAuthenticated,
        permissions.ReApplyPermission
    )
    serializer_class = serializers.CoverLetterforReApplySerializer

    def post(self, request, *args, **kwargs):
        """View for reaaply for a job.
        Request data:\n
            {
                "cover_letter": 1  # id
            }
        This view is used for manual and for auto apply.
        All validations are like for usual apply.
        """
        job_seeker = request.user.job_seeker
        job = shortcuts.get_object_or_404(
            job_models.Job,
            id=kwargs.get('job_id'))
        apply = shortcuts.get_object_or_404(job.applies, owner=job_seeker)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cover_letter = serializer.validated_data.get('cover_letter')
        validators.validate_job_seeker_can_reapply(
            job_seeker,
            job,
            apply,
            cover_letter)
        apply = services.reapply_to_job(job_seeker, job, apply, cover_letter)
        return response.Response(data=serializers.ApplySerializer(apply).data)


class AutoApplyStatsView(views.APIView):

    permission_classes = (
        drf_permissions.IsAuthenticated,
        permissions.AutoApplyStatsPermission
    )

    def get(self, request, *args, **kwargs):
        """
        View information about job seeker's most recent auto applies.
        Example JSON response:\n
        ```
           [
                {
                    "id": 3,
                    "title": "6My autoapply",
                    "applied_jobs_cnt": 1,
                    "progress_percents": 16
                },
                {
                    "id": 2,
                    "title": "5My autoapply",
                    "applied_jobs_cnt": 2,
                    "progress_percents": 20
                },
                {
                    "id": 1,
                    "title": "4My autoapply",
                    "applied_jobs_cnt": 10,
                    "progress_percents": 33
                }
            ]
        ```
        """
        data = services.get_auto_applies_stats(request.user)
        return response.Response(data=data)
