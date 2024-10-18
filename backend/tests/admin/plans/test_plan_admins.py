from tests.admin.plans import expected


class TestPlanAdmin:
    def test_plan_creation_form_fields(
            self, plans_admin, admin_request):
        fields = plans_admin.get_fields(admin_request)
        assert fields == expected.PLAN_CREATION_FORM_FIELDS
