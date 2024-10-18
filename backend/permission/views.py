from rest_framework import generics
from rest_framework.response import Response

from permission import models, permissions, serializers, utils, constants


class PermissionsGroupsView(generics.GenericAPIView):

    queryset = models.PermissionGroup.objects.order_by('id')
    serializer_class = serializers.PermissionGroupSerializer
    permission_classes = (
        permissions.BaseModelPermissions,
    )

    def get(self, request, *args, **kwargs):
        """
        Return list of grouped permissions groups.
        Example JSON response:\n
            [
                {
                    title: "Comment in the candidates profile",
                    permissions: [
                        {
                            "id": 12,
                            "name": "Manage comments ...",
                            "description": "Full access to working ..."
                        },
                        {
                            "id": 13,
                            "name": "View and add comments ...",
                            "description": "View comments, ..."
                        }
                    ]
                },
                ...
            ]
        """
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        resp_data = utils.group_perms_groups_for_response(serializer.data)
        return Response(data=resp_data)


class InitialPermissionsGroupsView(PermissionsGroupsView):

    def get_queryset(self):
        return self.queryset.filter(
            name__in=constants.INITIAL_INVITED_COMPANY_USERS_PERMISSIONS_GROUPS
        )
