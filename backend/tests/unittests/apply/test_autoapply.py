from copy import deepcopy
from datetime import timedelta
import uuid
from django.conf import settings
from django.utils import timezone
from constance import config
import mock
import pytest

from apply.models import Apply, Autoapply
from apply.services import AutoapplyService, get_autoapply_days_to_completion
from apply import tasks, exceptions, constants
from geo.models import Address
from job.models import Skill, Job
from job.services import add_skills
from leet import enums
from notification_center import models as notif_models
from notification_center import utils as notif_utils
from tests.fixtures.job import document_management_software_skill, \
    project_management_software_skill, mysql_skill, \
    electronic_mail_software_skill, outlook_skill


class TestAutoapplyService:

    @pytest.mark.parametrize(('value', 'expected_status'), (
            (enums.ClearanceTypesEnum.CONFIDENTIAL.name,
             enums.ApplyStatusEnum.APPLIED.name),
            (enums.ClearanceTypesEnum.TOP_SECRET_SCI.name,
             enums.ApplyStatusEnum.NEED_REVIEW.name),
            (enums.ClearanceTypesEnum.TOP_SECRET.name,
             enums.ApplyStatusEnum.APPLIED.name),
            (0,
             enums.ApplyStatusEnum.APPLIED.name)
    ))
    def test_autoapply_status_depends_on_clearance(
            self, value, expected_status, job_seeker, job, autoapply):
        job.clearance = value
        job.save()
        autoapply = AutoapplyService(job_seeker, autoapply).start_autoapply(
            [job])
        assert autoapply.apply_set.filter(job=job)
        assert autoapply.apply_set.get(job=job).status == expected_status
        assert autoapply.status == enums.AutoapplyStatusEnum.FINISHED.name
        assert autoapply.finished_at

    @pytest.mark.parametrize(('value', 'expected_status'), (
            (False,
             enums.ApplyStatusEnum.APPLIED.name),
            (True,
             enums.ApplyStatusEnum.NEED_REVIEW.name),
    ))
    def test_autoapply_status_depends_on_cover_letter(
            self, value, expected_status, job_seeker, job, autoapply):
        job.is_cover_letter_required = value
        job.save()
        autoapply = AutoapplyService(job_seeker, autoapply).start_autoapply(
            [job])
        assert autoapply.apply_set.filter(job=job)
        assert (autoapply.apply_set.get(job=job).status == expected_status)
        assert autoapply.status == enums.AutoapplyStatusEnum.FINISHED.name
        assert autoapply.finished_at

    def test_autoapply_uses_default_cover_letter_if_exist(
            self, job_seeker, job, autoapply, cover_letter):
        job.is_cover_letter_required = True
        job.save()
        autoapply = AutoapplyService(job_seeker, autoapply).start_autoapply(
            [job])
        assert autoapply.apply_set.filter(job=job)
        assert (autoapply.apply_set.get(job=job).status
                == enums.ApplyStatusEnum.APPLIED.name)
        assert autoapply.apply_set.get(job=job).cover_letter == cover_letter
        assert autoapply.status == enums.AutoapplyStatusEnum.FINISHED.name
        assert autoapply.finished_at

    def test_autoapply_set_need_review_if_no_default_cover_letter(
            self, job_seeker, job, autoapply):
        job.is_cover_letter_required = True
        job.save()
        autoapply = AutoapplyService(job_seeker, autoapply).start_autoapply(
            [job])
        assert autoapply.apply_set.filter(job=job)
        assert (autoapply.apply_set.get(job=job).status
                == enums.ApplyStatusEnum.NEED_REVIEW.name)
        assert autoapply.apply_set.get(job=job).cover_letter is None
        assert autoapply.status == enums.AutoapplyStatusEnum.FINISHED.name
        assert autoapply.finished_at

    @pytest.mark.parametrize(('skills_fixtures', 'expected_status'), (
            ([
                 'mysql_skill',
                 'project_management_software_skill',
                 'document_management_software_skill'
             ], enums.ApplyStatusEnum.NEED_REVIEW.name),
            ([
                'project_management_software_skill'
            ], enums.ApplyStatusEnum.NEED_REVIEW.name),
            ([
                 'mysql_skill',
                 'document_management_software_skill'
             ], enums.ApplyStatusEnum.APPLIED.name),
            ([
                'mysql_skill',
                'outlook_skill'
             ], enums.ApplyStatusEnum.APPLIED.name),
            ([], enums.ApplyStatusEnum.APPLIED.name),
    ))
    def test_autoapply_status_depends_on_required_skills_matching(
            self, skills_fixtures, expected_status, job_seeker, job, autoapply,
            request):
        skill_list = [
            request.getfixturevalue(skill) for skill in skills_fixtures
        ]
        add_skills(
            job, skill_list, is_required=True)
        autoapply = AutoapplyService(job_seeker, autoapply).start_autoapply(
            [job])
        assert autoapply.apply_set.filter(job=job)
        assert (autoapply.apply_set.get(job=job).status == expected_status)
        assert autoapply.status == enums.AutoapplyStatusEnum.FINISHED.name
        assert autoapply.finished_at

    @pytest.mark.parametrize(('education_type', 'strict', 'expected_status'), (
            (enums.EducationTypesEnum.HIGH_SCHOOL.name,
             False, enums.ApplyStatusEnum.APPLIED.name),
            (enums.EducationTypesEnum.CERTIFICATION.name,
             True, enums.ApplyStatusEnum.APPLIED.name),
            (enums.EducationTypesEnum.PHD.name,
             True, enums.ApplyStatusEnum.NEED_REVIEW.name),
    ))
    def test_autoapply_status_depends_on_education(
            self, education_type, strict, expected_status,
            job_seeker, job, autoapply):
        job.education = education_type
        job.education_strict = strict
        job.save()
        autoapply = AutoapplyService(job_seeker, autoapply).start_autoapply(
            [job])
        assert autoapply.apply_set.filter(job=job)
        assert (autoapply.apply_set.get(job=job).status == expected_status)
        assert autoapply.status == enums.AutoapplyStatusEnum.FINISHED.name
        assert autoapply.finished_at

    # tests for job list that returns for autoapply process
    @pytest.mark.parametrize(('status',), (
            (enums.ApplyStatusEnum.APPLIED.name,),
            (enums.ApplyStatusEnum.NEED_REVIEW.name,),
    ))
    def test_autoapply_queue_doesnt_contain_applied_or_need_review_jobs(
            self, status, job_seeker, job, autoapply, country_usa, city_ashville):
        Apply.objects.create(
            job=job,
            owner=job_seeker,
            status=status
        )
        unapplied_job = deepcopy(job)
        unapplied_job.pk = None
        unapplied_job.guid = uuid.uuid4()
        self.reset_location(unapplied_job, country_usa, city_ashville)
        unapplied_job.title = 'Electrician'
        unapplied_job.save()
        jobs_qs = AutoapplyService(job_seeker, autoapply).get_autoapply_jobs()
        jobs_list = list(jobs_qs)
        assert job not in jobs_list
        assert unapplied_job in jobs_list

    def test_get_autoapply_days_to_completion_returns_expected_result(
            self, autoapply):
        days_pass = 0
        autoapply.status = enums.AutoapplyStatusEnum.IN_PROGRESS.name
        autoapply.started_at = timezone.now() - timedelta(days=days_pass)
        autoapply.save()
        autoapply_len = getattr(config, "AUTOAPPLY_PERIOD_LENGTH")
        days_left = get_autoapply_days_to_completion(autoapply)
        expected_days_left = autoapply_len - days_pass
        assert days_left == expected_days_left

    def test_autoapply_status_gets_finished_when_1_days_passed(
            self, autoapply):
        autoapply.status = enums.AutoapplyStatusEnum.IN_PROGRESS.name
        autoapply.started_at = timezone.now()
        autoapply.save()
        date = timezone.now() + timedelta(days=1)
        with mock.patch('django.utils.timezone.now', new=lambda: date):
            tasks.find_autoapply_jobs.delay()
        autoapply.refresh_from_db()
        assert autoapply.status == enums.AutoapplyStatusEnum.FINISHED.name
        assert autoapply.finished_at

    def test_autoapply_status_doesnt_change_if_1_days_didnt_pass(
            self, autoapply):
        autoapply.status = enums.AutoapplyStatusEnum.IN_PROGRESS.name
        autoapply.started_at = timezone.now()
        autoapply.save()
        date = timezone.now() + timedelta(days=0.5)
        with mock.patch('django.utils.timezone.now', new=lambda: date):
            tasks.find_autoapply_jobs.delay()
        autoapply.refresh_from_db()
        assert autoapply.status == enums.AutoapplyStatusEnum.IN_PROGRESS.name

    def test_autoapply_jobs_list_updated_when_actual_job_appears(
            self, autoapply, job, country_usa, city_ashville):
        autoapply.number = 5
        autoapply.save()
        AutoapplyService(autoapply.owner, autoapply).start_autoapply([job])
        assert autoapply.jobs.count() == 1
        new_job = deepcopy(job)
        new_job.pk = None
        new_job.guid = uuid.uuid4()
        self.reset_location(new_job, country_usa, city_ashville)
        new_job.save()
        tasks.find_autoapply_jobs.delay()
        assert autoapply.jobs.count() == 2
        assert (autoapply.apply_set.get(job=new_job).status ==
                enums.ApplyStatusEnum.APPLIED.name)
        assert autoapply.status == enums.AutoapplyStatusEnum.IN_PROGRESS.name

    def test_autoapply_finishes_when_appropriate_jobs_number_found(
            self, autoapply, job, country_usa, city_ashville):
        autoapply.number = 2
        autoapply.save()
        AutoapplyService(autoapply.owner, autoapply).start_autoapply([job])
        new_job = deepcopy(job)
        new_job.pk = None
        new_job.guid = uuid.uuid4()
        self.reset_location(new_job, country_usa, city_ashville)
        new_job.save()
        tasks.find_autoapply_jobs.delay()
        assert autoapply.jobs.count() == 2
        assert (autoapply.apply_set.get(job=new_job).status ==
                enums.ApplyStatusEnum.APPLIED.name)
        autoapply.refresh_from_db()
        assert autoapply.status == enums.AutoapplyStatusEnum.FINISHED.name
        assert autoapply.finished_at

    def test_autoapply_jobs_list_with_viewed_apply_status(
            self, autoapply, job, country_usa, city_ashville, city_new_york):
        autoapply.number = 5
        autoapply.save()
        AutoapplyService(autoapply.owner, autoapply).start_autoapply([job])
        assert autoapply.jobs.count() == 1
        new_job = deepcopy(job)
        new_job.pk = None
        new_job.guid = uuid.uuid4()
        self.reset_location(new_job, country_usa, city_ashville)
        new_job.save()
        apply = Apply.objects.create(
            job=new_job,
            autoapply=autoapply,
            status=enums.ApplyStatusEnum.VIEWED.name,
            owner=autoapply.owner
        )
        tasks.find_autoapply_jobs.delay()
        assert autoapply.jobs.count() == 2
        assert (autoapply.apply_set.get(job=new_job).status ==
                enums.ApplyStatusEnum.APPLIED.name)


    def test_autoapply_new_jobs_respect_number(self, autoapply, job, country_usa, city_ashville):
        """Check that number of applied and need review jobs
        can't be greater than the number AA field."""
        autoapply.number = 2
        autoapply.save()
        AutoapplyService(autoapply.owner, autoapply).start_autoapply([job])
        for _ in range(2):
            new_job = deepcopy(job)
            new_job.pk = None
            new_job.guid = uuid.uuid4()
            self.reset_location(new_job, country_usa, city_ashville)
            new_job.save()
        tasks.find_autoapply_jobs.delay()
        assert Job.objects.count() == 3
        assert autoapply.jobs.count() == 2


    @pytest.mark.parametrize(
        ('field_name', 'query_param_name', 'good_value', 'bad_value'), (
        ('title', 'search',
         'Architect',
         'Support'),
        ('education', 'education',
         enums.EducationTypesEnum.BACHELORS_DEGREE.name,
         enums.EducationTypesEnum.NO_EDUCATION.name),
        ('clearance', 'clearance',
         enums.ClearanceTypesEnum.TOP_SECRET.name,
         enums.ClearanceTypesEnum.TOP_SECRET_SCI.name),
    ))
    def test_autoapply_filter_new_jobs(
            self, field_name, query_param_name, good_value, bad_value,
            autoapply, job, country_usa, city_ashville, city_new_york):
        query_params = f'{query_param_name}={good_value}'
        autoapply.query_params = query_params
        aa_service = AutoapplyService(autoapply.owner, autoapply)
        new_job = deepcopy(job)
        new_job.pk = None
        setattr(new_job, field_name, bad_value)
        new_job.guid = uuid.uuid4()
        self.reset_location(new_job, country_usa, city_ashville)
        new_job.save()
        jobs = aa_service.filter_jobs_by_autoapply_query_params(Job.objects.all())
        assert Job.objects.count() == 2
        assert getattr(jobs.get(), field_name) == good_value

    def test_autoapply_filter_by_position(self,autoapply, job, country_usa, city_ashville, city_new_york):
        aa_service = AutoapplyService(autoapply.owner, autoapply)
        new_job = deepcopy(job)
        new_job.pk = None
        new_job.position_type = enums.PositionTypesEnum.COMMISSION
        new_job.guid = uuid.uuid4()
        self.reset_location(new_job, country_usa, city_ashville)
        new_job.save()
        jobs = aa_service.filter_jobs_by_position(Job.objects.all())
        assert Job.objects.count() == 2
        assert jobs.count() == 1

    def test_autoapply_jobs_list_doesnt_change_when_applied_job_updates(
            self, autoapply, job, city_new_york):
        autoapply.number = 5
        autoapply.save()
        AutoapplyService(autoapply.owner, autoapply).start_autoapply([job])
        assert autoapply.jobs.count() == 1
        job.location.city = city_new_york
        job.save()
        tasks.find_autoapply_jobs.delay()
        assert autoapply.jobs.count() == 1

    def test_find_autoapply_jobs_ignores_wrong_position(
            self, autoapply, job, country_usa, city_ashville,):
        autoapply.number = 5
        autoapply.save()
        AutoapplyService(autoapply.owner, autoapply).start_autoapply([job])
        assert autoapply.jobs.count() == 1
        new_job = deepcopy(job)
        new_job.pk = None
        new_job.position_type = enums.PositionTypesEnum.COMMISSION
        new_job.guid = uuid.uuid4()
        self.reset_location(new_job, country_usa, city_ashville)
        new_job.save()
        tasks.find_autoapply_jobs.delay()
        assert Job.objects.count() == 2
        assert autoapply.jobs.count() == 1

    def test_autoapply_to_jobs_change_apply_status_if_exist(
            self, autoapply, job, job_seeker):
        autoapply.status = enums.AutoapplyStatusEnum.IN_PROGRESS.name
        autoapply.started_at = timezone.now()
        autoapply.save()
        apply = Apply.objects.create(
            autoapply=autoapply,
            job=job,
            status=enums.ApplyStatusEnum.VIEWED.name,
            owner=autoapply.owner
        )
        updated_apply = AutoapplyService(
            job_seeker, autoapply).autoapply_to_job(job)
        assert apply.id == updated_apply.id
        assert updated_apply.status in constants.APPLIED_OR_NEED_REVIEW

    @pytest.mark.parametrize(('status',), (
            (enums.AutoapplyStatusEnum.STOPPED.name,),
            (enums.AutoapplyStatusEnum.FINISHED.name,)
    ))
    def test_restart_autoapply_success_if_required_job_number_wasnt_found(
            self, status, autoapply, job_seeker, job):
        autoapply.status = status
        autoapply.number = 10
        autoapply.save()
        autoapply.apply_set.add(
            Apply.objects.create(
                autoapply=autoapply,
                job=job,
                status=enums.ApplyStatusEnum.VIEWED.name,
                owner=autoapply.owner
            )
        )
        AutoapplyService(job_seeker, autoapply).restart_autoapply()
        autoapply.refresh_from_db()
        assert autoapply.status == enums.AutoapplyStatusEnum.IN_PROGRESS.name

    def test_restart_fails_if_if_required_job_number_was_found(
            self, autoapply, job_seeker, job):
        autoapply.status = enums.AutoapplyStatusEnum.FINISHED.name
        autoapply.number = 1
        autoapply.save()
        autoapply.apply_set.add(
            Apply.objects.create(
                autoapply=autoapply,
                job=job,
                status=enums.ApplyStatusEnum.VIEWED.name,
                owner=autoapply.owner
            )
        )
        with pytest.raises(exceptions.ApplyException) as exc:
            AutoapplyService(job_seeker, autoapply).restart_autoapply()
            assert exc.value == constants.IMPOSSIBLE_TO_RESTART_AUTOAPPLY_ERROR
        autoapply.refresh_from_db()
        assert autoapply.status == enums.AutoapplyStatusEnum.FINISHED.name

    @pytest.mark.parametrize(('status',), (
            (enums.AutoapplyStatusEnum.IN_PROGRESS.name,),
            (enums.AutoapplyStatusEnum.SAVED.name,),
    ))
    def test_restart_fails_is_wrong_autoapply_status(
            self, status, autoapply, job_seeker):
        autoapply.status = status
        autoapply.save()
        with pytest.raises(exceptions.ApplyException) as exc:
            AutoapplyService(job_seeker, autoapply).restart_autoapply()
            assert exc.value == constants.IMPOSSIBLE_TO_RESTART_AUTOAPPLY_ERROR
        autoapply.refresh_from_db()
        assert autoapply.status == status

    @pytest.mark.parametrize(('status',), (
            (enums.AutoapplyStatusEnum.IN_PROGRESS.name,),
            (enums.AutoapplyStatusEnum.STOPPED.name,),
            (enums.AutoapplyStatusEnum.FINISHED.name,)
    ))
    def test_delete_autoapply_doesnt_delete_applied_jobs(
            self, status, autoapply, job, job_seeker,
            city_ashville, country_usa):

        autoapply.status = status
        autoapply.save()
        need_review_job = deepcopy(job)
        need_review_job.pk = None
        need_review_job.guid = uuid.uuid4()
        self.reset_location(need_review_job, country_usa, city_ashville)
        need_review_job.save()
        viewed_job = deepcopy(job)
        viewed_job.pk = None
        viewed_job.guid = uuid.uuid4()
        self.reset_location(viewed_job, country_usa, city_ashville)
        viewed_job.save()
        new_job = deepcopy(job)
        new_job.pk = None
        new_job.guid = uuid.uuid4()
        self.reset_location(new_job, country_usa, city_ashville)
        new_job.save()
        autoapply.apply_set.add(
            Apply.objects.create(
                job=job,
                status=enums.ApplyStatusEnum.APPLIED.name,
                applied_at=timezone.now(),
                owner=job_seeker
            ),
            Apply.objects.create(
                job=need_review_job,
                status=enums.ApplyStatusEnum.NEED_REVIEW.name,
                applied_at=timezone.now(),
                owner=job_seeker
            ),
            Apply.objects.create(
                job=viewed_job,
                status=enums.ApplyStatusEnum.VIEWED.name,
                applied_at=timezone.now(),
                owner=job_seeker
            ),
            Apply.objects.create(
                job=new_job,
                status=enums.ApplyStatusEnum.NEW.name,
                applied_at=timezone.now(),
                owner=job_seeker
            ),
        )

        AutoapplyService(job_seeker, autoapply).delete_autoapply()
        assert not Autoapply.objects.filter(id=autoapply.id).exists()
        assert Apply.objects.filter(
            job=job, owner=job_seeker, autoapply=None
        ).exists()
        assert not Apply.objects.filter(
            job=need_review_job, owner=job_seeker
        ).exists()
        assert not Apply.objects.filter(
            job=viewed_job, owner=job_seeker
        ).exists()
        assert not Apply.objects.filter(
            job=new_job, owner=job_seeker
        ).exists()

    def test_delete_saved_autoapply_success(self, autoapply, job_seeker):
        AutoapplyService(job_seeker, autoapply).delete_autoapply()
        assert not Autoapply.objects.filter(id=autoapply.id).exists()

    @staticmethod
    def reset_location(job, country, city):
        job.location = Address.objects.create(
            country=country,
            city=city
        )


class TestAutoapplyNotification:

    @pytest.mark.parametrize(('status',), (
            (enums.AutoapplyStatusEnum.STOPPED.name,),
            (enums.AutoapplyStatusEnum.FINISHED.name,)
    ))
    def test_autoapply_notification_sent_once_after_autoapply_finished_or_stopped(
            self, status, autoapply, mailoutbox):
        autoapply.status = status
        autoapply.finished_at = timezone.now()
        autoapply.save()
        tasks.send_autoapply_email_notifications.delay()
        assert mailoutbox
        mailoutbox.clear()
        date = timezone.now() + timedelta(days=1)
        with mock.patch('django.utils.timezone.now', new=lambda: date):
            tasks.send_autoapply_email_notifications.delay()
        assert not mailoutbox

    def test_autoapply_notification_isnt_sent_for_saved_autoapply(
            self, autoapply, mailoutbox):
        autoapply.status = enums.AutoapplyStatusEnum.SAVED.name
        autoapply.save()
        tasks.send_autoapply_email_notifications.delay()
        assert not mailoutbox

    def test_sent_autoapply_notif_is_not_sent_user_unsubscribed(
            self, job_seeker, finished_autoapply, mailoutbox):
        mailoutbox.clear()
        qs = notif_models.NotificationType.objects.all()
        qs = notif_utils.get_notif_types_for_manage(job_seeker.user, qs)
        job_seeker.user.subscribed_notifications.remove(*qs)
        tasks.send_autoapply_email_notifications.delay()
        assert not mailoutbox
