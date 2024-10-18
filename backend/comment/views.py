import json

from django import shortcuts
from django.conf import settings
from django.contrib.contenttypes import models as ct_models
from rest_framework import permissions as drf_permissions
from rest_framework import viewsets

from comment import models
from comment import permissions
from comment import serializers
from job import models as job_models
from job_seeker import models as js_models
from leet import services as base_services
from log import constants as log_constants
from log import utils as log_utils
from permission import permissions as base_permissions


class BaseCommentViewSet(viewsets.ModelViewSet):
    permission_classes = (
        drf_permissions.IsAuthenticated,
        permissions.CommentPermission,
        base_permissions.HasSubscription
    )

    def filter_queryset(self, queryset):
        user_company = self.request.user.company_user.company
        queryset = super().filter_queryset(queryset)
        queryset = queryset.filter(
            user__company_user__company=user_company,
            is_removed=False
        )
        queryset = base_services.get_ban_status_active_entities(queryset)
        if self.action == 'list':
            queryset = queryset.filter(object_pk=self.kwargs.get('pk'))
            return queryset.order_by('-submit_date')
        return queryset

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        view_comment, _ = self.get_comment_view()
        new_comments = self.queryset.filter(
            submit_date__gt=view_comment.modified_at).count()
        # modify view object to correctly count `new comments`
        view_comment.save()
        response.data['new_comments'] = new_comments
        return response

    def perform_create(self, serializer):
        super().perform_create(serializer)
        source = serializer.validated_data.get('source')
        log_utils.create_log(
            self.request.user,
            log_constants.LogEnum.comment_left.name,
            log_constants.LogEnum.comment_left.value,
            source)
        comment_view, is_created = self.get_comment_view(source)
        if not is_created:
            comment_view.save()

    def get_comment_view(self, source=None):
        if source is None:
            source = self.get_source_object(self.kwargs.get('pk'))
        return models.ViewComment.objects.get_or_create(
            user=self.request.user,
            content_type=ct_models.ContentType.objects.get_for_model(source),
            object_pk=source.pk
        )

    def get_source_object(self, pk):
        raise NotImplementedError

    def perform_update(self, serializer):
        serializer.save()
        log_utils.create_log(
            self.request.user,
            log_constants.LogEnum.comment_edit.name,
            log_constants.LogEnum.comment_edit.value,
            serializer.instance.content_object)

    def perform_destroy(self, instance):
        """
        Delete comment and create log about deleted comment.
        Save information about deleted comment for view this comment on UI.
        """
        source = instance.content_object
        other_info = {
            'deleted_comment': {
                'title': instance.title,
                'user': {
                    'id': instance.user.id,
                    'name': instance.user.get_full_name(),
                    'company_user': {
                        'id': instance.user.company_user.id
                    }
                },
                'submit_date': instance.submit_date.strftime(
                    settings.DEFAULT_SERVER_DATETIME_FORMAT),
                'comment': instance.comment
            }
        }
        other_info = json.dumps(other_info)
        instance.delete()
        log_utils.create_log(
            self.request.user,
            log_constants.LogEnum.comment_delete.name,
            log_constants.LogEnum.comment_delete.value,
            source,
            other_info=other_info)


class JobSeekerCommentViewSet(BaseCommentViewSet):
    """
    list:
         View for obtaining comment list attached to the `JobSeeker`.

    create:
        View for creating comment attached to the `JobSeeker`.
        'source' - `JobSeeker` id.
    """
    queryset = models.JobSeekerComment.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.CreateJobSeekerCommentSerializer
        return serializers.JobSeekerCommentSerializer

    def get_source_object(self, pk):
        return shortcuts.get_object_or_404(js_models.JobSeeker.objects, pk=pk)


class JobCommentViewSet(BaseCommentViewSet):
    """
    list:
         View for obtaining comment list attached to the `Job`.

    create:
        View for creating comment attached to the `Job`.
        'source' - `Job` id.
    """
    queryset = models.JobComment.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.CreateJobCommentSerializer
        return serializers.JobCommentSerializer

    def get_source_object(self, pk):
        return shortcuts.get_object_or_404(job_models.Job.objects, pk=pk)
