import pytest

from leet import enums
from tests.admin.auth import expected


class TestUserAdmin:
    @pytest.mark.parametrize(('user_type', 'exp'), (
            (
                'default',
                expected.BASE_USER_CREATION_FORM,
            ),
            (
                enums.AuthGroupsEnum.JOB_SEEKER.value,
                expected.JOB_SEEKER_CREATION_FORM,
            ),
            (
                enums.AuthGroupsEnum.COMPANY_USER.value,
                expected.COMPANY_USER_CREATION_FORM,
            ),
    ))
    def test_base_user_creation_form_fields(
            self, auth_model_admin, admin_request, user_type, exp):
        admin_request.update_request_type(user_type)
        fields = auth_model_admin.get_fields(admin_request)
        assert fields == exp
        assert (auth_model_admin.search_fields ==
                expected.BASE_USER_SEARCH_FIELDS)
        assert (auth_model_admin.sortable_by ==
                expected.BASE_USER_SORTABLE_FIELDS)
        assert (auth_model_admin.sortable_by ==
                expected.BASE_USER_SORTABLE_FIELDS)

    @pytest.mark.parametrize(('user_obj',), (
            (
                'company_user',
            ),
            (
                'job_seeker',
            ),
            (
                'admin_user',
            ),
    ))
    def test_user_change_form_fields(self, auth_model_admin, admin_request,
                                     request, user_obj):
        obj = request.getfixturevalue(user_obj)
        fields = auth_model_admin.get_fields(admin_request, obj)
        assert fields == expected.BASE_USER_FORM_FIELDS
        exclude_fields = auth_model_admin.get_exclude(admin_request, obj)
        assert exclude_fields is None

    @pytest.mark.parametrize(('user_obj',), (
            (
                'company_user',
            ),
            (
                'job_seeker',
            ),
            (
                'admin_user',
            ),
    ))
    def test_user_fieldsets(self, auth_model_admin, admin_request, request,
                            user_obj):
        obj = request.getfixturevalue(user_obj)
        fieldsets = auth_model_admin.get_fieldsets(admin_request, obj)
        assert fieldsets == expected.BASE_USER_FIELDSETS

    @pytest.mark.parametrize(('inline_site', 'user_obj', 'exp'), (
            (
                'company_user_inline',
                'company_user',
                expected.COMPANY_USER_INLINE_FIELDS,
            ),
            (
                'job_seeker_inline',
                'job_seeker',
                expected.JOB_SEEKER_INLINE_FIELDS,
            ),
    ))
    def test_user_inlines_fields(self, admin_request, request, inline_site,
                                 user_obj, exp):
        inline = request.getfixturevalue(inline_site)
        obj = request.getfixturevalue(user_obj)

        form = inline.get_formset(admin_request, obj).form
        for field in exp:
            assert field in form.base_fields
        assert len(exp) == len(form.base_fields)
