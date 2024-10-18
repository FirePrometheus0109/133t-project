from allauth import utils
from rest_framework import exceptions

from leet import constants


def validate_user_email_uniqueness(email):
    if utils.email_address_exists(email):
        raise exceptions.ValidationError(
            constants.USER_WITH_CERTAIN_EMAIL_EXISTS)

def validate_file_size(file_size, max_size_mb, error_msg):
    max_size = max_size_mb * 1024 * 1024
    if file_size > max_size:
        raise exceptions.ValidationError(error_msg)


def validate_file_extension(extension, valid_extensions, error_msg):
    if extension not in valid_extensions:
        raise exceptions.ValidationError(error_msg)
