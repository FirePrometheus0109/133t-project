from subscription import models


class SubscriptionCreateMixin:
    queryset = models.Subscription.objects.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['company_user'] = self.request.user.company_user
        return context
