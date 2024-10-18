# pylint: disable=abstract-method,no-member
from rest_auth import serializers as ra_serializers
from rest_framework import serializers

from company import constants
from company import models
from company import utils
from company import validators
from geo import serializers as geo_serializers
from geo import utils as geo_utils
from leet import enums
from leet import models as leet_models
from leet import serializers as base_serializers
from leet import validators as base_validators
from permission import models as perm_models
from permission import serializers as perm_serializers
from permission import utils as perm_utils
from subscription import serializers as subscription_serializers


class CompanyPublicDataSerializer(serializers.ModelSerializer):
    """
    This serializer holds base company data that can be showed public.
    """
    address = geo_serializers.AddressRequiredSerializer()
    photo = base_serializers.RestrictedVersatileImageFieldSerializer(
        sizes="thumbnail_images", allow_empty_file=True,
        required=False, read_only=True)

    class Meta:
        model = models.Company
        fields = (
            'id',
            'name',
            'description',
            'phone',
            'fax',
            'website',
            'email',
            'address',
            'industry',
            'photo',
        )

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if instance.industry:
            ret['industry'] = {
                'id': instance.industry.id,
                'name': instance.industry.name
            }
        return ret


class CompanySerializer(CompanyPublicDataSerializer):
    subscription = serializers.SerializerMethodField()
    is_billing_info_provided = serializers.SerializerMethodField()
    auto_renew_subscription = serializers.SerializerMethodField()

    class Meta(CompanyPublicDataSerializer.Meta):
        fields = CompanyPublicDataSerializer.Meta.fields + (
            'is_trial_available',
            'is_billing_info_provided',
            'is_profile_filled',
            'auto_renew_subscription',
            'subscription',
        )
        read_only_fields = (
            'is_trial_available',
            'is_profile_filled',
        )

    def update(self, company, validated_data):  # noqa
        address_data = validated_data.pop('address', None)
        if address_data:
            geo_utils.create_or_update_instance_address(company, address_data)
        company = super().update(company, validated_data)
        return company

    @staticmethod
    def get_subscription(instance):
        if hasattr(instance, 'customer'):
            subscription = instance.customer.subscriptions.filter(
                status=enums.SubscriptionStatusEnum.ACTIVE.name
            )
            if subscription.exists():
                return subscription_serializers.SubscriptionSerializer(
                    subscription[0]
                ).data
        return {}

    @staticmethod
    def get_is_billing_info_provided(instance):
        if hasattr(instance, 'customer'):
            return instance.customer.is_billing_info_provided
        return False

    @staticmethod
    def get_auto_renew_subscription(instance):
        if hasattr(instance, 'customer'):
            return instance.customer.auto_renew_subscription
        return False


class PhotoSerializer(base_serializers.PhotoSerializerMixin,
                      serializers.ModelSerializer):
    photo = base_serializers.RestrictedVersatileImageFieldSerializer(
        sizes='thumbnail_images', allow_empty_file=True,
        required=True, allow_null=True)

    class Meta:
        model = models.Company
        fields = ('id', 'photo')


class CompanyUserBaseSerializer(serializers.ModelSerializer):
    """Base Serializer for creating and updating company users."""

    first_name = serializers.CharField(max_length=256)
    last_name = serializers.CharField(max_length=256)
    permissions_groups = serializers.PrimaryKeyRelatedField(
        queryset=perm_models.PermissionGroup.objects.all(),
        write_only=True,
        many=True)

    class Meta:
        model = models.CompanyUser
        fields = (
            'id',
            'last_name',
            'first_name',
            'permissions_groups'
        )


class CompanyUserCreateSerializer(CompanyUserBaseSerializer):
    email = serializers.EmailField()

    class Meta(CompanyUserBaseSerializer.Meta):
        model = models.CompanyUser
        fields = CompanyUserBaseSerializer.Meta.fields + ('email',)

    def validate_email(self, email):
        validators.validate_company_user_is_not_deleted(
            email, self.context['company'])
        base_validators.validate_user_email_uniqueness(email)
        return email

    def validate(self, attrs):
        if self.instance is None:
            validators.validate_count_company_users_for_create(
                self.context['company'])
        return attrs

    def create(self, validated_data):
        return utils.create_or_restore_company_user(
            validated_data,
            self.context['company'],
            self.context['request'])


class CompanyUserUpdateSerializer(CompanyUserBaseSerializer):
    status = serializers.ChoiceField(
        constants.AVAILABLE_STATUSES_FOR_UPDATE,
        required=False)

    class Meta(CompanyUserCreateSerializer.Meta):
        fields = CompanyUserBaseSerializer.Meta.fields + ('status',)
        read_only_fields = ('email',)

    def validate_status(self, status):
        validators.validate_status_edited_user(self.instance)
        validators.validate_user_can_update_status(
            self.context['company_user'],
            self.instance,
            status)
        validators.validate_count_company_users_for_update(
            self.context['company'],
            self.instance,
            status)
        return status

    def validate_permissions_groups(self, permissions_groups):
        validators.validate_user_can_disable_permission_group(
            self.instance,
            self.context['company'],
            permissions_groups)
        return permissions_groups

    def update(self, instance, validated_data):
        return utils.update_company_user(instance, validated_data)


class CompanyUserSerializer(serializers.ModelSerializer):
    user = ra_serializers.UserDetailsSerializer()
    permissions_groups = serializers.SerializerMethodField()

    class Meta:
        model = models.CompanyUser
        fields = (
            'id',
            'user',
            'permissions_groups',
            'status'
        )

    @staticmethod
    def get_permissions_groups(company_user):
        groups = [
            g.permissiongroup for g in company_user.user.groups.order_by('id')
            if hasattr(g, 'permissiongroup')
        ]
        serializer_groups = perm_serializers.PermissionGroupSerializer(
            groups, many=True).data
        return perm_utils.group_perms_groups_for_response(serializer_groups)


class CompanyUserRestoreSerializer(CompanyUserCreateSerializer):

    def validate_email(self, email):
        validators.validate_company_user_restore_email(
            email,
            self.context['company'])
        return email


class CompanyEnumSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Company
        fields = (
            'id',
            'name'
        )


class CandidateStatusForScoreCardsSerializer(serializers.Serializer):

    statuses = serializers.PrimaryKeyRelatedField(
        queryset=leet_models.CandidateStatus.objects.all(),
        many=True
    )


class CompanyUserEnumSerializer(serializers.ModelSerializer):

    user = base_serializers.UserEnumSerializer()

    class Meta:
        model = models.CompanyUser
        fields = (
            'id',
            'user'
        )
