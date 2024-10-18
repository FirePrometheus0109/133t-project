import csv
import datetime
import functools
import http
import io
import operator
import random
import re

import pytest
from allauth.account import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from faker import Faker

from company import models as company_models
from geo.models import Country, City
from job.models import Industry, Skill
from leet import enums
from leet import enums as base_enums
from tests import api_requests
from tests import constants

fake = Faker()
User = get_user_model()

pytestmark = pytest.mark.django_db


def get_unique_company_email():
    return '{}{}'.format(
        company_models.Company.objects.count(),
        constants.DEFAULT_EMAIL
    )


def get_unique_username():
    return '{}{}'.format(
        User.objects.count(),
        constants.DEFAULT_USERNAME
    )


def get_unique_user_email():
    return '{}{}'.format(
        User.objects.count(),
        constants.DEFAULT_EMAIL
    )


def get_random_database_object(manager):
    count = manager.count()
    random_index = random.randint(0, count - 1)
    return manager.all()[random_index]


def get_random_database_objects_set(manager, count=None):
    objects_count = manager.count()
    count = count or random.randint(1, objects_count)
    return random.sample(list(manager.all()), k=count)


def generate_random_company_info(**kwargs):
    country = get_random_database_object(Country.objects)
    city = get_random_database_object(City.objects.filter(state__country=country))
    zip = get_random_database_object(city.zips)
    industry = get_random_database_object(Industry.objects)
    company_info = {
        'name': fake.company(),
        'description': fake.text(),
        'phone': fake.phone_number(),
        'fax': fake.msisdn(),
        'website': fake.url(),
        'email': get_unique_company_email(),
        'address': {
            'country': country.id,
            'address': fake.address(),
            'city': city.id,
            'zip': zip.id
        },
        'industry': industry.id,
    }
    company_info.update(**kwargs)
    return company_info


def generate_random_job_info(**kwargs):
    industry = get_random_database_object(Industry.objects)
    country = get_random_database_object(Country.objects)
    city = get_random_database_object(City.objects.filter(state__country=country))
    required_skill_ids = get_random_database_objects_set(Skill.objects)
    optional_skill_ids = set(get_random_database_objects_set(Skill.objects)) - set(required_skill_ids)
    job_info = {
        'title': fake.word(),
        'description': fake.text(),
        'location': {'city': city.id, 'country': country.id},
        'industry': industry.id,
        'position_type': random.choice(list(enums.PositionTypesEnum)).name,
        'education': random.choice(list(enums.EducationTypesEnum)).name,
        'salary_negotiable': False,
        'salary_min': 200,
        'salary_max': 400,
        'clearance': random.choice(list(enums.ClearanceTypesEnum)).name,
        'experience': random.choice(list(enums.ExperienceEnum)).name,
        'benefits': random.choice(list(enums.BenefitsEnum)).name,
        'travel': random.choice(list(enums.TravelOpportunitiesEnum)).name,
        'required_skills': [skill.id for skill in required_skill_ids],
        'optional_skills': [skill.id for skill in optional_skill_ids]
    }
    job_info.update(**kwargs)
    return job_info


def generate_random_job_seeker_info(**kwargs):
    skills = get_random_database_object(Skill.objects)
    job_seeker_info = {
        'position_type': random.choice(list(enums.PositionTypesEnum)).name,
        'education': random.choice(list(enums.EducationTypesEnum)).name,
        'salary_public': True,
        'salary_min': 200,
        'salary_max': 400,
        'clearance': random.choice(list(enums.ClearanceTypesEnum)).name,
        'experience': random.choice(list(enums.ExperienceEnum)).name,
        'benefits': random.choice(list(enums.BenefitsEnum)).name,
        'travel': random.choice(list(enums.TravelOpportunitiesEnum)).name,
        'skills': [skill.id for skill in skills],
        'phone': '+375297777777'
    }
    job_seeker_info.update(**kwargs)
    return job_seeker_info


def verify_email(user):
    email_address = models.EmailAddress.objects.get(user=user)
    email_address.verified = True
    email_address.save()


def date(year, month, day):
    tz = timezone.get_current_timezone()
    return datetime.datetime(year, month, day, tzinfo=tz)


def get_from_dict(data_dict, map_list):
    """
    Get deep value from dict
    # https://stackoverflow.com/questions/14692690/access-nested-dictionary-items-via-a-list-of-keys
    """
    try:
        return functools.reduce(operator.getitem, map_list, data_dict)
    except TypeError:
        return None


def Any(cls):
    class Inner(cls):

        def __eq__(self, other):
            return isinstance(other, cls)

    return Inner()


def AnyOrNone(cls):
    class Inner(cls):

        def __eq__(self, other):
            return isinstance(other, cls) or other is None

    return Inner()


def find_account_link_in_email(email):
    message = email.body
    search = re.search('<a href="(.+)">', message)
    link = search.group(1)
    token = link.split('/')[-1]
    user_id = link.split('/')[-2]
    return token, user_id


def ban_entity(obj):
    if hasattr(obj, 'ban_status'):
        obj.ban_status = base_enums.BanStatusEnum.BANNED.name
        obj.save()


def get_csv_response_data(resp):
    content = resp.content.decode('utf-8')
    cvs_reader = csv.reader(io.StringIO(content))
    body = list(cvs_reader)
    return body.pop(0), body


def get_candidate_by_job_seeker_id(candidates, job_seeker_id):
    return next(i for i in candidates
                if i['job_seeker']['id'] == job_seeker_id)


def create_candidate(client, job, job_seeker):
    data = {
        'jobs': [job['id']],
        'job_seekers': [job_seeker.id]
    }
    resp = api_requests.assign_candidate_to_job(client, data)
    assert resp.status_code == http.HTTPStatus.CREATED
    resp = api_requests.get_candidates(client)
    assert resp.status_code == http.HTTPStatus.OK
    return get_candidate_by_job_seeker_id(
        resp.json()['results'], job_seeker.id)
