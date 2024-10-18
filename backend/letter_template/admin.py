from django.contrib import admin

from leet import admin as base_admin
from letter_template import models
from letter_template import forms


@admin.register(models.LetterTemplate, site=base_admin.base_admin_site)
class LetterTemplateAdmin(base_admin.BaseModelAdmin):

    form = forms.LetterTemplateForm
