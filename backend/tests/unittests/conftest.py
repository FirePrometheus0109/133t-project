import pytest
from allauth.account.models import EmailAddress
from django.utils import timezone
from faker import Faker

from apply.models import Autoapply
from geo.models import Address
from job.models import Job, Skill, Industry
from job_seeker.models import JobSeeker, CoverLetter
from leet import enums
from notification_center import models as notif_models
from tests import utils

fake = Faker()


@pytest.fixture
def base_user(django_user_model):
    user = django_user_model(
        username=utils.get_unique_username(),
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=utils.get_unique_user_email()
    )
    user.set_password('JSPassword1')
    user.save()
    EmailAddress.objects.create(user=user, email=user.email,
                                verified=True, primary=True)
    return user


@pytest.fixture
def job_seeker(base_user, outlook_skill, mysql_skill):
    job_seeker = JobSeeker.objects.create(
        user=base_user,
        position_type=enums.PositionTypesEnum.FULL_TIME.name,
        education=enums.EducationTypesEnum.BACHELORS_DEGREE.name,
        clearance=enums.ClearanceTypesEnum.TOP_SECRET.name,
    )
    skills = [outlook_skill, mysql_skill]
    job_seeker.skills.add(*skills)
    notif_types = notif_models.NotificationType.objects.all()
    job_seeker.user.subscribed_notifications.add(*notif_types)
    return job_seeker


@pytest.fixture
def job(company, country_usa, city_ashville, company_user):
    location = Address.objects.create(country=country_usa, city=city_ashville)
    job = Job.objects.create(
        company=company,
        title='Architect',
        description=fake.text(),
        location=location,
        industry=Industry.objects.get_or_create(name='Architecture')[0],
        position_type=enums.PositionTypesEnum.FULL_TIME.name,
        education=enums.EducationTypesEnum.BACHELORS_DEGREE.name,
        clearance=enums.ClearanceTypesEnum.TOP_SECRET.name,
        status=enums.JobStatusEnum.ACTIVE.name,
        owner=company_user,
        autoapply_minimal_percent=50
    )
    return job


@pytest.fixture
def autoapply(job_seeker, city_ashville):
    autoapply = Autoapply.objects.create(
        title='My autoapply',
        status=enums.AutoapplyStatusEnum.SAVED.name,
        owner=job_seeker,
        number=1,
        query_params='title=Arch&city_id={}'.format(city_ashville.id)
    )
    return autoapply


@pytest.fixture
def finished_autoapply(autoapply):
    autoapply.status = enums.AutoapplyStatusEnum.FINISHED.name
    autoapply.finished_at = timezone.now()
    autoapply.save()
    return autoapply


@pytest.fixture
def cover_letter(job_seeker):
    cover_letter = CoverLetter.objects.create(
        title='title',
        body='body',
        is_default=True,
        owner=job_seeker
    )
    return cover_letter
