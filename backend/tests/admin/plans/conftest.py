import pytest
from subscription import admin
from subscription import forms
from subscription import models


@pytest.fixture
def plans_admin(admin_site):
    return admin.PlanAdmin(models.Plan, admin_site)


@pytest.fixture
def plan_creation_form():
    return forms.CreatePlanForm
