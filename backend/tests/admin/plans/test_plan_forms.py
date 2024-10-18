import pytest
import copy
from tests.admin.plans import constants


class TestCommentForms:
    @pytest.mark.usefixtures('create_stripe_plan_mock')
    def test_create_general_plan_form_success(
            self, plan_creation_form, admin_user):
        plan_data = constants.PLAN_DATA
        form_instance = plan_creation_form(plan_data)

        assert form_instance.is_valid()
        plan = form_instance.save(admin_user)
        assert plan.name == plan_data['name']
        assert plan.jobs_count == plan_data['jobs_count']
        assert plan.job_seekers_count == plan_data['job_seekers_count']
        assert plan.price == plan_data['price']
        assert not plan.is_custom
        assert not plan.company
        assert plan.stripe_id

    @pytest.mark.usefixtures('create_stripe_plan_mock')
    def test_create_custom_plan_form_success(
            self, plan_creation_form, admin_user, company):
        plan_data = copy.deepcopy(constants.PLAN_DATA)
        plan_data.update({'company': company.id})
        form_instance = plan_creation_form(plan_data)

        assert form_instance.is_valid()
        plan = form_instance.save(admin_user)
        assert plan.name == plan_data['name']
        assert plan.jobs_count == plan_data['jobs_count']
        assert plan.job_seekers_count == plan_data['job_seekers_count']
        assert plan.price == plan_data['price']
        assert plan.users_number == plan_data['users_number']
        assert plan.is_custom
        assert plan.company == company
        assert plan.stripe_id

    @pytest.mark.parametrize(('field',), (
        ('name',),
        ('jobs_count',),
        ('job_seekers_count',),
        ('price',),
    ))
    def test_create_plan_form_invalid_without_required_fields(
            self, field, plan_creation_form, admin_user):
        data = constants.PLAN_DATA.copy()
        data.pop(field)
        form_instance = plan_creation_form(data)
        assert not form_instance.is_valid()
