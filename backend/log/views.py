from rest_framework import mixins
from rest_framework import viewsets

from log import filters
from log import models
from log import serializers
from log import utils
from permission import permissions


class LogViewSet(mixins.ListModelMixin,
                 mixins.DestroyModelMixin,
                 viewsets.GenericViewSet):

    """
    list:
        view all company logs.
        Url for view company logs only for job seekers:\n
        api/v1/logs/?ct_model=jobseeker&object_id=1
        Url for view company logs job's logs:\n
        Example response JSON:\n
        ```
        {
            "count": 0,
            "next": null,
            "previous": null,
            "results":
            [
                {
                    "id": 2,
                    "owner": {
                        "id": 1,
                        "name": "cufirstname culastname"
                    },
                    "time": 2019-01-28T08:48:06Z,
                    "message": "deleted a comment.",
                    "other_info": {
                        "deleted_comment": {
                            "title": "what",
                            "user": {
                                "id": 1,
                                "name": "cufirstname culastname",
                                "company_user": {
                                    "id": 1,
                                }
                            },
                            "submit_date": 2019-01-28T08:48:06Z,
                            "comment": "ever"
                        }
                    }
                },
                {
                    "id": 1,
                    "owner": {
                        "id": 1,
                        "name": "cufirstname culastname"
                    },
                    "time": 2019-01-28T08:48:06Z,
                    "message": "left a comment.",
                    "other_info": {}
                }
            ]
        }
        ```
        Url for view company logs job's logs:\n
        api/v1/logs/?ct_model=job&object_id=1
    destroy:
        delete a log.
    """

    queryset = models.Log.objects.none()
    serializer_class = serializers.LogSerializer
    permission_classes = (
        permissions.BaseModelPermissions,
        permissions.HasSubscription
    )
    filterset_class = filters.LogFilterSet

    def filter_queryset(self, queryset):
        company = self.request.user.company_user.company
        queryset = utils.get_company_logs(company)
        return super().filter_queryset(queryset)
