from django.conf import settings as django_settings
from django.contrib.contenttypes import models as ct_models


class CreateCommentSerializerMixin:

    def create(self, validated_data):
        source = validated_data.pop('source')
        validated_data['content_type'] = (
            ct_models.ContentType.objects.get_for_model(source))
        validated_data['object_pk'] = source.pk
        # https://docs.djangoproject.com/en/2.1/ref/contrib/sites/
        validated_data['site_id'] = getattr(django_settings, 'SITE_ID')
        request = self.context.get('request')
        if request:
            validated_data['user'] = request.user
        return super().create(validated_data)
