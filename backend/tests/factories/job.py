from geo.models import Address, Country, City
from job.models import Job, Industry
from tests.utils import generate_random_job_info
from tests.utils import get_random_database_object


def create_job(company, **kwargs):
    industry = get_random_database_object(Industry.objects)
    country = get_random_database_object(Country.objects)
    city = get_random_database_object(
        City.objects.filter(state__country=country)
    )
    location = Address.objects.create(country=country, city=city)
    job_info = generate_random_job_info(
        industry=industry, location=location)
    job_info.update(**kwargs)
    job_info.pop('required_skills')
    job_info.pop('optional_skills')
    job = Job.objects.create(company=company, **job_info)
    return job
