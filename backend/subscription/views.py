# pylint: disable=no-member
import stripe
from django import shortcuts
from django.conf import settings
from django.db import transaction
from django.utils import decorators
from rest_framework import generics
from rest_framework import permissions as rest_permissions
from rest_framework import response
from rest_framework import status
from rest_framework import views

from leet import enums
from permission import permissions as base_permissions
from subscription import constants
from subscription import mixins
from subscription import models
from subscription import permissions
from subscription import serializers
from subscription import services
from subscription import utils
from subscription import webhook_handlers


class SubscriptionPlanList(generics.ListAPIView):
    """
    Returns public plans and custom plans that belong to company
    """
    permission_classes = (
        rest_permissions.IsAuthenticated,
        permissions.SubscribePermission,
    )
    serializer_class = serializers.SubscriptionPlanSerializer

    def get_queryset(self):
        custom_plans = models.Plan.objects.filter(
            company=self.request.user.company_user.company)
        if custom_plans.first() and not custom_plans.first().deletion_date:
            queryset = custom_plans
        else:
            queryset = models.Plan.objects.filter(
                is_custom=False, is_deleted=False
            )
        return queryset.order_by('price')


class TrialSubscriptionPlanList(SubscriptionPlanList):
    """
    Returns plans that're available for trial subscription
    """
    permission_classes = (
        rest_permissions.IsAuthenticated,
        permissions.TrialSubscribePermission,
    )
    queryset = (models.Plan.objects
                .filter(price__gt=0, is_custom=False,
                        deletion_date__isnull=True)
                .order_by('price'))

    def get_queryset(self):
        return self.queryset


@decorators.method_decorator(transaction.non_atomic_requests, name='dispatch')
class TrialSubscriptionCreate(mixins.SubscriptionCreateMixin,
                              generics.CreateAPIView):
    permission_classes = (
        rest_permissions.IsAuthenticated,
        permissions.TrialSubscribePermission,
    )
    serializer_class = serializers.TrialSubscriptionSerializer


@decorators.method_decorator(transaction.non_atomic_requests, name='dispatch')
class SubscriptionCreate(mixins.SubscriptionCreateMixin,
                         generics.CreateAPIView):
    permission_classes = (
        rest_permissions.IsAuthenticated,
        permissions.SubscribePermission,
    )
    serializer_class = serializers.SubscriptionSerializer


class ActiveSubscriptionRetrieve(generics.RetrieveAPIView):
    permission_classes = (permissions.ViewActiveSubscriptionPermission,)
    serializer_class = serializers.SubscriptionSerializer
    queryset = models.Subscription.objects.all()

    def get_object(self):
        active_subscription = shortcuts.get_object_or_404(
            models.Subscription,
            customer__company=self.request.user.company_user.company,
            status=enums.SubscriptionStatusEnum.ACTIVE.name
        )
        return active_subscription


class UnsubscribeFromPlan(views.APIView):
    permission_classes = (permissions.SubscribePermission,)

    def get_object(self):
        customer = self.request.user.company_user.company.customer
        subscription_id = self.kwargs.get('pk')
        return shortcuts.get_object_or_404(
            customer.subscriptions, id=subscription_id)

    def put(self, request, *args, **kwargs):  # noqa
        subscription = self.get_object()
        company_user = request.user.company_user
        services.SubscribeService(company_user).unsubscribe(subscription)
        return response.Response(status=status.HTTP_200_OK)


class BillingInformationCreate(generics.CreateAPIView):
    permission_classes = (permissions.SubscribePermission,)
    serializer_class = serializers.BillingInformationCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['token']
        email = serializer.validated_data['email']
        auto_renew_subscription = serializer.validated_data[
            'auto_renew_subscription']
        services.BillingInformationService(
            self.request.user.company_user
        ).set_billing_information(token, email, auto_renew_subscription)
        return response.Response(status=status.HTTP_201_CREATED)


class PaymentsHistoryRetrieve(views.APIView):
    permission_classes = (
        permissions.ViewActiveSubscriptionPermission,
        base_permissions.HasSubscription
    )

    def get(self, request):
        customer = getattr(request.user.company_user.company, 'customer')
        if customer:
            payments_history = utils.get_payments_history(customer)
            return response.Response(status=status.HTTP_200_OK,
                                     data=payments_history)
        return response.Response(status.HTTP_404_NOT_FOUND)


@decorators.method_decorator(transaction.non_atomic_requests, name='dispatch')
class SubscriptionWebhook(views.APIView):
    permission_classes = (rest_permissions.AllowAny,)

    def post(self, request):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        endpoint_secret = settings.WEBHOOKS_SIGNING_SECRET
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError:
            return response.Response(status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.SignatureVerificationError:
            return response.Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            if request.data['type'] == constants.SUBSCRIPTION_DELETED:
                webhook_handlers.subscription_cancel(event)
            elif request.data['type'] == constants.PAYMENT_SUCCEEDED:
                webhook_handlers.payment_succeeded(event)
            return response.Response(status=status.HTTP_200_OK)
