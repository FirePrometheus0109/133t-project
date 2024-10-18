from django.contrib import admin

from survey import models
from survey import forms
from leet import admin as base_admin


@admin.register(models.Question, site=base_admin.base_admin_site)
class QuestionAdmin(base_admin.BaseModelAdmin):

    form = forms.QuestionForm
    list_display = (
        'body',
        'is_answer_required',
        'answer_type',
        'disqualifying_answer',
        'is_active'
    )
    search_fields = ('body',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return (qs
                .filter(is_default=True)
                .select_related(
                    'job',
                    'company')
                .prefetch_related(
                    'surveys'
                ))
