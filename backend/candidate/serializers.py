# pylint: disable=abstract-method,too-many-public-methods
from django.conf import settings
from rest_framework import serializers

from apply import services as apply_services
from candidate import constants
from candidate import models
from candidate import utils
from candidate import validators
from company import models as company_models
from job import models as job_models
from job import serializers as job_serializers
from job_seeker import models as js_models
from job_seeker import serializers as js_serializers
from leet import constants as base_constants
from leet import enums
from leet import models as base_models
from leet import serializers as base_serializers
from leet import utils as base_utils
from survey import models as survey_models
from survey import serializers as survey_serializers
from survey import validators as survey_validators


class JobSeekerAnswerChildSerializer(serializers.Serializer):
    """
    This serializer is used like a child for JobSeekerAnswerCreateSerializer.
    """

    question = serializers.PrimaryKeyRelatedField(
        queryset=survey_models.Question.objects.all(),
    )
    answer = survey_serializers.AnswerSerializer()

    def validate(self, attrs):
        question = attrs['question']
        answer = attrs.get('answer', {})
        emsg = constants.ANSWER_IS_REQUIRED_ON_QUESTION_ERROR.format(
            question.body)
        survey_validators.validate_required_answers(question, answer, emsg)
        return attrs


class JobSeekerAnswerCreateSerializer(serializers.ListSerializer):
    """Serializer for bulk creating answers."""

    child = JobSeekerAnswerChildSerializer()

    def validate(self, attrs):
        questions = [i['question'] for i in attrs]
        job = self.context['job']
        survey_validators.validate_max_count_of_questions_in_survey(attrs)
        validators.validate_questions_for_answers(questions, job)
        validators.validate_job_seeker_can_create_answers(
            self.context['job_seeker'],
            job,
            self.context['existing_answers'])
        return attrs


class JobSeekerAnswerResponseSerializer(serializers.ModelSerializer):
    """Serializer for view answers by job seeker."""

    question = survey_serializers.QuestionEnumSerializer()
    answer = serializers.SerializerMethodField()

    class Meta:
        model = survey_models.AnswerJobSeeker
        fields = (
            'id',
            'question',
            'answer'
        )

    @staticmethod
    def get_answer(instance):
        if instance.answer_type == enums.AnswerTypeEnum.YES_NO.name:  # noqa
            return instance.answer.yes_no_value
        return ''


class CandidateAnswersSerializer(JobSeekerAnswerResponseSerializer):
    """
    Serializer for view answers by company user.
    Company user can see disaqualifiyng answers.
    """

    question = survey_serializers.QuestionEnumSerializer()
    is_disqualify = serializers.SerializerMethodField()

    class Meta(JobSeekerAnswerResponseSerializer.Meta):
        fields = (
            'id',
            'question',
            'answer',
            'is_disqualify'
        )

    @staticmethod
    def get_is_disqualify(answer):
        disqual_answer = answer.question.disqualifying_answer
        if disqual_answer and disqual_answer == answer.answer.yes_no_value:
            return True
        return False


class CandidateAssignSerializer(serializers.Serializer):

    job_seekers = serializers.PrimaryKeyRelatedField(
        queryset=js_models.JobSeeker.objects.values(
            'id', 'user__first_name', 'user__last_name'),
        many=True
    )
    jobs = serializers.PrimaryKeyRelatedField(
        queryset=job_models.Job.objects.values('id', 'status', 'title'),
        many=True
    )

    def validate_job_seekers(self, job_seekers):
        validators.validate_job_seekers_count(job_seekers)
        company = self.context['company']
        validators.validate_can_assign_job_seeker(job_seekers, company)
        return job_seekers

    @staticmethod
    def validate_jobs(jobs):
        validators.validate_jobs_count(jobs)
        validators.validate_jobs_statuses_for_assigning(jobs)
        return jobs


class CandidateBaseSerializer(serializers.ModelSerializer):

    job_seeker = js_serializers.JobSeekerForCompanyUserSerializer()
    rating = serializers.SerializerMethodField()
    job = job_serializers.JobEnumSerializer()
    status = base_serializers.CandidateStatusSerializer()
    applied_date = serializers.DateTimeField()

    class Meta:
        model = models.Candidate
        fields = (
            'id',
            'job',
            'job_seeker',
            'rating',
            'status',
            'applied_date',
        )

    @staticmethod
    def get_rating(candidate):
        if hasattr(candidate, 'rating'):
            return {
                'owner': candidate.rating.owner.user.get_full_name(),
                'rating': candidate.rating.rating
            }
        return {
            'owner': '',
            'rating': enums.RatingEnum.NO_RATING.name  # noqa
        }


class CandidateDetailsSerializer(CandidateBaseSerializer):

    is_applied_after_assignment = serializers.SerializerMethodField()
    is_disqualified_for_questionnaire = serializers.BooleanField()
    is_disqualified_for_skills = serializers.SerializerMethodField()
    cover_letter = serializers.SerializerMethodField()

    class Meta(CandidateBaseSerializer.Meta):
        fields = CandidateBaseSerializer.Meta.fields + (
            'is_applied_after_assignment',
            'is_disqualified_for_questionnaire',
            'is_disqualified_for_skills',
            'created_at',
            'previous_applied_date',
            'cover_letter'
        )

    @staticmethod
    def get_cover_letter(candidate):
        apply = candidate.apply
        if apply is not None and apply.cover_letter is not None:
            return js_serializers.CoverLetterSerializer(
                apply.cover_letter).data
        return None

    @staticmethod
    def get_is_applied_after_assignment(candidate):
        apply = candidate.apply
        if apply and apply.applied_at:
            return apply.applied_at > candidate.created_at
        return False

    @staticmethod
    def get_is_disqualified_for_skills(candidate):
        """
        If and applied candidate does not have any required skill
        he is disqualified.
        """
        if candidate.apply is None:
            return False

        job_seeker = candidate.job_seeker
        job = candidate.job
        are_skills_matched = apply_services.are_js_required_skills_matched(
            job_seeker,
            job)
        return not are_skills_matched


class CandidateListSerializer(CandidateDetailsSerializer):

    job_seeker = js_serializers.PurchasedJobSeekersListSerializer()


class CandidateQuickViewSerializer(CandidateBaseSerializer):
    pass


class CandidateRatingCreateUpdateSerializer(serializers.Serializer):

    rating = serializers.ChoiceField(choices=enums.RatingEnum.choices)


class CandidateStatusSerializer(serializers.Serializer):

    status = serializers.PrimaryKeyRelatedField(
        queryset=base_models.CandidateStatus.objects.all()
    )

    def validate(self, attrs):
        validators.validate_can_change_status_on_workflow(self.instance)
        return attrs


class CandidateActivitySerializer(serializers.ModelSerializer):

    candidate = serializers.SerializerMethodField()
    activity = serializers.SerializerMethodField()
    job = serializers.SerializerMethodField()

    class Meta:
        model = models.WorkflowStep
        fields = (
            'candidate',
            'activity',
            'job',
            'created_at'
        )

    @staticmethod
    def get_candidate(workflow_step):
        return {
            'id': workflow_step.candidate.id,
            'name': workflow_step.candidate.job_seeker.user.get_full_name()
        }

    @staticmethod
    def get_job(workflow_step):
        return {
            'id': workflow_step.candidate.job.id,
            'title': workflow_step.candidate.job.title
        }

    @staticmethod
    def get_activity(workflow_step):
        applied_status = base_constants.CANDIDATE_STATUS_APPLIED
        status_name = workflow_step.status.name
        activity = status_name
        apply = workflow_step.candidate.apply
        if apply is None and status_name == applied_status:
            activity = constants.CANIDIDATE_ASSIGN_ACTIVITY
        return activity


# NOTE (m.nizovtsova): located in candidate module to avoid of circular
# dependencies between company and candidate modules
class CompanyUserCandidatesActivitySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    is_online = serializers.SerializerMethodField()
    stats = serializers.SerializerMethodField()

    class Meta:
        model = company_models.CompanyUser
        fields = (
            'is_online',
            'user',
            'stats'
        )

    @staticmethod
    def get_is_online(instance):
        return base_utils.get_user_online_status(instance.user)

    @staticmethod
    def get_user(instance):
        return {
            'id': instance.user.id,
            'name': instance.user.get_full_name()
        }

    @staticmethod
    def get_stats(instance):
        to_repr_status_map = {
            base_constants.CANDIDATE_STATUS_SCREENED: 'Screenings',
            base_constants.CANDIDATE_STATUS_INTERVIEWED: 'Interviews',
            base_constants.CANDIDATE_STATUS_OFFERED: 'Offers',
            base_constants.CANDIDATE_STATUS_HIRED: 'Hired Candidates',
            base_constants.CANDIDATE_STATUS_REJECTED: 'Rejected Candidates'
        }
        # TODO (m.nizovtsova): clarify requirements about Applied status
        # and nullable values
        workflow_stats = utils.get_candidate_workflow_steps_stats(
            instance.workflowstep_set)
        result = []
        for item in workflow_stats:
            if item['name'] != base_constants.CANDIDATE_STATUS_APPLIED:
                result.append({
                    to_repr_status_map[item['name']]: item['n_candidates']
                })
        saved_candidates_count = instance.savedjobseeker_set.count()
        jobs_count = instance.jobs.count()
        result.insert(0, {'Created Job postings': jobs_count})
        result.append({'Saved Candidates': saved_candidates_count})
        return result


class CandidateExportToCSVSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    job = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    industries = serializers.SerializerMethodField()
    position_type = serializers.SerializerMethodField()
    education = serializers.SerializerMethodField()
    experience = serializers.SerializerMethodField()
    travel = serializers.SerializerMethodField()
    salary_min = serializers.SerializerMethodField()
    salary_max = serializers.SerializerMethodField()
    clearance = serializers.SerializerMethodField()
    benefits = serializers.SerializerMethodField()
    skills = serializers.SerializerMethodField()
    education_details = serializers.SerializerMethodField()
    experience_details = serializers.SerializerMethodField()
    workflow_step = serializers.SerializerMethodField()
    applied_date = serializers.DateTimeField(
        format=settings.DEFAULT_SERVER_DATE_FORMAT
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        model = models.Candidate
        fields = (
            'first_name', 'last_name', 'job', 'applied_date', 'location',
            'updated_at', 'email', 'phone', 'address', 'industries',
            'position_type', 'education', 'experience', 'travel', 'salary_min',
            'salary_max', 'clearance', 'benefits', 'skills', 'rating',
            'education_details', 'experience_details', 'workflow_step',
        )

    @staticmethod
    def get_first_name(obj):
        return obj.job_seeker.user.first_name

    @staticmethod
    def get_last_name(obj):
        return obj.job_seeker.user.last_name

    @staticmethod
    def get_job(obj):
        return obj.job.title

    @staticmethod
    def get_updated_at(obj):
        return obj.job_seeker.modified_at.strftime(
            settings.DEFAULT_SERVER_DATE_FORMAT
        )

    @staticmethod
    def get_location(obj):
        return '{} ({})'.format(obj.job_seeker.address.city,
                                obj.job_seeker.address.city.state.abbreviation)

    @staticmethod
    def get_email(obj):
        return obj.job_seeker.user.email

    @staticmethod
    def get_phone(obj):
        return obj.job_seeker.phone

    @staticmethod
    def get_address(obj):
        return obj.job_seeker.address.address

    @staticmethod
    def get_industries(obj):
        industry_names = [
            industry.name for industry in obj.job_seeker.industries.all()
        ]
        return ','.join(industry_names)

    @staticmethod
    def get_position_type(obj):
        return obj.job_seeker.get_position_type_display()

    @staticmethod
    def get_education(obj):
        return obj.job_seeker.get_education_display()

    @staticmethod
    def get_experience(obj):
        return obj.job_seeker.get_experience_display()

    @staticmethod
    def get_travel(obj):
        return obj.job_seeker.get_travel_display()

    @staticmethod
    def get_salary_min(obj):
        return (obj.job_seeker.salary_min
                if obj.job_seeker.salary_public else '')

    @staticmethod
    def get_salary_max(obj):
        return (obj.job_seeker.salary_max
                if obj.job_seeker.salary_public else '')

    @staticmethod
    def get_clearance(obj):
        return obj.job_seeker.get_clearance_display()

    @staticmethod
    def get_benefits(obj):
        return obj.job_seeker.get_benefits_display()

    @staticmethod
    def get_skills(obj):
        skill_names = [skill.name for skill in obj.job_seeker.skills.all()]
        return ','.join(skill_names)

    @staticmethod
    def get_education_details(obj):
        js_educations = obj.job_seeker.educations.order_by('id')
        js_certifications = obj.job_seeker.certifications.order_by('id')
        educations_formatted = []

        for education in js_educations:
            education_attrs = [
                education.institution,
                education.get_degree_display(),
                education.field_of_study,
                str(education.date_to.year) if education.date_to else ''
            ]
            education_formatted = ' '.join(
                attr for attr in education_attrs if attr
            )
            educations_formatted.append(education_formatted)

        for certification in js_certifications:
            certification_attrs = [
                certification.institution,
                certification.field_of_study,
                str(certification.graduated.year)
                if certification.graduated else ''
            ]
            certification_formatted = ' '.join(
                attr for attr in certification_attrs if attr
            )
            educations_formatted.append(certification_formatted)

        return ','.join(educations_formatted)

    @staticmethod
    def get_experience_details(obj):
        js_experiences = obj.job_seeker.job_experience.all()
        experiences = [
            ' '.join([
                ex.job_title,
                'at',
                ex.company,
                '{} - {}'.format(
                    str(ex.date_from.year),
                    str(ex.date_to.year) if ex.date_to else 'Now'
                )
            ]) for ex in js_experiences
        ]
        return ','.join(experiences)

    @staticmethod
    def get_workflow_step(obj):
        return obj.status.name

    @staticmethod
    def get_rating(obj):
        return (
            obj.rating.get_rating_display()
            if hasattr(obj, 'rating')
            else enums.RatingEnum.NO_RATING.value  # noqa
        )


class CandidateEnumSerializer(serializers.ModelSerializer):

    job_seeker = js_serializers.JobSeekerEnumSerializer()

    class Meta:
        model = models.Candidate
        fields = (
            'id',
            'job_seeker',
        )
