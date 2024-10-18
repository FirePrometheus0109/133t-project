import io

import pytest
from allauth.socialaccount import models
from django.core import management

from auth import constants


def test_set_social_appid_and_secret_command(db, settings):
    stdout = io.StringIO()
    management.call_command('set_social_appid_and_secret', stdout=stdout)
    apps = models.SocialApp.objects.all()
    result = stdout.getvalue()
    for app in apps:
        assert app.name in settings.SOCIALACCOUNT_PROVIDERS
        assert app.name in result

def test_social_appid_and_secret_command_no_required_value(db, settings):
    settings.SOCIALS_PROVIDERS_APPID_AND_SECRET[0]['secret'] = ''
    emsg = constants.SET_SOCIAL_APPID_AND_SECRET_ERROR
    with pytest.raises(management.CommandError, message=emsg) as exc:
        management.call_command('set_social_appid_and_secret')
        assert exc.message == emsg
