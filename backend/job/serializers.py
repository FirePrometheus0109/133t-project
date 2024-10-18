# pylint: disable=abstract-method, arguments-differ
from rest_framework import serializers

from geo import serializers as geo_serializers
from job import models
from job import services as job_services
from job import validators
from leet import services as base_services
from leet import enums
from survey import serializers as survey_serializers
from survey import validators as survey_validators


class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Industry
        fields = (
            'id',
            'name'
        )


class SkillDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Skill
        fields = (
            'id',
            'name'
        )


class SkillDetailWithMatchingSerializer(SkillDetailSerializer):
    match = serializers.SerializerMethodField()

    class Meta(SkillDetailSerializer.Meta):
        fields = SkillDetailSerializer.Meta.fields + ('match',)

    def get_match(self, skill):
        return skill in self.context['js_skills']


class LocationSerializer(geo_serializers.AddressSerializer):
    class Meta(geo_serializers.AddressSerializer.Meta):
        fields = ('country', 'city', 'zip')
        extra_kwargs = {
            'country': {'required': True},
            'city': {'required': True},
        }


class JobDummySerializer(serializers.Serializer):
    amount = serializers.IntegerField(default=1)
    title = serializers.CharField(default='test job')

class JobCompanyUserSerializer(serializers.ModelSerializer,
                               validators.SalaryValueValidatorMixin):
    required_skills = serializers.PrimaryKeyRelatedField(
        queryset=models.Skill.objects.all(),
        write_only=True,
        many=True
    )
    optional_skills = serializers.PrimaryKeyRelatedField(
        queryset=models.Skill.objects.all(),
        write_only=True,
        required=False,
        many=True
    )
    status = serializers.CharField(max_length=16)
    description = serializers.CharField(max_length=1024)
    position_type = serializers.CharField(max_length=40)
    owner = serializers.SerializerMethodField()
    views_count = serializers.SerializerMethodField()
    applies_count = serializers.SerializerMethodField()
    questions = survey_serializers.BaseSurveyQuestionsSerializer(
        many=True,
        required=False)
    location = LocationSerializer(required=True)
    candidates_count = serializers.SerializerMethodField()

    class Meta:
        model = models.Job
        fields = (
            # required fields
            'id',
            'title',
            'industry',
            'location',
            'position_type',
            'description',
            'status',
            'required_skills',
            'autoapply_minimal_percent',

            # not required fields

            'education',
            'clearance',
            'experience',
            'salary_min',
            'salary_max',
            'salary_negotiable',
            'benefits',
            'travel',
            'education_strict',
            'publish_date',
            'optional_skills',
            'questions',
            'is_cover_letter_required',
            'closing_date',
            'manual_apply_strict_required_skills_matching',

            # read only fields
            'owner',
            'company',
            'created_at',
            'modified_at',
            'views_count',
            'applies_count',
            'company',
            'is_deleted',
            'deleted_at',
            'candidates_count',
            'guid'
        )

        read_only_fields = (
            'owner',
            'company',
            'created_at',
            'views_count',
            'applies_count',
            'company',
            'is_deleted',
            'deleted_at',
            'modified_at',
            'guid'
        )

    def create(self, validated_data):
        company_user = self.context['request'].user.company_user
        validated_data['owner'] = company_user
        validated_data['company'] = company_user.company
        return job_services.create_job(validated_data)

    def update(self, instance, validated_data):
        user = self.context['request'].user
        return job_services.update_job(user, instance, validated_data)

    @staticmethod
    def get_views_count(job):
        return job.views.count()

    @staticmethod
    def get_applies_count(job):
        return job.applies.count()

    @staticmethod
    def get_candidates_count(job):
        result = job_services.get_count_candidates(job.candidates.all())
        result['all'] = sum(result.values())
        return result

    @staticmethod
    def get_owner(job):
        return {
            'id': job.owner.id,
            'name': job.owner.user.get_full_name()
        }

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['required_skills'] = SkillDetailSerializer(
            instance.required_skills, many=True).data
        ret['optional_skills'] = SkillDetailSerializer(
            instance.optional_skills, many=True).data
        ret['industry'] = {
            'id': instance.industry.id,
            'name': instance.industry.name
        }
        return ret

    def validate(self, attrs):
        salary_min = attrs.get('salary_min')
        salary_max = attrs.get('salary_max')
        education = attrs.get('education')
        education_strict = attrs.get('education_strict', False)
        publish_date = attrs.get('publish_date')
        closing_date = attrs.get('closing_date')

        validators.validate_education(
            education,
            education_strict,
            self.error_messages['required'])
        validators.validate_salary(salary_min, salary_max)
        validators.validate_skills(
            attrs.get('required_skills', []),
            attrs.get('optional_skills', []))
        validators.validate_publish_and_closing_dates(
            publish_date, closing_date)

        customer = self.context['company'].customer
        validators.validate_company_jobs_balance(
            status=attrs.get('status'),
            job=self.instance,
            customer=customer
        )

        return attrs

    def validate_empty_values(self, data):
        handle_empty_dict = {
            'clearance': enums.ClearanceTypesEnum.NO_CLEARANCE.name, # noqa
            'education': enums.EducationTypesEnum.NO_EDUCATION.name, # noqa
            'experience': enums.ExperienceEnum.NO_EXPERIENCE.name,   # noqa
            'benefits': enums.BenefitsEnum.NO_BENEFITS.name,         # noqa
            'travel': enums.TravelOpportunitiesEnum.NO_TRAVEL.name,  # noqa
        }
        for key in handle_empty_dict.keys():    # noqa
            value = data.get(key, None)
            if value == '':
                data[key] = handle_empty_dict[key]
        return super().validate_empty_values(data)

    def validate_publish_date(self, publish_date):
        if publish_date:
            validators.validate_publish_date(self.instance, publish_date)
        return publish_date

    @staticmethod
    def validate_closing_date(closing_date):
        if closing_date:
            validators.validate_closing_date(closing_date)
        return closing_date

    @staticmethod
    def validate_required_skills(required_skills):
        validators.validate_count_of_skills(required_skills)
        return required_skills

    @staticmethod
    def validate_optional_skills(optional_skills):
        validators.validate_count_of_skills(optional_skills)
        return optional_skills

    def validate_questions(self, questions):
        survey_validators.validate_max_count_of_questions_in_survey(questions)
        survey_validators.validate_can_add_questions_to_saved(
            questions,
            self.context['company'])
        return questions

    def validate_status(self, status):
        if self.instance is not None:
            validators.validate_job_can_be_closed(self.instance, status)
        else:
            validators.validate_status_for_creating_job(status)
        return status


class JobUnauthorizedSerializer(JobCompanyUserSerializer):
    company = serializers.SerializerMethodField()
    questions = survey_serializers.JobSeekerJobQuestionsSerializer(many=True)
    location = LocationSerializer()

    class Meta:
        model = models.Job
        fields = (
            # required fields
            'id',
            'title',
            'company',
            'industry',
            'location',
            'position_type',
            'description',
            'required_skills',
            'education',
            'clearance',
            'experience',
            'salary_min',
            'salary_max',
            'salary_negotiable',
            'benefits',
            'travel',
            'education_strict',
            'publish_date',
            'optional_skills',
            'created_at',
            'questions'
        )

    @staticmethod
    def get_company(instance):
        return {
            'id': instance.company.id,
            'name': instance.company.name
        }

    def to_representation(self, instance):
        if not base_services.is_job_active(instance):
            return base_services.get_inactive_job_representation(instance)
        ret = super().to_representation(instance)
        if instance.salary_negotiable:
            ret.pop('salary_min')
            ret.pop('salary_max')
        return ret


class JobListJobSeekerSerializer(JobUnauthorizedSerializer):

    saved_at = serializers.SerializerMethodField()
    applied_at = serializers.SerializerMethodField()
    matching_percent = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        required=False
    )

    class Meta(JobUnauthorizedSerializer.Meta):
        fields = JobUnauthorizedSerializer.Meta.fields + (
            'saved_at',
            'matching_percent',
            'applied_at',
            'is_cover_letter_required',
            'ban_status',
            'guid'
        )

    def get_saved_at(self, job):
        js = self.context['request'].user.job_seeker
        savedjob_set = job.savedjob_set.all()
        saved_at = None
        for i in savedjob_set:
            if i.job_seeker == js:
                saved_at = i.created_at
        return saved_at

    def get_applied_at(self, job):
        js = self.context['request'].user.job_seeker
        job_applies = job.applies.all()
        applied_at = None
        for i in job_applies:
            if i.owner == js:
                applied_at = i.created_at
        return applied_at


class JobDetailsJobSeekerSerializer(JobListJobSeekerSerializer):
    is_education_match = serializers.SerializerMethodField()
    is_clearance_match = serializers.SerializerMethodField()
    is_questionnaire_answered = serializers.SerializerMethodField()

    class Meta(JobListJobSeekerSerializer.Meta):
        fields = JobListJobSeekerSerializer.Meta.fields + (
            'is_education_match',
            'is_clearance_match',
            'is_questionnaire_answered',
        )

    def get_is_clearance_match(self, job):
        job_seeker = self.context['request'].user.job_seeker
        return job_services.is_clearance_match(job, job_seeker)

    @staticmethod
    def get_is_education_match(job):  # noqa
        return True

    def get_is_questionnaire_answered(self, job):
        job_seeker = self.context['request'].user.job_seeker
        return job_services.is_questionnaire_answered(job, job_seeker)

    def to_representation(self, job):
        ret = super().to_representation(job)
        ret['required_skills'] = SkillDetailWithMatchingSerializer(
            job.required_skills, many=True, context=self.context).data
        ret['optional_skills'] = SkillDetailWithMatchingSerializer(
            job.optional_skills, many=True, context=self.context).data
        return ret


class JobViewerSerializer(serializers.ModelSerializer):

    viewer = serializers.SerializerMethodField()

    class Meta:
        model = models.ViewJob
        fields = (
            'viewer',
            'created_at'
        )

    @staticmethod
    def get_viewer(view):
        return {
            'id': view.owner.id,
            'name': view.owner.user.get_full_name()
        }


class JobIdsSerializer(serializers.Serializer):
    jobs = serializers.PrimaryKeyRelatedField(
        queryset=models.Job.objects.prefetch_related('candidates').all(),
        many=True
    )


class JobExportCSVSerializer(serializers.ModelSerializer):
    company = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    industry = serializers.SerializerMethodField()
    required_skills = serializers.SerializerMethodField()
    optional_skills = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    state = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    zip = serializers.SerializerMethodField()

    class Meta:
        model = models.Job
        fields = ('company', 'title', 'created_at', 'publish_date', 'author',
                  'status', 'country', 'state', 'city', 'zip', 'industry',
                  'position_type', 'education', 'experience',
                  'travel', 'salary_min', 'salary_max', 'salary_negotiable',
                  'clearance', 'benefits', 'description', 'required_skills',
                  'optional_skills',)

    @staticmethod
    def get_company(obj):
        return obj.company.name

    @staticmethod
    def get_author(obj):
        return obj.owner.user.get_full_name()

    @staticmethod
    def get_industry(obj):
        return obj.industry.name

    @staticmethod
    def get_country(obj):
        return obj.location.country.name

    @staticmethod
    def get_state(obj):
        return obj.location.city.state.name

    @staticmethod
    def get_city(obj):
        return obj.location.city.name

    @staticmethod
    def get_zip(obj):
        return obj.location.zip.code if obj.location.zip else ''

    def get_required_skills(self, obj):
        return self._get_skill_names(obj.required_skills)

    def get_optional_skills(self, obj):
        return self._get_skill_names(obj.optional_skills)

    @staticmethod
    def _get_skill_names(skills):
        skills = [skill.name for skill in skills]
        return ','.join(skills)


class ShareJobSerializer(serializers.Serializer):
    email = serializers.EmailField()
    url = serializers.URLField()


class JobEnumSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Job
        fields = (
            'id',
            'title'
        )
