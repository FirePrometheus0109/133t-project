from datetime import timedelta
from unittest import mock

from django.conf import settings
import pytest

from job.models import Job
from job import tasks


class TestHardDeleteJob:

    def test_soft_deleted_jobs_becomes_inactive_after_half_a_year_passed(
            self, company_deleted_job):
        hard_delete_period_length = getattr(
            settings, 'HARD_DELETE_JOBS_INTERVAL_LENGTH'
        )
        deleted_job = Job.objects.get(id=company_deleted_job['id'])
        deleted_at = deleted_job.deleted_at
        in_future_date = deleted_at + timedelta(
            days=hard_delete_period_length
        )
        with mock.patch('django.utils.timezone.now',
                        new=lambda: in_future_date):
            tasks.hard_delete_jobs.delay()
        with pytest.raises(Job.DoesNotExist):
            Job.objects.get(id=company_deleted_job['id'])

    def test_filter_doesnt_return_inactive_job(
            self, company_inactive_job_id):
        assert not Job.objects.filter(id=company_inactive_job_id).exists()

    def test_count_doesnt_consider_inactive_job(
            self, company_inactive_job_id):
        assert not Job.objects.filter(id=company_inactive_job_id).count()

    def test_get_inactive_job_raises(
            self, company_inactive_job_id):
        with pytest.raises(Job.DoesNotExist):
            Job.objects.get(id=company_inactive_job_id)

    @pytest.mark.usefixtures('company_inactive_job_id')
    def test_all_doesnt_include_inactive_job(self):
        assert not len(Job.objects.all())
