from rest_framework import exceptions
from rest_framework import status


class PurchaseSubscriptionError(exceptions.APIException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
