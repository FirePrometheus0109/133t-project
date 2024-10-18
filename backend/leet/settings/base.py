"""
Base settings to build other settings files upon.
"""

import datetime
import pathlib

import environ
import stripe
from celery import schedules

ROOT_DIR = environ.Path(__file__) - 4  # (133t/backend/leet/settings/base.py - 4 = 133t/)
APPS_DIR = ROOT_DIR.path('app')

env = environ.Env()

READ_DOT_ENV_FILE = env.bool('DJANGO_READ_DOT_ENV_FILE', default=False)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(ROOT_DIR.path('.env')))

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool('DJANGO_DEBUG', False)
# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
TIME_ZONE = 'UTC'
# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en-us'
# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1
# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

DEFAULT_SERVER_DATE_FORMAT = "%Y-%m-%d"
DEFAULT_SERVER_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
DATE_FORMAT_FOR_CLOSING_JOBS_EMAIL_TEMPLATE = '%m/%d/%Y'
DATE_FORMAT_FOR_TRIAL_EXPIRES_EMAIL_TEMPLATE = '%d{suffix} of %B'

# REST_FRAMEWORK
# ------------------------------------------------------------------------------
#
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication'
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
        'rest_framework.filters.SearchFilter',
    ],
    'EXCEPTION_HANDLER': 'leet.views.exception_handler',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100,
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'DATE_FORMAT': DEFAULT_SERVER_DATE_FORMAT,
    'DATETIME_FORMAT': DEFAULT_SERVER_DATETIME_FORMAT
}

REST_USE_JWT = True

JWT_AUTH = {
    'JWT_ALLOW_REFRESH': True,
    'JWT_VERIFY_EXPIRATION': True,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
}

REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'auth.serializers.UserDetailsSerializer',
    'LOGIN_SERIALIZER': 'auth.serializers.LoginSerializer',
    'PASSWORD_RESET_SERIALIZER': 'auth.serializers.UserPasswordResetSerializer',
    'PASSWORD_RESET_CONFIRM_SERIALIZER': 'auth.serializers.PasswordResetConfirmSerializer'
}

OLD_PASSWORD_FIELD_ENABLED = True

# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASE_URL = f"postgres://{env('POSTGRES_USER')}:{env('POSTGRES_PASSWORD')}@{env('POSTGRES_HOST')}:{env('POSTGRES_PORT')}/{env('POSTGRES_DB')}"
DATABASES = {
    'default': env.db('DATABASE_URL', default=DATABASE_URL),
}
DATABASES['default']['ATOMIC_REQUESTS'] = True

IMPORT_EXPORT_USE_TRANSACTIONS = True

# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = 'leet.urls.base'
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'leet.wsgi.application'

# APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres'
]
THIRD_PARTY_APPS = [
    'constance',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'rest_framework',
    'django_filters',
    'corsheaders',
    'rest_framework.authtoken',
    'rest_auth.registration',
    'versatileimagefield',
    'threadedcomments',
    'django_comments',
    'notifications',
    'rangefilter',
    'import_export',
    'constance.backends.database',
]
LOCAL_APPS = [
    'leet',
    'auth',
    'apply',
    'candidate',
    'company',
    'geo',
    'job',
    'job_seeker',
    'permission',
    'survey',
    'comment',
    'subscription',
    'log',
    'notification_center',
    'letter_template',
    'event'
    # Your stuff: custom apps go here
]
# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# AUTHENTICATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    'auth.backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
AUTH_USER_MODEL = 'auth.User'
# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
# LOGIN_REDIRECT_URL = 'users:redirect'
# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
# LOGIN_URL = 'account_login'


# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
    {
        'NAME': 'auth.validators.BaseCharacterPasswordValidator',
    },
]

# MIDDLEWARE
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'leet.middleware.CacheControlMiddleware',
    'auth.middleware.UserActivityMiddleware',
]


# STATIC
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR('staticfiles'))
# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [
    str(APPS_DIR.path('static')),
]
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR('media'))
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES_ROOT = APPS_DIR.path('templates')
TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        'DIRS': [
            str(TEMPLATES_ROOT),
            str(TEMPLATES_ROOT.path('emails')),
            str(TEMPLATES_ROOT.path('account')),
            str(TEMPLATES_ROOT.path('account', 'email')),
        ],
        'OPTIONS': {
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
            'debug': DEBUG,
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
# http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# FIXTURES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#fixture-dirs
FIXTURE_DIRS = (
    str(APPS_DIR.path('fixtures')),
)

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = 'admin/'
# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [
    ("""Developer""", 'anmekin@gmail.com'),
]
# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# Celery
# ------------------------------------------------------------------------------
INSTALLED_APPS += ['leet.taskapp.celery.CeleryAppConfig']
if USE_TZ:
    # http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-timezone
    CELERY_TIMEZONE = TIME_ZONE
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-broker_url
CELERY_BROKER_URL = env('CELERY_BROKER_URL', default=env('REDIS_URL'))
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-result_backend
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-accept_content
CELERY_ACCEPT_CONTENT = ['json']
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-task_serializer
CELERY_TASK_SERIALIZER = 'json'
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-result_serializer
CELERY_RESULT_SERIALIZER = 'json'
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-time-limit
# TODO: set to whatever value is adequate in your circumstances
CELERYD_TASK_TIME_LIMIT = 5 * 60
# http://docs.celeryproject.org/en/latest/userguide/configuration.html#task-soft-time-limit
# TODO: set to whatever value is adequate in your circumstances
CELERYD_TASK_SOFT_TIME_LIMIT = 60

CELERY_BEAT_SCHEDULE = {
    'publish-jobs-task': {
        'task': 'publish-jobs',
        'schedule': schedules.crontab(minute="*/10")
    },
    'find-jobs-task': {
        'task': 'find-autoapply-jobs',
        'schedule': schedules.crontab(minute="*/10")
    },
    'hard-delete-jobs-task': {
        'task': 'hard-delete-jobs',
        'schedule': schedules.crontab(minute="*/10")
    },
    'send-autoapply-web-notifications-task': {
        'task': 'send-autoapply-web-notifications',
        'schedule': schedules.crontab(minute="*/10")
    },
    'send-autoapply-email-notifications-task': {
        'task': 'send-autoapply-email-notifications',
        'schedule': schedules.crontab(minute=0, hour=9)
    },
    'close-expired-jobs-task': {
        'task': 'close-expired-jobs',
        'schedule': schedules.crontab(minute="*/10")
    },
    'notify-job-owners-about-closing-date-task': {
        'task': 'notify-job-owners-about-closing-date',
        'schedule': schedules.crontab(minute=0, hour=10)
    },
    'send-trial-expiration-notifications-task': {
        'task': 'send-trial-expiration-notifications',
        'schedule': schedules.crontab(minute=0)
    },
    'send-profile-views': {
        'task': 'send-profile-views',
        'schedule': schedules.crontab(minute=0, hour=9)
    },
    'delete-subscription-plans': {
        'task': 'delete-subscription-plans',
        'schedule': schedules.crontab(minute="*/10")
    },
    'update-plan-prices': {
        'task': 'update-plan-prices',
        'schedule': schedules.crontab(minute="*/10")
    },
    'sync-customer-invoices': {
        'task': 'sync-customer-invoices',
        'schedule': schedules.crontab(hour="*/4", minute=0)
    }
}
# django-allauth
# ------------------------------------------------------------------------------
ACCOUNT_ALLOW_REGISTRATION = env.bool('DJANGO_ACCOUNT_ALLOW_REGISTRATION', True)
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_AUTHENTICATION_METHOD = 'email'
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_EMAIL_REQUIRED = True
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_EMAIL_MAX_LENGTH = 255
# https://django-allauth.readthedocs.io/en/latest/configuration.html

ACCOUNT_USERNAME_REQURIED = False

ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_ADAPTER = 'auth.adapters.BaseAllauthAdapter'
# https://django-allauth.readthedocs.io/en/latest/configuration.html
SOCIALACCOUNT_ADAPTER = 'auth.adapters.SocialAccountAdapter'
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_USERNAME_VALIDATORS = "auth.validators.custom_username_validators"
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_USER_DISPLAY = 'auth.utils.get_user_display'

SOCIAL_AUTH_FACEBOOK_NAME = env(
    'SOCIAL_AUTH_FACEBOOK_NAME', default='facebook')
SOCIAL_AUTH_FACEBOOK_APP_ID = env('SOCIAL_AUTH_FACEBOOK_APP_ID', default='')
SOCIAL_AUTH_FACEBOOK_SECRET = env('SOCIAL_AUTH_FACEBOOK_SECRET', default='')

SOCIAL_AUTH_GOOGLE_NAME = env('SOCIAL_AUTH_GOOGLE_NAME', default='google')
SOCIAL_AUTH_GOOGLE_APP_ID = env('SOCIAL_AUTH_GOOGLE_APP_ID', default='')
SOCIAL_AUTH_GOOGLE_SECRET = env('SOCIAL_AUTH_GOOGLE_SECRET', default='')

SOCIALS_PROVIDERS_APPID_AND_SECRET = [
    {
        'name': SOCIAL_AUTH_FACEBOOK_NAME,
        'provider': SOCIAL_AUTH_FACEBOOK_NAME,
        'client_id': SOCIAL_AUTH_FACEBOOK_APP_ID,
        'secret': SOCIAL_AUTH_FACEBOOK_SECRET
    },
    {
        'name': SOCIAL_AUTH_GOOGLE_NAME,
        'provider': SOCIAL_AUTH_GOOGLE_NAME,
        'client_id': SOCIAL_AUTH_GOOGLE_APP_ID,
        'secret': SOCIAL_AUTH_GOOGLE_SECRET
    }
]

SOCIALACCOUNT_PROVIDERS = {
    SOCIAL_AUTH_FACEBOOK_NAME: {
        'METHOD': 'oauth2',
        'SCOPE': ['email', 'public_profile', 'user_friends'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'INIT_PARAMS': {'cookie': True},
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
            'verified',
            'locale',
            'timezone',
            'link',
            'gender',
            'updated_time',
        ],
        'EXCHANGE_TOKEN': True,
        'LOCALE_FUNC': lambda request: 'en_US',
        'VERIFIED_EMAIL': True,
        'VERSION': 'v2.12',
    },
    SOCIAL_AUTH_GOOGLE_NAME: {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

# Stripe
# ------------------------------------------------------------------------------
STRIPE_PUBLIC_KEY = env('STRIPE_PUBLIC_KEY', default='')
STRIPE_SECRET_KEY = env('STRIPE_SECRET_KEY', default='')
WEBHOOKS_SIGNING_SECRET = env('WEBHOOKS_SIGNING_SECRET', default='')
STRIPE_LIVE_MODE = env.bool("STRIPE_LIVE_MODE", default=False)
STRIPE_API_VERSION = '2018-11-08'

stripe.api_key = STRIPE_SECRET_KEY
stripe.api_version = STRIPE_API_VERSION

TRIAL_PERIOD_LENGTH = 30
# Your stuff...
# ------------------------------------------------------------------------------
DOMAIN_NAME = env('DOMAIN_NAME')
HTTP_SCHEME = env('HTTP_SCHEME', default='http')
VERIFY_EMAIL_TEMPLATE_URL = '{http}://{domain_name}/#/verify-email/{code}'
RECOVER_ACCOUNT_TEMPLATE_URL = '{http}://{domain_name}/#/restore-account/{id}/{token}'
PASSWORD_RESET_TEMPLATE_URL = '{http}://{domain_name}/#/reset-password'
INVITED_COMPANY_USER_TEMPLATE_URL = '{http}://{domain_name}/#/sign-up/{id}/{token}'
AUTOAPPLY_DETAILS_URL = '{http}://{domain_name}/#/auto-apply/edit/{id}'
JOB_DETAILS_URL = '{http}://{domain_name}/#/company/job/{id}/details'
COMPANY_PROFILE_DETAILS_URL = '{http}://{domain_name}/#/company/profile/{id}/view'
COMPANY_DASHBOARD_URL = '{http}://{domain_name}/#/company/dashboard'
NOTIFICATION_LIST_URL = '{http}://{domain_name}/#/notification/list'

VALIDATION_REGEXPS = {
    'password_validator': r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,32}$',
    'phone_number_validator': r'^[\d-]{7,14}$',
}
NUMBER_OF_AUTOAPPLIES_FOR_STATS_FOR_DASHBOARD = 3
HARD_DELETE_JOBS_INTERVAL_LENGTH = 183  # six months
MAX_EMAIL_LENGTH = 256
COUNT_OF_DAYS_FOR_SENDING_EMAIL_BEFORE_CLOSING_JOBS = 3
MONTHS_COUNT_BEFORE_PLAN_CHANGES_APPLY = 3

MAX_SALARY = 999999999

# Images
USER_PHOTO_DIR = 'user_photo'
VERSATILEIMAGEFIELD_SETTINGS = {
    'create_images_on_demand': True
}
VERSATILEIMAGEFIELD_RENDITION_KEY_SETS = {
    'thumbnail_images': [
        ('original', 'url'),
        ('small', 'thumbnail__24x24')
    ],
    'profile_logo_images': [
        ('original', 'url'),
        ('small', 'thumbnail__50x50')
    ],
    'profile_images': [
        ('url', 'url'),
        ('thumbnail', 'thumbnail__240x240')
    ]
}

COMMENTS_APP = 'threadedcomments'

USER_CONSIDERED_ONLINE_TIME_DELTA = 10  # minutes

UNKNOWN_VERSION = 'unknown'
version = UNKNOWN_VERSION
version_file = APPS_DIR / pathlib.Path('VERSION')
try:
    with open(version_file) as vf:
        version = vf.read().strip()
    version_date = datetime.date.fromtimestamp(version_file.lstat().st_mtime)
except FileNotFoundError:
    version = UNKNOWN_VERSION
    version_date = datetime.date.today()

changes = []
changes_file = APPS_DIR / pathlib.Path('CHANGES')
try:
    with open(changes_file) as cf:
        changes_data = cf.readlines()
except FileNotFoundError:
    changes_data = []

default_cv = {'name': 'unknown', 'children': []}
current_version = default_cv
for line in changes_data:
    if 'Version' in line:
        if current_version and current_version != default_cv:
            changes += [current_version]
        current_version_name = line.strip().replace('Version ', '').replace(':', '')
        current_version = {'name': current_version_name, 'children': []}
    elif line.strip():
        current_version['children'] += [{'name': line.strip().lstrip(' -')}]
if current_version and current_version != default_cv:
    changes += [current_version]

CHANGELOG = changes
APP_VERSION = {'version': version, 'date': version_date, 'changelog': CHANGELOG}

NUMBER_SHORT_NOTIFICATIONS = 4
DJANGO_NOTIFICATIONS_CONFIG = {
    'USE_JSONFIELD': True
}

NUMBER_DAYS_FOR_QUICK_LIST = 5
MAX_COUNT_OF_LETTER_TEMPLATES_FOR_COMPANY = 100
MAX_COUNT_OF_CANDIDATES_FOR_EVENT = 10
MAX_COUNT_OF_COLLEAGUES_FOR_EVENT = 10
VALID_TIME_MINUTE_VALUE_FOR_EVENT = (0, 30)

REQUEST_QUERY_PARAMETERS_FALSE_VALUE = (False, 'False', 'false', '0')
REQUEST_QUERY_PARAMETERS_TRUE_VALUES = (True, 'True', 'true', '1')

# Constance
CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
CONSTANCE_CONFIG = {
    'AUTOAPPLY_PERIOD_LENGTH': (1, 'Autoapply Period Length'),
}
