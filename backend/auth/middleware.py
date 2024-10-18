from django.utils import timezone
from django.db import transaction

from auth import models


class UserActivityMiddleware:
    # PRECAUTION: Possible bottleneck with too often database hits.
    # If it will cause real troubles reduce this db write operations by
    # some timeout or cache `activity` information.

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        user = request.user
        if user.is_authenticated:
            try:
                models.UserActivity.objects.update_or_create(
                    user=user, defaults={'last_activity': timezone.now()})
            except transaction.TransactionManagementError:
                pass
        return response
