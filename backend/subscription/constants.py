STARTER_PACKAGE = {
    'name': 'Starter Package',
    'metadata': {
        'is_custom': False,
        'job_postings_number': 2,
        'profile_views_number': 0
    },
    'price': 0
}

BASIC_PACKAGE_3 = {
    'name': 'Basic Package-3',
    'metadata': {
        'is_custom': False,
        'job_postings_number': 3,
        'profile_views_number': 50
    },
    'price': 36
}

BASIC_PACKAGE_5 = {
    'name': 'Basic Package-5',
    'metadata': {
        'is_custom': False,
        'job_postings_number': 5,
        'profile_views_number': 100
    },
    'price': 50
}

BASIC_SMALL_BUSINESS_PACKAGE_10 = {
    'name': 'Basic Small Business Package-10',
    'metadata': {
        'is_custom': False,
        'job_postings_number': 10,
        'profile_views_number': 200
    },
    'price': 60
}

BASIC_SMALL_BUSINESS_PACKAGE_20 = {
    'name': 'Basic Small Business Package-20',
    'metadata': {
        'is_custom': False,
        'job_postings_number': 20,
        'profile_views_number': 300
    },
    'price': 80
}

CORPORATE_PACKAGE_30 = {
    'name': 'Corporate Package-30',
    'metadata': {
        'is_custom': False,
        'job_postings_number': 30,
        'profile_views_number': 400
    },
    'price': 90
}

CORPORATE_PACKAGE_40 = {
    'name': 'Corporate Package-40',
    'metadata': {
        'is_custom': False,
        'job_postings_number': 40,
        'profile_views_number': 500
    },
    'price': 120
}

ENTERPRISE_CORPORATE_PACKAGE_50 = {
    'name': 'Enterprise Corporate Package-50',
    'metadata': {
        'is_custom': False,
        'job_postings_number': 50,
        'profile_views_number': 600
    },
    'price': 150
}

ENTERPRISE_CORPORATE_PACKAGE_75 = {
    'name': 'Enterprise Corporate Package-75',
    'metadata': {
        'is_custom': False,
        'job_postings_number': 75,
        'profile_views_number': 1000
    },
    'price': 225
}

DEFAULT_PLANS = (
    STARTER_PACKAGE,
    BASIC_PACKAGE_3,
    BASIC_PACKAGE_5,
    BASIC_SMALL_BUSINESS_PACKAGE_10,
    BASIC_SMALL_BUSINESS_PACKAGE_20,
    CORPORATE_PACKAGE_30,
    CORPORATE_PACKAGE_40,
    ENTERPRISE_CORPORATE_PACKAGE_50,
    ENTERPRISE_CORPORATE_PACKAGE_75,
)

USD_CURRENCY_ISO_CODE = 'usd'

CENTS_IN_DOLLAR = 100

TRIAL_SUBSCRIPTION_NOTIFICATION_TEMPLATE_NAME = (
    'trial_expires_notification.html'
)

SUBSCRIPTION_PLAN_CHANGE_TEMPLATE_NAME = 'plan_was_deleted_notification.html'
SUBSCRIPTION_PLAN_DELETE_TEMPLATE_NAME = 'plan_will_deleted_notification.html'
SUBSCRIPTION_PRICE_CHANGE_TEMPLATE_NAME = (
    'plan_price_changes_notification.html'
)

FIRST_NOTIFICATION_DAYS_BEFORE = 5
SECOND_NOTIFICATION_DAYS_BEFORE = 1

SUBSCRIPTION_CYCLE_BILLING_REASON = 'subscription_cycle'
PAYMENT_SUCCEEDED = 'invoice.payment_succeeded'
SUBSCRIPTION_DELETED = 'customer.subscription.deleted'

# Error messages
CANT_SUBSCRIBE_TO_NOT_YOUR_COMPANY_PLAN = (
    'You can\'t subscribe to plan that doesn\'t belong to your company.'
)

PLAN_CANT_BE_SELECTED = 'This package can no longer be selected.'

TRIAL_SUBSCRIPTION_IS_ALREADY_USED = 'Trial subscription is already used.'

YOU_ALREADY_PURCHASED_SUBSCRIPTION = (
    'You have already purchased {plan} '
    'for period from {date_start} to {date_end}'
)

BILLING_INFORMATION_REQUIRED_ERROR = (
    'Please, provide billing information to purchase subscription.'
)

FAILED_TO_PROCESS_PAYMENT_ERROR = (
    'Failed to process your payment. '
    'Try again later or change your credit card.'
)

PURCHASE_SUBSCRIPTION_FAILED_BECAUSE_OF_DATABASE_LOCK = (
    'Somebody from your company is purchasing subscription right now. '
    'Try again later.'
)

FAILED_TO_PURCHASE_TRIAL_SUBSCRIPTION_ERROR = (
    'Failed to purchase trial subscription. Try again later.'
)

PLAN_HAS_NOT_REPORTING_ERROR = (
    'The current plan does not include reporting functionality'
)

PLAN_NUMBER_OF_USERS_EXCEEDED_ERROR = (
    'The current plan does not allow '
    'the creation of more than {} active users'
)