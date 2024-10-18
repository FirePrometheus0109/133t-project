from django import forms

from subscription import models
from subscription import utils


class CreatePlanForm(forms.ModelForm):

    class Meta:
        model = models.Plan
        fields = (
            'name',
            'job_seekers_count',
            'jobs_count',
            'price',
            'company',
            'is_reporting_enabled',
            'users_number',
        )

    def save(self, commit=True):
        company = self.cleaned_data.get('company')
        if company:
            self.instance.is_custom = True
        stripe_plan = utils.create_stripe_plan(self.instance)
        self.instance.stripe_id = stripe_plan['id']
        return super().save(commit=commit)


class UpdatePlanForm(forms.ModelForm):
    class Meta:
        model = models.Plan
        fields = (
            'name',
            'job_seekers_count',
            'jobs_count',
            'price',
            'company',
            'is_active',
            'is_reporting_enabled',
            'users_number',
        )

    def save(self, commit=True):
        # handle only price and is_active flag changes because of requirements
        # (amekin) What requirements?
        new_price = self.cleaned_data.get('price')
        is_active = self.cleaned_data.get('is_active')
        self.instance.refresh_from_db()
        is_price_changed = (new_price is not None
                            and new_price != self.instance.price)
        if is_price_changed:
            self.instance.new_price = new_price
            price_apply_date = utils.get_plan_change_or_delete_apply_date()
            self.instance.price_apply_date = price_apply_date
        if is_active is not None:
            self.instance.is_active = is_active
        is_reporting_enabled = self.cleaned_data.get('is_reporting_enabled')
        self.instance.is_reporting_enabled = is_reporting_enabled
        instance = super().save(commit)
        if is_price_changed:
            utils.notify_users_about_price_changes(instance)
        return instance
