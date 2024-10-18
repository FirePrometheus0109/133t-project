import random

import pytz
from allauth.account.models import EmailAddress
from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker
from faker.providers import BaseProvider

from company.models import Company, CompanyUser
from company import utils as company_utils
from geo.models import Address, Country, State, City, Zip
from job.models import Industry, Job, JobSkill, Skill
from job_seeker.models import JobSeeker
from leet import enums
from notification_center import models as notif_models
from permission import utils

fake = Faker()

DEFAULT_ADMIN_USERNAME = 'admin'
DEFAULT_ADMIN_PASSWORD = 'admin'  # noqa
DEFAULT_USER_PASSWORD = '1Password123'  # noqa
DEFAULT_JS_USERNAME_TMPL = 'jobseeker{}'
DEFAULT_COMPANY_TMPL = 'company{}'
DEFAULT_EMAIL_DOMAIN = 'itransition.com'


class LeetBaseProvider(BaseProvider):
    def leet_country(self):
        return random.choice([x for x in Country.objects.all()])

    def leet_state(self, country_id):
        return random.choice([x for x in State.objects.filter(country__id=country_id)])

    def leet_city(self, state_id):
        return random.choice([x for x in City.objects.filter(state__id=state_id)])

    def leet_zip(self, city_id):
        return random.choice([x for x in Zip.objects.filter(city_id=city_id)])

    def leet_position_type(self):
        return random.choice([x for x in enums.PositionTypesEnum.to_dict().keys()])

    def leet_education(self):
        return random.choice([x for x in enums.EducationTypesEnum.to_dict().keys()])

    def leet_clearance(self):
        return random.choice([x for x in enums.ClearanceTypesEnum.to_dict().keys()])

    def leet_experience(self):
        return random.choice([x for x in enums.ExperienceEnum.to_dict().keys()])

    def leet_salary_min(self):
        return random.randint(100, 1000)

    def leet_salary_max(self):
        return random.randint(1000, 3000)

    def leet_benefits(self):
        return random.choice([x for x in enums.BenefitsEnum.to_dict().keys()])

    def leet_js_travel(self):
        return random.choice([x for x in enums.JSTravelOpportunitiesEnum.to_dict().keys()])

    def leet_job_travel(self):
        return random.choice([x for x in enums.TravelOpportunitiesEnum.to_dict().keys()])

    def leet_skills(self):
        skills = []
        for i in range(random.randint(2, 10)):
            skill = random.choice([x.id for x in Skill.objects.all()])
            if skill not in skills:
                skills += [skill]
        return skills

    def leet_industry(self):
        return random.choice([x for x in Industry.objects.all()])


fake.add_provider(LeetBaseProvider)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--job-seeker-count',
            type=int,
            dest='job_seeker_count',
            default=10,
            help='Count of Job Seeker need to be created',
        )
        parser.add_argument(
            '--company-count',
            type=int,
            dest='company_count',
            default=10,
            help='Count of Company need to be created',
        )
        parser.add_argument(
            '--job-per-company',
            type=int,
            dest='job_per_company',
            default=10,
            help='Count of Jobs per Company need to be created',
        )

    def handle(self, *args, **options):
        self.create_admin()
        for i in range(options['job_seeker_count']):
            self.create_job_seeker(i)

        for i in range(options['company_count']):
            company, company_user = self.create_company(i)
            for j in range(options['job_per_company']):
                self.create_job(company, company_user, j)

    def create_admin(self):
        User.objects.create_superuser(
            DEFAULT_ADMIN_USERNAME,
            '{}@{}'.format(DEFAULT_ADMIN_USERNAME, DEFAULT_EMAIL_DOMAIN),
            DEFAULT_ADMIN_PASSWORD
        )

    def create_job_seeker(self, counter):
        with transaction.atomic():
            username = DEFAULT_JS_USERNAME_TMPL.format(counter)
            email = '{}@{}'.format(username, DEFAULT_EMAIL_DOMAIN)
            password = DEFAULT_USER_PASSWORD
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=fake.first_name(),
                last_name=fake.last_name()
            )
            EmailAddress.objects.create(
                user=user,
                email=email,
                verified=True,
                primary=True
            )
            country = fake.leet_country()
            state = fake.leet_state(country.id)
            city = fake.leet_city(state.id)
            address = Address.objects.create(**{
                'address': fake.street_address(),
                'country': country,
                'city': fake.leet_city(state.id),
                'zip': fake.leet_zip(city.id),
            })
            js_data = {
                'user': user,
                'address': address,
                'about': fake.text(),
                'phone': fake.phone_number(),
                # 'photo': photo,
                'position_type': fake.leet_position_type(),
                'education': fake.leet_education(),
                'clearance': fake.leet_clearance(),
                'experience': fake.leet_experience(),
                'salary_min': fake.leet_salary_min(),
                'salary_max': fake.leet_salary_max(),
                'salary_public': fake.boolean(),
                'benefits': fake.leet_benefits(),
                'travel': fake.leet_js_travel(),
                # 'skills': [],
                'is_public': True
            }
            job_seeker = JobSeeker.objects.create(**js_data)
            skills = fake.leet_skills()
            job_seeker.skills.add(*skills)
            job_seeker.save()
            job_seeker_group = Group.objects.get_by_natural_key('job_seeker')
            job_seeker.user.groups.add(job_seeker_group)
            notif_types = notif_models.NotificationType.objects.filter(
                groups__id=job_seeker_group.id)
            job_seeker.user.subscribed_notifications.add(*notif_types)
            self.stdout.write(self.style.SUCCESS('Created Job Seeker "%s"' % job_seeker))
            return job_seeker

    def create_company(self, counter):
        with transaction.atomic():
            username = DEFAULT_COMPANY_TMPL.format(counter)
            email = '{}@{}'.format(username, DEFAULT_EMAIL_DOMAIN)
            password = DEFAULT_USER_PASSWORD
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=fake.first_name(),
                last_name=fake.last_name()
            )
            EmailAddress.objects.create(
                user=user,
                email=email,
                verified=True,
                primary=True
            )
            country = fake.leet_country()
            state = fake.leet_state(country.id)
            city = fake.leet_city(state.id)
            address = Address.objects.create(**{
                'address': fake.street_address(),
                'country': country,
                'city': fake.leet_city(state.id),
                'zip': fake.leet_zip(city.id),
            })
            company_data = {
                'name': fake.company(),
                'description': fake.text(),
                'address': address,
                'phone': fake.phone_number(),
                'fax': fake.phone_number(),
                'website': fake.url(),
                'email': fake.email(),
            }
            company = Company.objects.create(**company_data)
            company_user = CompanyUser.objects.create(
                user=user,
                company=company,
                status=enums.CompanyUserStatusEnum.ACTIVE.name,
            )
            company_utils.set_viewed_candidates_statuses(company_user)
            company_user_group = Group.objects.get_by_natural_key(
                'company_user')
            company_user.user.groups.add(company_user_group)
            utils.add_permission_initial_company_user(
                company_user.user
            )
            notif_types = notif_models.NotificationType.objects.filter(
                groups__id=company_user_group.id)
            company_user.user.subscribed_notifications.add(*notif_types)
            self.stdout.write(self.style.SUCCESS('Created Company "%s"' % company))
            return company, company_user

    def create_job(self, company, company_user, counter):
        with transaction.atomic():
            country = fake.leet_country()
            state = fake.leet_state(country.id)
            city = fake.leet_city(state.id)
            zip = fake.leet_zip(city.id)
            location = Address.objects.create(**{
                'country': country,
                'city': city,
                'zip': zip,
            })
            industry = fake.leet_industry()
            job_data = {
                'company': company,
                'title': fake.job(),
                'description': fake.text(),
                'location': location,
                'industry': industry,
                'position_type': fake.leet_position_type(),
                'education': fake.leet_education(),
                'clearance': fake.leet_clearance(),
                'experience': fake.leet_experience(),
                'salary_min': fake.leet_salary_min(),
                'salary_max': fake.leet_salary_max(),
                'salary_negotiable': fake.boolean(),
                'benefits': fake.leet_benefits(),
                'travel': fake.leet_job_travel(),
                'status': enums.JobStatusEnum.ACTIVE.name,
                'education_strict': fake.boolean(),
                'publish_date': fake.past_datetime().astimezone(pytz.timezone('UTC')),
                'owner': company_user,
            }
            job = Job.objects.create(**job_data)
            required_skills = fake.leet_skills()
            for skill in required_skills:
                JobSkill.objects.create(
                    job=job,
                    skill=Skill.objects.get(pk=skill),
                    is_required=True
                )
            optional_skills = list(set(fake.leet_skills()) - set(required_skills))
            for skill in optional_skills:
                JobSkill.objects.create(
                    job=job,
                    skill=Skill.objects.get(pk=skill),
                    is_required=False
                )
            job.save()
            self.stdout.write(self.style.SUCCESS('Created Job "%s"' % job))
            return job
