# pylint: disable=no-member
import uuid

from django.contrib.postgres import indexes
from django.contrib.postgres import search
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from job import search_vectors
from leet import enums, models as base_models


class Industry(models.Model):
    name = models.CharField(
        'name',
        max_length=256,
        unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Industries'


class Skill(base_models.BaseModel):
    name = models.CharField(
        'name',
        max_length=256,
        unique=True
    )
    description = models.TextField(
        'description',
        blank=True,
        null=True
    )
    type = models.CharField(
        'type',
        max_length=256,
        null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class JobManager(base_models.BaseManager):

    def get_all_with_relations(self):
        return (self
                .prefetch_related(
                    'job_skill_set',
                    'job_skill_set__skill',
                    'savedjob_set',
                    'savedjob_set__job_seeker',
                    'views',
                    'applies',
                    'applies__owner',
                    'questions',
                    'candidates')
                .select_related(
                    'company',
                    'owner__user',
                    'industry',
                    'location',
                    'location__city',
                    'location__city__state',
                    'location__zip',
                    'location__country')
                .annotate(
                    rank=models.Value(0, output_field=models.FloatField()))
                .annotate(
                    loca_rank=models.Value(0, output_field=models.FloatField())
                ))

    def get_published(self):
        """Return all jobs with status active and ban status active."""
        return (self
                .get_all_with_relations()
                .filter(
                    status=enums.JobStatusEnum.ACTIVE.name,
                    ban_status=enums.BanStatusEnum.ACTIVE.name,
                    is_deleted=False))

    def with_documents(self):
        return self.get_queryset().annotate(
            document=search_vectors.SEARCH_VECTOR,
            location_document=search_vectors.LOCATION_SEARCH_VECTOR
        )


class Job(base_models.BaseModel, base_models.BanStatusModel):
    company = models.ForeignKey(
        to='company.Company',
        on_delete=models.CASCADE,
        related_name='jobs',
        related_query_name='job'
    )
    title = models.CharField(
        'title',
        max_length=255
    )
    description = models.TextField(
        'description',
        max_length=1024,
    )
    location = models.OneToOneField(
        to='geo.Address',
        on_delete=models.PROTECT,
    )
    industry = models.ForeignKey(
        to=Industry,
        on_delete=models.PROTECT
    )
    position_type = models.CharField(
        'position_type',
        max_length=40,
        choices=enums.PositionTypesEnum.choices
    )
    education = models.CharField(
        'education',
        max_length=40,
        blank=True,
        default=enums.EducationTypesEnum.NO_EDUCATION.name,
        choices=enums.EducationTypesEnum.choices
    )
    clearance = models.IntegerField(
        'clearance',
        default=enums.ClearanceTypesEnum.NO_CLEARANCE.name,
        choices=enums.ClearanceTypesEnum.choices
    )
    experience = models.CharField(
        'experience',
        max_length=40,
        default=enums.ExperienceEnum.NO_EXPERIENCE.name,
        choices=enums.ExperienceEnum.choices
    )
    salary_min = models.PositiveIntegerField(
        'salary_min',
        null=True,
        blank=True
    )
    salary_max = models.PositiveIntegerField(
        'salary_max',
        null=True,
        blank=True
    )
    salary_negotiable = models.BooleanField(
        'salary_negotiable',
        default=False
    )
    benefits = models.CharField(
        'benefits',
        max_length=40,
        default=enums.BenefitsEnum.NO_BENEFITS.name,
        choices=enums.BenefitsEnum.choices
    )
    travel = models.CharField(
        'travel',
        max_length=40,
        default=enums.TravelOpportunitiesEnum.NO_TRAVEL.name,
        choices=enums.TravelOpportunitiesEnum.choices
    )
    status = models.CharField(
        'status',
        max_length=16,
        choices=enums.JobStatusEnum.choices,
        default=enums.JobStatusEnum.DRAFT.name
    )
    education_strict = models.BooleanField(
        'education_strict',
        default=False
    )
    publish_date = models.DateTimeField(
        'publish_date',
        null=True,
        blank=True
    )
    owner = models.ForeignKey(
        'company.CompanyUser',
        on_delete=models.CASCADE,
        related_name='jobs',
    )
    is_deleted = models.BooleanField(
        default=False
    )
    deleted_at = models.DateTimeField(
        null=True,
        blank=True
    )
    is_cover_letter_required = models.BooleanField(default=False)
    closing_date = models.DateTimeField(
        null=True,
        blank=True
    )
    guid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )
    autoapply_minimal_percent = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(100), MinValueValidator(0)], default=100
    )
    manual_apply_strict_required_skills_matching = models.BooleanField(default=False)
    search_vector = search.SearchVectorField(null=True)
    location_search_vector = search.SearchVectorField(null=True)

    objects = JobManager()

    class Meta:
        indexes = [
            indexes.GinIndex(fields=['search_vector']),
            indexes.GinIndex(fields=['location_search_vector'])
        ]

    @property
    def all_skills(self):
        """Return list of all job's skills"""
        return self.job_skill_set.all()

    @property
    def required_skills(self):
        """Return list of required job's skills"""
        return [jp_s.skill for jp_s in self.all_skills if jp_s.is_required]

    @property
    def optional_skills(self):
        """Return list of optional job's skills"""
        return [jp_s.skill for jp_s in self.all_skills if not jp_s.is_required]

    def save(self, *args, **kwargs):  # noqa
        super().save(*args, **kwargs)
        if ('update_fields' not in kwargs
                or 'search_vector' not in kwargs['update_fields']
                or 'location_search_vector' not in kwargs['update_fields']):
            try:
                instance = self._meta.default_manager.with_documents().get(
                    pk=self.pk)
            except self.DoesNotExist:
                # objects is inactive
                pass
            else:
                instance.search_vector = instance.document
                instance.location_search_vector = instance.location_document
                instance.save(update_fields=[
                    'search_vector', 'location_search_vector'])

    def __str__(self):
        return self.title


class JobSkill(models.Model):
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='job_skill_set'
    )
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE
    )
    is_required = models.BooleanField(
        'is_required',
        default=False
    )

    def __str__(self):
        return self.skill.name

    class Meta:
        unique_together = (('job', 'skill'),)


class ViewJob(base_models.BaseModel):
    owner = models.ForeignKey(
        'job_seeker.JobSeeker',
        on_delete=models.CASCADE
    )
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='views'
    )


class JobSearch(base_models.BaseModel):
    owner = models.ForeignKey(
        'job_seeker.JobSeeker',
        on_delete=models.CASCADE,
        related_name='searches'
    )
    criteria = models.TextField()
    is_saved = models.BooleanField(default=False)
    count = models.PositiveIntegerField(default=1)
