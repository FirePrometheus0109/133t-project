from django import http as dj_http
from django.core import exceptions as dj_exceptions
from rest_framework import exceptions
from rest_framework import response
from rest_framework import status
from rest_framework import views


def exception_handler(exc, context):  # noqa
    """
    Returns the response that should be used for any given exception.
    """
    if isinstance(exc, exceptions.APIException):
        # headers' logic like in default DRF exception_handler
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = str(exc.wait)

        if isinstance(exc.detail, dict):
            if exc.detail.get('non_field_errors', None):
                data = {'errors': exc.detail['non_field_errors']}
            else:
                data = {'field_errors': exc.detail}
        elif isinstance(exc.detail, list):
            data = {'errors': exc.detail}
        else:
            data = {'errors': [exc.detail]}
            views.set_rollback()
        return response.Response(data, status=exc.status_code, headers=headers)

    elif isinstance(exc, dj_http.Http404):
        msg = exceptions.NotFound.default_detail
        data = {'errors': [msg]}
        views.set_rollback()
        return response.Response(data, status=status.HTTP_404_NOT_FOUND)

    elif isinstance(exc, dj_exceptions.PermissionDenied):
        msg = exceptions.PermissionDenied.default_detail
        data = {'errors': [msg]}
        views.set_rollback()
        return response.Response(data, status=status.HTTP_403_FORBIDDEN)

    return None
