from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED

from company import constants


class CompanyUserCreateRestoreMixin:

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.context['company'] = self.get_company()
        serializer.is_valid(raise_exception=True)
        invited_user, created = serializer.save()
        self.send_invited_user_email(invited_user)
        status = HTTP_201_CREATED if created else HTTP_200_OK
        return Response(
            data={'detail': constants.COMPANY_USER_CREATE_SUCCESS_MESSAGE},
            status=status)

    def get_company(self):
        return self.request.user.company_user.company

    def get_company_user(self):
        return self.request.user.company_user
