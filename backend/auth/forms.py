from django import forms
from django.contrib.auth import forms as auth_forms
from django.core import exceptions

from auth import services
from auth import validators
from company import models
from company import validators as company_validators
from job_seeker import validators as js_validators
from leet import forms as base_forms
from leet import mixins as base_mixins
from leet import validators as leet_validators
from permission import utils


class UserResetPasswordForm(forms.Form):
    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }
    new_password = forms.CharField(
        label="New password",
        widget=forms.PasswordInput,
        strip=False,
    )
    new_password_confirm = forms.CharField(
        label="New password confirmation",
        strip=False,
        widget=forms.PasswordInput,
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_new_password_confirm(self):
        password1 = self.cleaned_data.get('new_password')
        password2 = self.cleaned_data.get('new_password_confirm')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        auth_forms.password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user


class UserSetPasswordForm(UserResetPasswordForm):

    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        self.fields.pop('new_password_confirm')

    def clean_new_password(self):
        field_name = 'new_password'
        password1 = self.cleaned_data.get(field_name)
        if password1:
            try:
                validator = validators.BaseCharacterPasswordValidator
                validator.validate(password1)
            except exceptions.ValidationError:
                self.add_error(field_name, validator.get_help_text())
        return password1


class CreateUserForm(auth_forms.UserCreationForm):

    def save(self, commit=True):
        user = super().save(commit=True)
        user.is_staff = True
        user.save()
        return user


class CreateCompanyUserForm(auth_forms.UserCreationForm):
    company = forms.ModelChoiceField(
        queryset=models.Company.objects.all(),
        required=True
    )
    is_owner = forms.BooleanField(
        help_text='Grant all permissions for this company'
    )

    def clean_company(self):
        company = self.cleaned_data.get('company')
        company_validators.validate_count_company_users_for_create(company)
        return company

    def save(self, commit=True):
        user = super().save(commit=True)
        company = self.cleaned_data.get('company')
        is_owner = self.cleaned_data.get('is_owner')
        return services.create_company_user(user, company, is_owner)


class CreateJobSeekerForm(auth_forms.UserCreationForm):

    def save(self, commit=True):
        user = super().save(commit=True)
        return services.create_job_seeker(user)


class ChangeUserForm(base_mixins.ValidationModelFormMixin,
                     auth_forms.UserChangeForm):

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if (utils.is_company_user(self.instance) and
                'email' in self.changed_data):
            company_validators.validate_company_user_is_not_deleted(
                email, self.instance.company_user.company)
            leet_validators.validate_user_email_uniqueness(email)
        return email


class CompanyUserInlineFormset(base_forms.ValidationFormSet):

    def extended_clean(self):
        status = self.cleaned_data[0].get('status')
        company_validators.validate_count_company_users_for_update(
            self.instance.company_user.company,
            self.instance.company_user,
            status)


class JobSeekerInlineFormset(base_forms.ValidationFormSet):

    def extended_clean(self):
        cleaned_data = self.cleaned_data[0]

        salary_min = cleaned_data.get('salary_min')
        salary_max = cleaned_data.get('salary_max')
        js_validators.validate_salary(
            self.instance.job_seeker, salary_min, salary_max)

        is_public = cleaned_data.get('is_public')
        js_validators.validate_can_public(self.instance.job_seeker, is_public)
        phone = cleaned_data.get('phone')
        js_validators.validate_phone(phone)


class PasswordResetForm(auth_forms.PasswordResetForm):
    email = forms.EmailField(label="Email", max_length=256)
