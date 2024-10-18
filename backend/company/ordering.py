# pylint: disable=no-member
from django.db import models as orm

from leet import enums

COMPANY_USERS_LIST_ORDERING = orm.Case(
    orm.When(
        orm.Q(status=enums.CompanyUserStatusEnum.NEW.name),
        then=0),
    orm.When(
        orm.Q(status=enums.CompanyUserStatusEnum.ACTIVE.name),
        then=1),
    orm.When(
        orm.Q(status=enums.CompanyUserStatusEnum.DISABLED.name),
        then=2),
    default=3,
    output_field=orm.IntegerField())
