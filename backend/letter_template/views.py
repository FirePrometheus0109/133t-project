from rest_framework import viewsets

from letter_template import models
from letter_template import serializers
from permission import permissions


class LetterTemplateViewSet(viewsets.ModelViewSet):

    """
    list:\n
        Endpoint with query paramters for searching:
            api/v1/letter-templates/?search=somestring
        Endpoint with query paramters for ordering:
            api/v1/letter-templates/?ordering=name
            api/v1/letter-templates/?ordering=-modified_at
    """

    queryset = models.LetterTemplate.objects.select_related('event_type')
    serializer_class = serializers.LetterTemplateSerializer
    permission_classes = (
        permissions.BaseModelPermissions,
        permissions.HasSubscription
    )
    search_fields = (
        'name',
    )
    ordering_fields = (
        'name',
        'modified_at'
    )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['company'] = self.get_request_company()
        return context

    def filter_queryset(self, queryset):
        company = self.get_request_company()
        queryset = queryset.filter(company=company)
        return super().filter_queryset(queryset)

    def get_request_company(self):
        return self.request.user.company_user.company
