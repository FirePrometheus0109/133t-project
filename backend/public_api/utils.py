from django.conf import settings


def get_social_names_and_ids():
    return {
        i['name']: i['client_id']
        for i in settings.SOCIALS_PROVIDERS_APPID_AND_SECRET
    }
