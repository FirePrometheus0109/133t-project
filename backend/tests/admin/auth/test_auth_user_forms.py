import pytest

from tests.admin.auth import constants
from company import models as company_models
from job_seeker import models as js_models


class TestUserCreationForms:

    @pytest.mark.parametrize('base_user_creation_form', [
        # password mismatch
        {
            'username': 'hello',
            'password1': 'world',
            'password2': 'noworld',
        },
        # password too weak
        {
            'username': 'wierd_name',
            'password1': 'world',
            'password2': 'world',
        },
        # password to similar with name
        {
            'username': 'company_user',
            'password1': 'company_user',
            'password2': 'company_user',
        },
        # username validation
        {
            'username': 'q',
            'password1': 'strong@passw0rd1',
            'password2': 'strong@passw0rd1',
        },
        # avoid @ in username
        {
            'username': 'normalu@sername',
            'password1': 'strong@passw0rd1!',
            'password2': 'strong@passw0rd1!',
        },
    ], indirect=True)
    def test_cant_create_user_invalid_data(self, admin_user,
                                           base_user_creation_form):
        assert not base_user_creation_form.is_valid()

    @pytest.mark.parametrize('base_user_creation_form', [
        constants.BASE_VALID_CREDENTIALS,
    ], indirect=True)
    def test_can_create_user_with_valid_data(self, base_user_creation_form):
        assert base_user_creation_form.is_valid()
        user = base_user_creation_form.save()
        assert user.is_staff is True
        assert user.username == constants.BASE_VALID_CREDENTIALS['username']

    @pytest.mark.parametrize('company_user_creation_form', [
        constants.COMPANY_USER_VALID_CREDENTIALS,
    ], indirect=True)
    def test_cant_create_company_user_without_company(
            self, company_user_creation_form, company):
        assert not company_user_creation_form.is_valid()
        # update user form with company and re-run validation
        company_user_creation_form.data['company'] = company.id
        company_user_creation_form.full_clean()
        assert company_user_creation_form.is_valid()
        user = company_user_creation_form.save()
        assert user.company_user.company == company
        assert (user.username == constants.COMPANY_USER_VALID_CREDENTIALS[
            'username'])
        assert isinstance(user.company_user, company_models.CompanyUser)

    @pytest.mark.parametrize('job_seeker_creation_form', [
        constants.BASE_VALID_CREDENTIALS,
    ], indirect=True)
    def test_can_create_job_seeker(self, job_seeker_creation_form):
        assert job_seeker_creation_form.is_valid()
        user = job_seeker_creation_form.save()
        assert isinstance(user.job_seeker, js_models.JobSeeker)
        assert user.username == constants.BASE_VALID_CREDENTIALS['username']
