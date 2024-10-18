from django import forms


class CommentModelChoiceField(forms.ModelChoiceField):
    """
    Intentional prevention of saving value since this field don't have
    straight bound with model, but connected as generic foreign key with mark
    `disabled`.
    """

    def to_python(self, value):
        assert self.disabled, (
            '{} class must have a `disabled=True` attribute '.format(
                self.__class__.__name__))
        self.required = False
