from allauth.socialaccount import models
from django.core import management
from django.conf import settings
from django.contrib.sites import models as sites_models

from auth import constants


class Command(management.BaseCommand):

    requires_migrations_checks = True
    output_transaction = True
    help = 'Create or update social entries in allauth social models.'

    def handle(self, *args, **options):
        social_apps = []
        for i in settings.SOCIALS_PROVIDERS_APPID_AND_SECRET:
            name = i['name']
            client_id = i['client_id']
            secret = i['secret']

            if not all((name, client_id, secret)):
                raise management.CommandError(
                    constants.SET_SOCIAL_APPID_AND_SECRET_ERROR
                )

            app, _ = models.SocialApp.objects.update_or_create(
                name=name,
                provider=name,
                defaults={
                    'client_id': client_id,
                    'secret': secret
                }
            )
            social_apps.append(app)
            site = sites_models.Site.objects.get(id=settings.SITE_ID)
            site.socialapp_set.add(*social_apps)
        result = [
            constants.SET_SOCIAL_APPID_AND_SECRET_SUCCESS.format(app.name)
            for app in social_apps]
        self.stdout.writelines(result)
