from django.db import models
from versatileimagefield.fields import VersatileImageField

from leet import enums
from leet import models as base_models
from leet import utils


class CompanyManager(models.Manager):
    """Allows to retrieve only Companies with valid profile"""

    def not_draft(self):
        return self.filter(address__isnull=False, phone__isnull=False)


class Company(base_models.BaseModel, base_models.BanStatusModel):
    name = models.CharField(
        'name',
        max_length=255
    )
    photo = VersatileImageField(
        'photo',
        upload_to=utils.get_photo_path,
        null=True,
        blank=True
    )
    industry = models.ForeignKey(
        to='job.Industry',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    description = models.CharField(
        'description',
        max_length=4000,
        blank=True
    )
    address = models.OneToOneField(
        'geo.Address',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    phone = models.CharField(
        'phone',
        max_length=32,
        blank=True,
        null=True
    )
    fax = models.CharField(
        'fax',
        max_length=32,
        blank=True,
        null=True
    )
    website = models.CharField(
        'website',
        max_length=255,
        blank=True,
        null=True
    )
    # NOTE (i.bogretsov) email is not unique
    email = models.CharField(
        'email',
        max_length=255,
        blank=True
    )
    purchased_job_seekers = models.ManyToManyField(
        'job_seeker.JobSeeker'
    )
    is_trial_available = models.BooleanField(
        'is_trial_available',
        default=True
    )

    class Meta:
        verbose_name_plural = 'Companies'

    @property
    def is_profile_filled(self):
        map_lists = (
            ['name'],
            ['phone'],
            ['address', 'address'],
            ['address', 'county'],
            ['address', 'city'],
            ['address', 'zip']
        )
        for i in map_lists:
            if not utils.get_from_nested_structure(self, i, func=getattr):
                return False
        return True

    def __str__(self):
        return self.name


class CompanyUser(base_models.BaseModel, base_models.BanStatusModel):
    user = models.OneToOneField(
        'leet_auth.ProxyUser',
        on_delete=models.CASCADE,
        related_name='company_user'
    )
    company = models.ForeignKey(
        'company.Company',
        on_delete=models.CASCADE,
        related_name='company_users',
        related_query_name='company_user',
    )
    status = models.CharField(
        'status',
        max_length=16,
        choices=enums.CompanyUserStatusEnum.choices,
        default=enums.CompanyUserStatusEnum.NEW.name  # noqa
    )
    is_disabled_by_subscription = models.BooleanField(
        default=False
    )
    candidate_statuses = models.ManyToManyField(
        'leet.CandidateStatus'
    )

    def __str__(self):
        return self.user.get_full_name()  # noqa


class CompanyActivityReport(Company):
    class Meta:
        proxy = True


class CompanyRegistrationReport(Company):
    class Meta:
        proxy = True


class CompanyTransactionsReport(Company):
    class Meta:
        proxy = True
