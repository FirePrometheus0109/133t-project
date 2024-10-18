# pylint: disable=no-member
from django.db import models as orm
from django.db.models import functions

from leet import enums


def annotate_jobs_with_matching_percent(job_seeker, jobs_qs):
    js_skills = job_seeker.skills.all()
    matched_skills_count = orm.Count(
        orm.Case(
            orm.When(
                orm.Q(job_skill_set__skill__in=js_skills)
                & orm.Q(job_skill_set__is_required=True),
                then=1),
            output_field=orm.IntegerField())
    )
    all_req_skills_count = orm.Count(
        orm.Case(
            orm.When(job_skill_set__is_required=True, then=1),
            output_field=orm.IntegerField())
    )
    percents_calc = (functions.Cast(matched_skills_count, orm.FloatField()) /
                     functions.Cast('skills_count', orm.FloatField()) * 100)
    percents = orm.Case(orm.When(skills_count__gt=0, then=percents_calc),
                        default=100.0)

    jobs = jobs_qs.annotate(
        skills_count=all_req_skills_count,
        matching_percent=percents
    )
    return jobs


def is_user_candidate_for_company(job_seeker, company):
    applies = job_seeker.applies.filter(
        job__company=company,
        status=enums.ApplyStatusEnum.APPLIED.name
    )
    return applies.exists()


def is_job_seeker_purchased(job_seeker, company):
    return company.purchased_job_seekers.filter(id=job_seeker.id).exists()


def get_inactive_job_representation(job):
    return {
        'id': job.id,
        'title': job.title,
        'is_deleted': True,
        'company': {
            'id': job.company_id,
            'name': job.company.name,
        }
    }


def is_job_active(job):
    return job.status == enums.JobStatusEnum.ACTIVE.name


def get_ban_status_active_entities(entities):
    return entities.filter(ban_status=enums.BanStatusEnum.ACTIVE.name)


def ban_entities(entities):
    return entities.update(ban_status=enums.BanStatusEnum.BANNED.name)


def unban_entities(entities):
    return entities.update(ban_status=enums.BanStatusEnum.ACTIVE.name)
