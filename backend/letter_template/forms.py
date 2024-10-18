from django import forms

from leet import mixins
from letter_template import models
from letter_template import utils
from letter_template import validators


class LetterTemplateForm(mixins.ValidationModelFormMixin, forms.ModelForm):

    class Meta:
        model = models.LetterTemplate
        fields = (
            'id',
            'event_type',
            'company',
            'name',
            'subject',
            'body',
        )

    def clean_name(self):
        name = self.cleaned_data.get('name')
        company = self.cleaned_data.get('company')
        validators.validate_name_letter_template(
            self.instance,
            company,
            name
        )
        return name

    def save(self, commit=False):
        company = self.cleaned_data.get('company')
        event_type = self.cleaned_data.get('event_type')
        utils.delete_default_letter_template_for_event(company, event_type)
        return super().save(commit=False)

    def clean(self):
        company = self.cleaned_data.get('company')
        validators.validate_count_of_existing_templates_admin(company)
        return self.cleaned_data
