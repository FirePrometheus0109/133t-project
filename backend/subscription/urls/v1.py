from django.urls import path

from subscription import views

app_name = 'api_v1_subscriptions'

urlpatterns = [
    path(
        'subscription/trial-plan/',
        views.TrialSubscriptionPlanList.as_view(),
        name='trial-plan-list'
    ),
    path(
        'subscription/plan/',
        views.SubscriptionPlanList.as_view(),
        name='plan-list'
    ),
    path(
        'subscription/trial/',
        views.TrialSubscriptionCreate.as_view(),
        name='trial-subscription-create'
    ),
    path(
        'subscription/',
        views.SubscriptionCreate.as_view(),
        name='subscription-create'
    ),
    path(
        'subscription/<int:pk>/unsubscribe/',
        views.UnsubscribeFromPlan.as_view(),
        name='unsubscribe'
    ),
    path(
        'subscription/active/',
        views.ActiveSubscriptionRetrieve.as_view(),
        name='subscription-active'
    ),
    path(
        'subscription/billing-information/',
        views.BillingInformationCreate.as_view(),
        name='billing-information-create'
    ),
    path(
        'subscription/payment-history/',
        views.PaymentsHistoryRetrieve.as_view(),
        name='payment_history'
    ),
    path(
        'webhooks/subscription/',
        views.SubscriptionWebhook.as_view(),
        name='subscription-webhook'
    ),
]
