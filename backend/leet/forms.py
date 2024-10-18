from django.forms import BaseInlineFormSet
from django.core.exceptions import ValidationError
from rest_framework.exceptions import ValidationError as DrfValidationError


class ValidationFormSet(BaseInlineFormSet):
    """
    Extend base validation to handle `Validation error` from `rest_framework`.
    """

    def clean(self):
        clean = super().clean()
        if self.is_valid():
            try:
                self.extended_clean()
            except DrfValidationError as e:
                raise ValidationError(e.detail[0])
        return clean

    def extended_clean(self):
        raise NotImplementedError
