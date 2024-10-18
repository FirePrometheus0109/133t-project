# pylint: disable=no-member
import uuid

from django.contrib.postgres import indexes
from django.contrib.postgres import search
from django.db import models
from versatileimagefield.fields import VersatileImageField

from job_seeker import search_vectors
from leet import enums
from leet import models as base_models
from leet import utils


class JobSeekerProfileManager(models.Manager):

    def get_all_with_relations(self):
        """
        Return queryset with all relations.
        Annotated 'rank' field is used in full text search.
        We annotated this field explicitly.
        """
        return (self
                .select_related(
                    'user',
                    'address')
                .prefetch_related(
                    'job_experience',
                    'skills',
                    'educations',
                    'certifications',
                    'documents',
                    'saved_jobs',
                    'cover_letters',
                    'address__zip',
                    'address__country',
                    'address__city',
                    'address__city__state',
                    'savedjobseeker_set',
                    'industries')
                .annotate(
                    rank=models.Value(0, output_field=models.FloatField())
                ))

    def with_documents(self):
        return self.get_queryset().annotate(
            document=search_vectors.SEARCH_VECTOR,
            location_document=search_vectors.LOCATION_SEARCH_VECTOR
        )


class JobSeeker(base_models.BaseModel, base_models.BanStatusModel):
    """Extended User model to keep custom fields"""

    user = models.OneToOneField(
        'leet_auth.ProxyUser',
        on_delete=models.CASCADE,
        related_name='job_seeker',
        verbose_name="User")
    about = models.TextField(
        'about',
        max_length=2000,
        blank=True,
        null=True
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
    photo = VersatileImageField(
        'photo',
        upload_to=utils.get_photo_path,
        blank=True,
        null=True
    )
    position_type = models.CharField(
        'position_type',
        max_length=40,
        blank=True,
        null=True,
        choices=enums.PositionTypesEnum.choices
    )
    education = models.CharField(
        'education',
        max_length=40,
        blank=True,
        null=True,
        choices=enums.EducationTypesEnum.choices
    )
    clearance = models.IntegerField(
        'clearance',
        blank=True,
        null=True,
        choices=enums.ClearanceTypesEnum.choices,
        default=0
    )
    experience = models.CharField(
        'experience',
        max_length=40,
        blank=True,
        null=True,
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
    salary_public = models.BooleanField(
        'salary_public',
        default=False
    )
    benefits = models.CharField(
        'benefits',
        max_length=40,
        blank=True,
        null=True,
        choices=enums.BenefitsEnum.choices
    )
    travel = models.CharField(
        'travel',
        max_length=40,
        blank=True,
        null=True,
        choices=enums.JSTravelOpportunitiesEnum.choices
    )
    skills = models.ManyToManyField(
        'job.Skill',
        blank=True
    )
    is_public = models.BooleanField(
        'is_public',
        default=False
    )
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(
        null=True,
        blank=True
    )
    industries = models.ManyToManyField(
        'job.Industry',
        blank=True
    )
    is_shared = models.BooleanField(default=False)
    # Leave this for now as this attribute can be used only for job seeker.
    # Can be False only in case of signup with social media
    is_password_set = models.BooleanField(default=True)
    guid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )
    search_vector = search.SearchVectorField(null=True)
    location_search_vector = search.SearchVectorField(null=True)

    objects = JobSeekerProfileManager()

    class Meta:
        indexes = [
            indexes.GinIndex(fields=['search_vector']),
            indexes.GinIndex(fields=['location_search_vector'])
        ]

    def save(self, *args, **kwargs):  # noqa
        super().save(*args, **kwargs)
        if ('update_fields' not in kwargs
                or 'search_vector' not in kwargs['update_fields']
                or 'location_search_vector' not in kwargs['update_fields']):
            try:
                instance = self._meta.default_manager.with_documents().get(
                    pk=self.pk)
            except self.DoesNotExist:
                # object is inactive
                pass
            else:
                instance.search_vector = instance.document
                instance.location_search_vector = instance.location_document
                instance.save(update_fields=[
                    'search_vector', 'location_search_vector'])

    def __str__(self):
        return self.user.get_full_name()


class JobExperience(base_models.BaseModel):

    owner = models.ForeignKey(
        JobSeeker,
        on_delete=models.CASCADE,
        related_name='job_experience',
    )
    company = models.CharField(
        'company',
        max_length=256
    )
    job_title = models.CharField(
        'job_title',
        max_length=256
    )
    date_from = models.DateTimeField()
    date_to = models.DateTimeField(
        blank=True,
        null=True
    )
    description = models.TextField(
        'description',
        max_length=4000,
        blank=True,
        null=True
    )
    is_current = models.BooleanField(
        default=False
    )
    employment = models.CharField(
        'employment',
        max_length=16,
        choices=enums.EmploymentEnum.choices,
        blank=True,
        null=True
    )


class Document(base_models.BaseModel):
    owner = models.ForeignKey(
        JobSeeker,
        on_delete=models.CASCADE,
        related_name='documents'
    )
    file = models.FileField()
    name = models.CharField(max_length=100)
    extension = models.CharField(max_length=5)


class EducationBaseAbstract(base_models.BaseModel):
    """Base Education abstract model for job seeker education.
    Education can be Certification"""

    institution = models.CharField(
        'institution',
        max_length=256
    )
    field_of_study = models.CharField(
        'field_of_study',
        max_length=256,
    )
    location = models.CharField(
        'location',
        max_length=256,
        blank=True,
        null=True
    )
    description = models.TextField(
        'description',
        blank=True,
        null=True
    )
    is_current = models.BooleanField(
        'is_current',
        default=False
    )

    class Meta:
        abstract = True


class Education(EducationBaseAbstract):

    owner = models.ForeignKey(
        JobSeeker,
        on_delete=models.CASCADE,
        related_name='educations',
    )
    degree = models.CharField(
        'education',
        max_length=40,
        blank=True,
        choices=[
            (e.name, e.value) for e in enums.EducationTypesEnum
            if e != enums.EducationTypesEnum.CERTIFICATION
        ],
        null=True
    )
    date_from = models.DateTimeField(
        'date_from'
    )
    date_to = models.DateTimeField(
        'date_to',
        blank=True,
        null=True
    )


class Certification(EducationBaseAbstract):

    owner = models.ForeignKey(
        JobSeeker,
        on_delete=models.CASCADE,
        related_name='certifications',
    )
    graduated = models.DateTimeField(
        'graduated',
        blank=True,
        null=True
    )
    licence_number = models.CharField(
        'licence_number',
        max_length=100,
        blank=True,
        null=True
    )


class SavedJob(base_models.BaseModel):

    job = models.ForeignKey(
        'job.Job',
        on_delete=models.CASCADE,
        related_name='savedjob_set'
    )
    job_seeker = models.ForeignKey(
        JobSeeker,
        on_delete=models.CASCADE,
        related_name='saved_jobs'
    )

    class Meta:
        unique_together = ('job', 'job_seeker')


class CoverLetter(base_models.BaseModel):

    title = models.CharField(
        max_length=256
    )
    body = models.TextField()
    is_default = models.BooleanField(default=False)
    owner = models.ForeignKey(
        JobSeeker,
        on_delete=models.CASCADE,
        related_name='cover_letters'
    )

    class Meta:
        unique_together = ('owner', 'title')


class ViewJobSeeker(base_models.BaseModel):

    job_seeker = models.ForeignKey(
        'JobSeeker',
        on_delete=models.CASCADE,
    )
    company_user = models.ForeignKey(
        'company.CompanyUser',
        on_delete=models.CASCADE,
        related_name='viewed_job_seekers',
    )


class SavedJobSeeker(base_models.BaseModel):

    job_seeker = models.ForeignKey(
        'JobSeeker',
        on_delete=models.CASCADE,
    )
    company_user = models.ForeignKey(
        'company.CompanyUser',
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('job_seeker', 'company_user')


class JobSeekerActivityReport(JobSeeker):
    class Meta:
        proxy = True


class JobSeekerRegistrationReport(JobSeeker):
    class Meta:
        proxy = True
