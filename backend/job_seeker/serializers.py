# pylint: disable=abstract-method
import mimetypes

import magic

from django.contrib import auth
from rest_framework import serializers
from rest_framework import exceptions

from geo import serializers as geo_serializers
from geo import utils as geo_utils
from job import models as job_models
from job import serializers as job_serializers
from job import validators as job_validators
from job_seeker import models
from job_seeker import services
from job_seeker import validators
from leet import serializers as base_serializers
from leet import services as base_services
from leet import utils
from leet import validators as base_validators

User = auth.get_user_model()


class SaveRemoveBaseSerializer(serializers.Serializer):

    add = serializers.BooleanField(required=False)
    remove = serializers.BooleanField(required=False)

    def validate(self, attrs):
        add = attrs.get('add', False)
        remove = attrs.get('remove', False)
        validators.validate_save_remove_actions(add, remove)
        return attrs


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
        )


class UserSerializer(UserListSerializer):

    class Meta(UserListSerializer.Meta):
        model = User
        fields = UserListSerializer.Meta.fields + (
            'email',
        )

    @staticmethod
    def validate_email(email):
        base_validators.validate_user_email_uniqueness(email)
        return email


class JobSeekerProfileBaseSerializer(serializers.ModelSerializer):

    user = UserSerializer(required=False)
    address = geo_serializers.AddressSerializer(
        required=False,
        allow_null=True)
    photo = base_serializers.RestrictedVersatileImageFieldSerializer(
        sizes="thumbnail_images", allow_empty_file=True,
        required=False, read_only=True)

    class Meta:
        model = models.JobSeeker
        fields = (
            'id',
            'user',
            'photo',
            'phone',
            'address',
            'about',
            'position_type',
            'education',
            'salary_min',
            'salary_max',
            'clearance',
            'experience',
            'benefits',
            'travel',
            'skills',
            'industries'
        )

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['skills'] = job_serializers.SkillDetailSerializer(
            instance.skills.all(), many=True).data
        ret['industries'] = job_serializers.IndustrySerializer(
            instance.industries.all(), many=True).data
        return ret


class JobSeekerSerializer(JobSeekerProfileBaseSerializer,
                          job_validators.SalaryValueValidatorMixin):
    profile_completion = serializers.SerializerMethodField()
    guid = serializers.SerializerMethodField()

    class Meta(JobSeekerProfileBaseSerializer.Meta):
        fields = JobSeekerProfileBaseSerializer.Meta.fields + (
            'salary_public',
            'is_public',
            'profile_completion',
            'is_shared',
            'guid',
            'is_password_set'
        )
        read_only_fields = ('user', 'is_password_set')

    @staticmethod
    def get_guid(instance):
        if instance.is_shared:
            return instance.guid
        return None

    @staticmethod
    def get_profile_completion(instance):
        return services.get_profile_completion(instance)

    def update(self, instance, validated_data):
        skills = validated_data.pop('skills', None)
        user_data = validated_data.pop('user', None)
        address_data = validated_data.pop('address', None)
        industries = validated_data.pop('industries', None)
        instance = super().update(instance, validated_data)

        if skills is not None:
            instance.skills.clear()
            instance.skills.add(*skills)
        if industries is not None:
            instance.industries.clear()
            instance.industries.add(*industries)
        if user_data is not None:
            user_serializer = UserSerializer(data=user_data)
            user_serializer.is_valid(raise_exception=True)
            user_data = user_serializer.validated_data
            for attr, val in user_data.items():
                setattr(instance.user, attr, val)
            if 'email' in user_data:
                user_email_address = instance.user.emailaddress_set.first()
                user_email_address.email = user_data['email']
                user_email_address.save()
            instance.user.save()

        if address_data is not None:
            geo_utils.create_or_update_instance_address(instance, address_data)
        if instance.is_public and not services.is_profile_public(instance):
            instance.is_public = False
        instance.save()
        return instance

    def validate(self, attrs):
        salary_min = attrs.get('salary_min')
        salary_max = attrs.get('salary_max')
        validators.validate_salary(self.instance, salary_min, salary_max)
        is_public = attrs.get('is_public')
        validators.validate_can_public(self.instance, is_public)
        return attrs

    @staticmethod
    def validate_industries(industries):
        validators.validate_count_of_industries(industries)
        return industries

    @staticmethod
    def validate_skills(skills):
        validators.validate_count_of_skills(skills)
        return skills

    @staticmethod
    def validate_phone(phone):
        validators.validate_phone(phone)
        return phone

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if not instance.is_shared:
            ret.pop('guid')
        return ret


class PhotoSerializer(base_serializers.PhotoSerializerMixin,
                      serializers.ModelSerializer):
    photo = base_serializers.RestrictedVersatileImageFieldSerializer(
        sizes='thumbnail_images', allow_empty_file=True,
        required=True, allow_null=True)

    class Meta:
        model = models.JobSeeker
        fields = (
            'id',
            'user',
            'photo'
        )
        read_only_fields = ('user',)


class JobExperienceSerializer(serializers.ModelSerializer):

    """Serializer for JobExperienceViewSet"""

    class Meta:
        model = models.JobExperience
        fields = (
            'id',
            'owner',
            'company',
            'job_title',
            'description',
            'date_from',
            'date_to',
            'is_current',
            'employment'
        )
        read_only_fields = ('owner',)

    @staticmethod
    def validate_date_from(date_from):
        return validators.validate_date(date_from)

    @staticmethod
    def validate_date_to(date_to):
        return validators.validate_date(date_to)

    def validate(self, attrs):
        date_from = attrs.get('date_from')
        date_to = attrs.get('date_to')
        is_current = attrs.get('is_current', False)

        if self.instance is None:
            job_seeker = self.context['job_seeker']
            validators.validate_can_add_one_more_experience(job_seeker)

        validators.validate_dates_period(date_from, date_to, is_current)

        return attrs


class EducationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Education
        fields = (
            'id',
            'owner',
            'institution',
            'field_of_study',
            'degree',
            'date_from',
            'date_to',
            'location',
            'description',
            'is_current',
            'created_at'
        )
        read_only_fields = ('owner', 'created_at')

    @staticmethod
    def validate_date_from(date_from):
        return validators.validate_date(date_from)

    @staticmethod
    def validate_date_to(date_to):
        return validators.validate_date(date_to)

    def validate(self, attrs):
        date_from = attrs.get('date_from')
        date_to = attrs.get('date_to')
        is_current = attrs.get('is_current', False)
        job_seeker = self.context['job_seeker']

        validators.validate_count_educations_and_certifications(job_seeker)
        validators.validate_dates_period(date_from, date_to, is_current)

        return attrs


class CertificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Certification
        fields = (
            'id',
            'owner',
            'institution',
            'field_of_study',
            'graduated',
            'licence_number',
            'location',
            'description',
            'is_current',
            'created_at'
        )
        read_only_fields = ('owner', 'created_at')

    def validate(self, attrs):
        graduated = attrs.get('graduated')
        is_current = attrs.get('is_current')
        licence_number = attrs.get('licence_number')
        job_seeker = self.context.get('job_seeker')

        validators.validate_certification(
            graduated,
            is_current,
            licence_number)
        validators.validate_count_educations_and_certifications(job_seeker)

        return attrs


class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Document
        fields = (
            'id',
            'owner',
            'file',
            'name',
            'extension',
        )
        read_only_fields = (
            'id',
            'owner',
            'extension',
        )

    def validate(self, attrs):
        f = attrs['file']
        extension = self._get_extension(f)
        attrs['extension'] = extension
        validators.validate_document(
            self.context.get('job_seeker'), f, extension
        )
        return attrs

    def _get_extension(self, f):
        """Get document extension."""
        extension_mapping = {
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
            'text/rtf': '.rtf',
            'text/plain': '.txt',
            'application/vnd.oasis.opendocument.text': '.odt'
        }
        mimetype = magic.from_buffer(f.read(), mime=True)
        f.seek(0)
        extension = extension_mapping.get(mimetype, None)
        if not extension:
            extension = mimetypes.guess_extension(mimetype)
            if not extension:
                raise exceptions.ValidationError('The file has an unknown extension')
        return extension[1:]


class PublicJobSeekerProfileSerializer(JobSeekerProfileBaseSerializer):
    # TODO (m.nizovtsova): discuss with BA about salary negotiable
    #  in public profile
    educations = EducationSerializer(many=True)
    job_experience = JobExperienceSerializer(many=True)
    certifications = CertificationSerializer(many=True)

    class Meta(JobSeekerProfileBaseSerializer.Meta):
        fields = JobSeekerProfileBaseSerializer.Meta.fields + (
            'educations',
            'job_experience',
            'certifications',
        )

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if not instance.salary_public:
            ret.pop('salary_max')
            ret.pop('salary_min')
        return ret


class JobSeekerForCompanyUserSerializer(PublicJobSeekerProfileSerializer):
    is_applied = serializers.SerializerMethodField()
    is_purchased = serializers.SerializerMethodField()
    saved_at = serializers.SerializerMethodField()
    documents = DocumentSerializer(many=True)

    class Meta(PublicJobSeekerProfileSerializer.Meta):
        fields = PublicJobSeekerProfileSerializer.Meta.fields + (
            'is_applied',
            'is_purchased',
            'modified_at',
            'saved_at',
            'documents',
        )

    def get_is_applied(self, job_seeker):
        # TODO (i.bogretsov) company to serializer context
        company = self.context['request'].user.company_user.company
        return base_services.is_user_candidate_for_company(job_seeker, company)

    def get_is_purchased(self, job_seeker):
        company = self.context['request'].user.company_user.company
        return base_services.is_job_seeker_purchased(job_seeker, company)

    def get_saved_at(self, job_seeker):
        company_user = self.context['request'].user.company_user
        for saved_js in job_seeker.savedjobseeker_set.all():
            if saved_js.company_user == company_user:
                return saved_js.created_at
        return None

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if not ret['is_purchased']:
            ret['user'].pop('email')
            ret.pop('phone')
            ret.pop('address')
            ret.pop('documents')
        return ret


class SavedJobSerializer(SaveRemoveBaseSerializer):
    job = serializers.PrimaryKeyRelatedField(
        queryset=job_models.Job.objects.all()
    )


class CoverLetterSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CoverLetter
        fields = (
            'id',
            'owner',
            'title',
            'body',
            'is_default',
        )
        read_only_fields = ('owner',)

    def validate_title(self, title):
        validators.validate_cover_letter_title_uniqueness(
            self.context['job_seeker'], title, self.instance
        )
        return title

    def validate(self, attrs):
        if self.instance is None:
            validators.validate_max_cover_letter_count(
                self.context['job_seeker']
            )
        return attrs

    def create(self, validated_data):
        instance = super().create(validated_data)
        if validated_data.get('is_default'):
            services.set_the_rest_cover_letters_as_not_default(
                instance, validated_data)
        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        services.set_the_rest_cover_letters_as_not_default(
            instance, validated_data)
        return instance


class PurchasedJobSeekersListSerializer(serializers.ModelSerializer):

    user = UserListSerializer()
    location = serializers.SerializerMethodField()

    class Meta:
        model = models.JobSeeker
        fields = (
            'id',
            'modified_at',
            'is_deleted',
            'user',
            'location'
        )

    @staticmethod
    def get_location(job_seeker):
        city = utils.get_from_nested_structure(
            job_seeker, ['address', 'city'], default=None, func=getattr
        )
        if city:
            return geo_serializers.CitySerializer(city).data
        return {}


class JobSeekerViewerListSerializer(serializers.ModelSerializer):
    company = serializers.SerializerMethodField()

    class Meta:
        model = models.ViewJobSeeker
        fields = (
            'company',
            'created_at'
        )

    @staticmethod
    def get_company(instance):
        return {
            'id': instance.company_user.company.id,
            'company': instance.company_user.company.name
        }


class JobSeekerEnumSerializer(serializers.ModelSerializer):

    user = base_serializers.UserEnumSerializer()

    class Meta:
        model = models.JobSeeker
        fields = (
            'id',
            'user'
        )
