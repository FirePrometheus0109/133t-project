from django.db import models as orm


USER_LIST_ORDERING = orm.Case(
    orm.When(
        orm.Q(company_user__isnull=True) & orm.Q(job_seeker__isnull=True),
        then=0),
    orm.When(
        company_user__isnull=False,
        then=1),
    orm.When(
        job_seeker__isnull=False,
        then=2),
    default=3,
    output_field=orm.IntegerField())
