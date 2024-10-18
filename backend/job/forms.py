from django import forms
from rest_framework.exceptions import ValidationError as DrfValidationError

from job import models, validators
from leet.forms import ValidationFormSet
from leet.mixins import ValidationModelFormMixin


class JobForm(ValidationModelFormMixin, forms.ModelForm):

    class Meta:
        model = models.Job
        fields = '__all__'

    def clean_salary_max(self):
        salary_min = self.cleaned_data.get('salary_min')
        salary_max = self.cleaned_data.get('salary_max')
        validators.validate_salary(salary_min, salary_max)
        return salary_max

    def clean_education_strict(self):
        education = self.cleaned_data.get('education')
        education_strict = self.cleaned_data.get('education_strict', False)
        if education_strict and not education:
            raise DrfValidationError('Empty education can`t be strict')
        return education_strict

    def clean_closing_date(self):
        publish_date = self.cleaned_data.get('publish_date')
        closing_date = self.cleaned_data.get('closing_date')
        validators.validate_publish_and_closing_dates(
            publish_date, closing_date)
        if closing_date is not None:
            validators.validate_closing_date(closing_date)
        return closing_date

    def clean_publish_date(self):
        publish_date = self.cleaned_data.get('publish_date')
        if publish_date is not None:
            validators.validate_publish_date(
                job=self.instance, date=publish_date)
        return publish_date

    def clean_status(self):
        status = self.cleaned_data.get('status')
        if self.instance is not None:
            validators.validate_job_can_be_closed(self.instance, status)
        else:
            validators.validate_status_for_creating_job(status)
        return status


class JobSkillInlineForm(ValidationFormSet):

    def extended_clean(self):
        req = [s for s in self.cleaned_data if s.get('is_required')]
        opt = [s for s in self.cleaned_data if not s.get('is_required')]
        validators.validate_count_of_skills(req)
        validators.validate_count_of_skills(opt)
        validators.validate_skills(req, opt, is_obj=False)
