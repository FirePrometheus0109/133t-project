# pylint: disable-msg=too-many-arguments,arguments-differ
from django import forms
from django.conf import settings as django_settings
from django.contrib.sites.models import Site
from django.contrib.contenttypes import models as ct_models
from django.forms.utils import ErrorList

from comment import models
from comment import fields
from job import models as job_models
from job_seeker import models as js_models


class BaseCommentCreationForm(forms.ModelForm):

    def save(self, user, commit=True):
        instance = super().save(commit=False)
        instance.user = user
        instance.site = Site.objects.get(
            id=getattr(django_settings, 'SITE_ID'))

        obj = self.get_source_obj()
        instance.content_type = ct_models.ContentType.objects.get_for_model(
            obj)
        instance.object_pk = obj.pk

        instance.save()
        return instance

    def get_source_obj(self):
        raise NotImplementedError


class JobCommentCreationForm(BaseCommentCreationForm):

    job = forms.ModelChoiceField(
        queryset=job_models.Job.objects.all(),
        required=True
    )

    class Meta:
        model = models.JobComment
        fields = ('title', 'comment')

    def get_source_obj(self):
        return self.cleaned_data.get('job')


class JobSeekerCommentCreationForm(BaseCommentCreationForm):

    job_seeker = forms.ModelChoiceField(
        queryset=js_models.JobSeeker.objects.all(),
        required=True
    )

    class Meta:
        model = models.JobSeekerComment
        fields = ('title', 'comment')

    def get_source_obj(self):
        return self.cleaned_data.get('job_seeker')


class BaseCommentChangeForm(forms.ModelForm):

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=None,
                 empty_permitted=False, instance=None,
                 use_required_attribute=None, renderer=None):
        super().__init__(
            data, files, auto_id, prefix, initial, error_class,
            label_suffix, empty_permitted, instance, use_required_attribute,
            renderer)
        self.update_initial_value()

    def update_initial_value(self):
        raise NotImplementedError


class JobCommentChangeForm(BaseCommentChangeForm):

    job = fields.CommentModelChoiceField(
        queryset=job_models.Job.objects.all(),
        disabled=True
    )

    class Meta:
        model = models.JobComment
        fields = ('title', 'comment', 'ban_status')

    def update_initial_value(self):
        self.initial['job'] = self.instance.content_object


class JobSeekerCommentChangeForm(BaseCommentChangeForm):

    job_seeker = fields.CommentModelChoiceField(
        queryset=js_models.JobSeeker.objects.all(),
        disabled=True
    )

    class Meta:
        model = models.JobComment
        fields = ('title', 'comment', 'ban_status')

    def update_initial_value(self):
        self.initial['job_seeker'] = self.instance.content_object
