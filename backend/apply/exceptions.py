from rest_framework import exceptions


class ApplyException(exceptions.APIException):
    status_code = 400
