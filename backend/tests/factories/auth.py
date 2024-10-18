from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils.crypto import get_random_string
from faker import Faker

from company.models import Company, CompanyUser
from job_seeker.models import JobSeeker
from leet import enums
from permission.utils import add_permission_initial_company_user
from tests import utils
from tests.factories.address import create_address

User = get_user_model()
fake = Faker()


def create_base_user(**kwargs):
    """Create base user without roles and companies"""
    password = kwargs.pop('password', get_random_string())
    data = {
        'username': utils.get_unique_username(),
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'email': utils.get_unique_user_email(),
    }
    data.update(kwargs)
    user = User(**data)
    user.set_password(password)
    user.save()
    EmailAddress.objects.create(user=user, email=user.email,
                                verified=True, primary=True)
    return user


def create_job_seeker(**kwargs):
    """Create job seeker"""
    user = kwargs.pop('user', None) or create_base_user()
    address = kwargs.pop('address', None) or create_address()
    skills = kwargs.pop('skills', None)
    industries = kwargs.pop('industries', None)
    group = Group.objects.get_by_natural_key(
        enums.AuthGroupsEnum.JOB_SEEKER.value)
    group.user_set.add(user)
    job_seeker = JobSeeker.objects.create(
        user=user, address=address, **kwargs
    )
    if skills is not None:
        job_seeker.skills.add(*skills)
    if industries is not None:
        job_seeker.industries.add(*industries)
    return job_seeker


def create_company_user(**kwargs):
    """Create company user"""

    user = kwargs.pop('user', None) or create_base_user()
    group = Group.objects.get_by_natural_key(
        enums.AuthGroupsEnum.COMPANY_USER.value)
    group.user_set.add(user)
    user = add_permission_initial_company_user(user)
    company = kwargs.pop('company', None) or Company.objects.create(
        name=fake.company()
    )
    user.company_user = CompanyUser.objects.create(
        company=company,
        user=user,
        status=kwargs.get('status') or enums.CompanyUserStatusEnum.ACTIVE.name
    )
    user.save()
    return user.company_user


def verify_email(user):
    email_address = EmailAddress.objects.get(user=user)
    email_address.verified = True
    email_address.save()
