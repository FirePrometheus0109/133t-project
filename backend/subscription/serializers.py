# pylint: disable=abstract-method
from rest_framework import serializers

from subscription import models
from subscription import services
from subscription import validators


class SubscriptionSerializerMixin:
    class Meta:
        model = models.Subscription
        fields = (
            'id',
            'plan',
            'is_trial',
            'date_start',
            'date_end',
            'is_auto_renew',
            'balance',
            'status',
        )
        read_only_fields = (
            'is_auto_renew',
            'is_trial',
            'date_start',
            'date_end',
            'status',
        )

    @staticmethod
    def get_balance(subscription):
        balance = subscription.customer.balance
        bal = {
            'job_seekers_remain': balance.job_seekers_remain,
            'job_seekers_total': balance.job_seekers_total,
            'jobs_remain': balance.jobs_remain,
            'jobs_total': balance.jobs_total,
        }
        return bal

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['plan'] = SubscriptionPlanSerializer(instance.plan).data
        return ret

    def validate_plan(self, plan):
        company = self.context['company_user'].company
        validators.validate_plan(plan, company)
        validators.validate_plan_isnt_for_deletion(plan)
        return plan


class TrialSubscriptionSerializer(SubscriptionSerializerMixin,
                                  serializers.ModelSerializer):
    plan = serializers.PrimaryKeyRelatedField(
        queryset=models.Plan.objects.filter(price__gt=0)
    )
    balance = serializers.SerializerMethodField()

    def create(self, validated_data):
        subscription = services.SubscribeService(
            company_user=self.context['company_user']
        ).subscribe(
            plan=validated_data['plan'],
            is_trial=True
        )
        return subscription


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Plan
        fields = (
            'id',
            'name',
            'job_seekers_count',
            'jobs_count',
            'price',
            'deletion_date',
            'new_price',
            'price_apply_date',
            'is_reporting_enabled',
            'users_number',
        )


class SubscriptionSerializer(SubscriptionSerializerMixin,
                             serializers.ModelSerializer):
    plan = serializers.PrimaryKeyRelatedField(
        queryset=models.Plan.objects.all()
    )
    balance = serializers.SerializerMethodField()
    next_subscription = serializers.SerializerMethodField()

    class Meta(SubscriptionSerializerMixin.Meta):
        fields = (SubscriptionSerializerMixin.Meta.fields
                  + ('next_subscription',))

    def create(self, validated_data):
        company_user = self.context['company_user']
        plan = validated_data['plan']
        subscription = services.SubscribeService(company_user).subscribe(plan)
        return subscription

    def validate(self, attrs):
        attrs = super().validate(attrs)
        validators.validate_billing_information(
            attrs['plan'],
            self.context['company_user'].company.customer
        )
        validators.validate_next_subscription_hasnt_chosen(
            self.context['company_user'].company
        )
        return attrs

    @staticmethod
    def get_next_subscription(subscription):
        if subscription.next_subscription:
            return {
                'id': subscription.next_subscription.id,
                'plan': SubscriptionPlanSerializer(
                    subscription.next_subscription.plan).data,
                'is_auto_renew': subscription.next_subscription.is_auto_renew,
                'date_start': subscription.next_subscription.date_start,
                'date_end': subscription.next_subscription.date_end,
                'status': subscription.next_subscription.status,
            }
        return None


class BillingInformationCreateSerializer(serializers.Serializer):
    token = serializers.CharField()
    email = serializers.EmailField()
    auto_renew_subscription = serializers.BooleanField()
