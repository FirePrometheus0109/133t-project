import mimetypes
import os

import magic

from django.conf import settings
from django.template.defaultfilters import filesizeformat
from django.contrib import auth
from rest_framework import serializers
from rest_framework import exceptions
from versatileimagefield.serializers import VersatileImageFieldSerializer

from leet import models
from leet import validators
from leet import constants

User = auth.get_user_model()


class RestrictedVersatileImageFieldSerializer(VersatileImageFieldSerializer):
    default_error_messages = {
        "max_upload_size":
            "File size must be under {max_upload_size}."
            " Current file size is {file_size}.",
        'content_type':
            "File content type must be {content_types}."
            " Current file content type is {file_content_type}.",
    }

    def to_representation(self, value):
        file_name = value and value.name and os.path.basename(value.name)
        if not file_name:
            return None
        result = super().to_representation(value)
        if result:
            result["name"] = file_name
        for key, img_url in result.items():
            if key in ['small', 'original'] and ':443' in img_url:
                new_img_url = \
                    img_url.replace(':443', '').replace('http', 'https')
                result[key] = new_img_url
        return result

    def to_internal_value(self, data):
        try:
            file_size = data.size
            file_name = data.name
            file_content_type = data.content_type
            if file_content_type == "application/octet-stream":
                file_content_type = mimetypes.guess_type(file_name)[0]
        except AttributeError:
            self.fail('invalid')

        validators.validate_file_size(file_size, constants.PHOTO_MAX_SIZE_MB,
                                      constants.PHOTO_FILE_SIZE_ERROR)
        validators.validate_file_extension(
            self._get_extension(data), constants.PHOTO_VALID_EXTENSIONS,
            constants.NOT_VALID_PHOTO_EXTENSION_ERROR)

        return super().to_internal_value(data)

    def _get_extension(self, f):
        """Get image extension."""
        extension_mapping = {
            'image/jpeg': '.jpeg',
            'image/tiff': '.tiff'
        }
        mimetype = magic.from_buffer(f.read(), mime=True)
        f.seek(0)
        extension = extension_mapping.get(mimetype, None)
        if not extension:
            extension = mimetypes.guess_extension(mimetype)
            if not extension:
                raise exceptions.ValidationError('The file has an unknown extension')
        return extension[1:]


class CandidateStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CandidateStatus
        fields = (
            'id',
            'name'
        )


class EventTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.EventType
        fields = (
            'id',
            'name'
        )


class UserEnumSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'name'
        )

    @staticmethod
    def get_name(user):
        return user.get_full_name()


class PhotoSerializerMixin:

    def update(self, instance, validated_data):
        if validated_data['photo'] is None and instance.photo:  # noqa
            instance.photo.delete_all_created_images()
            instance.photo.delete(save=True)
            return instance
        elif validated_data['photo'] and instance.photo:
            instance.photo.delete_all_created_images()
            instance.photo.delete(save=False)
        instance = super().update(instance, validated_data)
        return instance
