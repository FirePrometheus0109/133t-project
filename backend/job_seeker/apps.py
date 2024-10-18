from django.apps import AppConfig


class JobSeekerConfig(AppConfig):
    name = 'job_seeker'

    def ready(self):
        import job_seeker.signals  # noqa
