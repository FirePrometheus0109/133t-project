
import os
from celery import Celery
from django.apps import apps, AppConfig
from django.conf import settings


if not settings.configured:
    # set the default Django settings module for the 'celery' program.
    os.environ.setdefault(
        'DJANGO_SETTINGS_MODULE',
        'leet.settings.dev'
    )  # pragma: no cover


app = Celery('leet')


class CeleryAppConfig(AppConfig):
    name = 'leet.taskapp'
    verbose_name = 'Celery Config'

    def ready(self):
        # Using a string here means the worker will not have to
        # pickle the object when using Windows.
        # - namespace='CELERY' means all celery-related configuration keys
        #   should have a `CELERY_` prefix.
        app.config_from_object('django.conf:settings', namespace='CELERY')
        installed_apps = [
            app_config.name for app_config in apps.get_app_configs()
        ]
        app.autodiscover_tasks(lambda: installed_apps, force=True)

        if hasattr(settings, 'SENTRY_DSN'):
            # Celery signal registration
            # Since raven is required in production only,
            # imports might (most surely will) be wiped out
            # during PyCharm code clean up started
            # in other environments.
            # @formatter:off
            import sentry_sdk  # pylint: disable=import-error
            from sentry_sdk.integrations.celery import CeleryIntegration

            sentry_sdk.init(
                settings.SENTRY_DSN,
                integrations=[CeleryIntegration()],
                environment=settings.SENTRY_ENVIRONMENT_TAG
            )


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')  # pragma: no cover
