from leet import enums
from tests import utils

EXPECTED_PLAN_LIST_ITEM = {
    'id': utils.Any(int),
    'name': utils.Any(str),
    'job_seekers_count': utils.Any(int),
    'jobs_count': utils.Any(int),
    'price': utils.Any(str),  # decimal field
    'deletion_date': utils.AnyOrNone(str),
    'new_price': utils.AnyOrNone(str),  # decimal field
    'price_apply_date': utils.AnyOrNone(str),
    'is_reporting_enabled': True,
    'users_number': utils.Any(int),
}

EXPECTED_TRIAL_SUBSCRIPTION = {
    'id': utils.Any(int),
    'plan': utils.Any(dict),
    'is_trial': True,
    'date_start': utils.Any(str),
    'date_end': utils.Any(str),
    'is_auto_renew': False,
    'balance': utils.Any(dict),
    'status': enums.SubscriptionStatusEnum.ACTIVE.name
}

EXPECTED_AUTORENEW_SUBSCRIPTION = {
    'id': utils.Any(int),
    'plan': utils.Any(dict),
    'is_trial': False,
    'date_start': utils.Any(str),
    'date_end': utils.Any(str),
    'is_auto_renew': True,
    'balance': utils.Any(dict),
    'next_subscription': None,
    'status': enums.SubscriptionStatusEnum.ACTIVE.name
}

EXPECTED_NOT_AUTORENEW_SUBSCRIPTION = {
    'id': utils.Any(int),
    'plan': utils.Any(dict),
    'is_trial': False,
    'date_start': utils.Any(str),
    'date_end': utils.Any(str),
    'is_auto_renew': False,
    'balance': utils.Any(dict),
    'next_subscription': None,
    'status': enums.SubscriptionStatusEnum.ACTIVE.name
}

EXPECTED_DOWNGRADED_SUBSCRIPTION = {
    'id': utils.Any(int),
    'plan': utils.Any(dict),
    'is_trial': False,
    'date_start': utils.Any(str),
    'date_end': utils.Any(str),
    'is_auto_renew': False,
    'balance': utils.Any(dict),
    'status': enums.SubscriptionStatusEnum.ACTIVE.name,
    'next_subscription': {
        'id': utils.Any(int),
        'plan': utils.Any(dict),
        'is_auto_renew': False,
        'status': enums.SubscriptionStatusEnum.SCHEDULED.name,
        'date_start': utils.Any(str),
        'date_end': utils.Any(str),
    },
}
