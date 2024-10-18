from django.db import models as orm
from rest_framework import filters as drf_filters
from rest_framework import generics
from rest_framework import permissions as drf_permissions
from rest_framework import response
from rest_framework import views
from rest_framework import viewsets

from company import constants
from company import mixins
from company import models
from company import ordering
from company import permissions as company_permissions
from company import serializers
from company import utils
from company import validators
from leet import enums
from leet import serializers as leet_serializers
from permission import permissions
from subscription import permissions as subscription_permissions


class CompanyRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):

    permission_classes = (
        drf_permissions.IsAuthenticated,
        company_permissions.CompanyPermission,
        permissions.HasSubscription
    )
    serializer_class = serializers.CompanySerializer

    def get_queryset(self):
        return (models.Company
                      .objects
                      .prefetch_related('jobs')
                      .filter(id=self.kwargs.get('pk')))


class CompanyPhotoUpdateView(generics.UpdateAPIView):
    queryset = models.Company.objects.all()
    serializer_class = serializers.PhotoSerializer
    permission_classes = (
        drf_permissions.IsAuthenticated,
        company_permissions.CompanyLogoPermission,
        permissions.HasSubscription
    )


class CompanyUserViewSet(mixins.CompanyUserCreateRestoreMixin,
                         viewsets.ModelViewSet):
    """
    ViewSet for managing company users.
    list:
        Return list of company users.\n
        Example response JSON:
            [
                {
                    "id": 273,
                    "user": {
                        "pk": 367,
                        "username": "9QWFyYwFDJ7g",
                        "email": "unique@mail.com",
                        "first_name": "first_name",
                        "last_name": "last_name"
                    },
                    "permissions_groups": [
                        {
                            title: "Comment in the candidates profile",
                            permissions: [
                                {
                                    "id": 12,
                                    "name": "Manage comments ...",
                                    "description": "Full access to working ..."
                                },
                                ...
                            ]
                        ...
                        }
                    ],
                    "status": "NEW"
                },
                ...
            ]
    create:
        Create new company user.\n
        Example request data:
            {
                "last_name": "string",
                "first_name": "string",
                "email": "email@email.com",
                "permissions_groups": [1, 2, 3] (can be blank array)
            }
        Errors:
            User with the same email exists in the system.
            Max count of company users.
            There is deleted user in company with certain email
                emsg - There is deleted user with certain email in company.
    update:
        Edit company user (PUT).\n
        "email" field is read_only.
        Errors:
            User changes status fot himself.
            User sends status "NEW".
            User disables permissions groups "Manage company users"
                or "Manage Subscription plan" if only edited user has
                this permissions in company.
            User try to change status of user with status "NEW".
            User try to change status of disabled user if in company
                ("ACTIVE" + "NEW") == 10 users.
    retrieve:
        Return company user details.
    partial_update:
        Not Allowed.
    destroy:
        Delete company_user account.\n
        Errors:
            User try delete his account.
    """
    http_method_names = (
        'get', 'post', 'put', 'delete', 'head', 'options', 'trace'
    )
    queryset = (models.CompanyUser.objects
                                  .select_related(
                                      'user')
                                  .prefetch_related(
                                      'user__groups',
                                      'user__groups__permissiongroup')
                                  .order_by(
                                      ordering.COMPANY_USERS_LIST_ORDERING,
                                      'user__first_name',
                                      'user__last_name'))
    permission_classes = (
        permissions.BaseModelPermissions,
        permissions.HasSubscription
    )

    def filter_queryset(self, queryset):
        company = self.get_company()
        queryset = queryset.filter(company=company)
        return super().filter_queryset(queryset)

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.CompanyUserCreateSerializer
        if self.action == 'update':
            return serializers.CompanyUserUpdateSerializer
        return serializers.CompanyUserSerializer

    def update(self, request, *args, **kwargs):
        company_user = self.get_object()
        serializer = self.get_serializer(
            company_user,
            data=request.data)
        serializer.context['company'] = self.get_company()
        serializer.context['company_user'] = self.get_company_user()
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return response.Response(
            data=serializers.CompanyUserSerializer(company_user).data)

    def perform_destroy(self, instance):
        company_user = self.get_company_user()
        validators.validate_user_can_be_deleted(company_user, instance)
        utils.soft_delete_company_user(instance)

    def send_invited_user_email(self, invited_user):
        utils.send_invited_user_email(
            constants.INVITED_COMPANY_USER_TEMPLATE_NAME,
            invited_user,
            self.get_company_user())


class CompanyUserRestoreView(mixins.CompanyUserCreateRestoreMixin,
                             generics.GenericAPIView):

    serializer_class = serializers.CompanyUserRestoreSerializer
    permission_classes = (
        drf_permissions.IsAuthenticated,
        company_permissions.CompanyUserRestorePermission,
        permissions.HasSubscription
    )

    def post(self, request, *args, **kwargs):
        """
        Restore deleted company user.\n
        Example request data:
            {
                "last_name": "string",
                "first_name": "string",
                "email": "email@email.com",
                "permissions_groups": [1, 2, 3] (can be blank array)
            }
        Errors:
            Certain email does not belong to deleted company user.
        """
        return self.create(request, *args, **kwargs)

    def send_invited_user_email(self, invited_user):
        utils.send_invited_user_email(
            constants.RESTORED_COMPANY_USER_TEMPLATE_NAME,
            invited_user,
            self.get_company_user())


class CompanyEnumView(generics.ListAPIView):

    """get:
        Return list of all registred companies id and names
        for autocomplete for filters by companies on find job page.
        Response is not paginated.
    """

    queryset = models.Company.objects.order_by('name')
    pagination_class = None
    serializer_class = serializers.CompanyEnumSerializer
    filter_backends = (drf_filters.SearchFilter,)
    search_fields = ('name',)


class CandidatesStatusesManagementView(views.APIView):

    permission_classes = (
        drf_permissions.IsAuthenticated,
        company_permissions.CandidatesStatusesManagePermission,
        permissions.HasSubscription
    )

    def post(self, request, *args, **kwargs):
        """
        View for manage viewed candidaets statuses' scorecards
        Example request data:\n
            {
                "statuses": [1, 2, 3],
            }
        permissions: Only company users can manage viewed statuses scorecards
        Example response JSON:\n
            [
                {
                    "id": 1,
                    "name": "Applied"
                },
                {
                    "id": 2,
                    "name": "Screened"
                }
                ...
            ]
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        company_user = request.user.company_user
        company_user.candidate_statuses.clear()
        company_user.candidate_statuses.add(
            *serializer.validated_data['statuses'])
        company_user.save()
        data = leet_serializers.CandidateStatusSerializer(
            company_user.candidate_statuses, many=True).data
        return response.Response(data=data)

    @staticmethod
    def get_serializer(**kwargs):
        # this method used for swagger
        return serializers.CandidateStatusForScoreCardsSerializer(**kwargs)


class CompanyUserEnumView(generics.ListAPIView):

    """get:
        Return list of all active company users' id and names.
        Can search candidates by names (first and last).
    """

    queryset = models.CompanyUser.objects.select_related('user')
    pagination_class = None
    permission_classes = (
        drf_permissions.IsAuthenticated,
        company_permissions.CompanyUserEnumPermission,
        permissions.HasSubscription
    )
    serializer_class = serializers.CompanyUserEnumSerializer
    filter_backends = (drf_filters.SearchFilter,)
    search_fields = (
        'user__first_name',
        'user__last_name'
    )

    def get_queryset(self):
        return (
            self
            .queryset
            .filter(
                company=self.request.user.company_user.company,
                status=enums.CompanyUserStatusEnum.ACTIVE.name)  # noqa
        )


class JobOwnersView(generics.ListAPIView):
    permission_classes = (
        drf_permissions.IsAuthenticated,
        company_permissions.CompanyUserEnumPermission,
        permissions.HasSubscription
    )
    serializer_class = serializers.CompanyUserEnumSerializer

    def get_queryset(self):
        queryset = models.CompanyUser.objects.annotate(
            jobs_count=orm.Count('jobs')
        ).filter(company=self.request.user.company_user.company,
                 jobs_count__gt=0)
        return queryset
