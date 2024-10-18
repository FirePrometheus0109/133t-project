from django import forms

from survey import models


class QuestionForm(forms.ModelForm):

    class Meta:
        model = models.Question
        fields = (
            'body',
            'is_answer_required',
            'answer_type',
            'disqualifying_answer',
        )

    def save(self, commit=True):
        instance = super().save(False)
        instance.is_default = True
        instance.save()
        return instance
