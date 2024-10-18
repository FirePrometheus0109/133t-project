import copy
import datetime
import http
from unittest import mock

import faker
import pytest
from django.conf import settings
from django.utils import timezone

from job import constants, tasks
from job import models
from leet import enums
from survey import constants as survey_constants
from tests import api_requests
from tests import utils
from tests import validators
from tests.api.job import expected

fake = faker.Faker()


class TestJobApiCommon:

    def test_unauthenticated_user_cant_create(self, anonym_client):
        resp = api_requests.create_job(
            anonym_client,
            {})
        assert resp.status_code == http.HTTPStatus.UNAUTHORIZED

    @pytest.mark.parametrize(('http_method',), (
        (api_requests.update_job,),
        (api_requests.partial_update_job,),
    ))
    def test_unauthenticated_user_cant_create_update(
            self, anonym_client, http_method, job):
        resp = http_method(
            anonym_client,
            job['id'],
            {})
        assert resp.status_code == http.HTTPStatus.UNAUTHORIZED


class TestJob:

    def test_create_dummy(self, company_user_client):
        from django import urls
        import json
        resp = company_user_client.post(
            urls.reverse('job:api_v1:create-dummy'),
            data=json.dumps({'amount': 10, 'title': 'Hello world'}),
            content_type='application/json'
        )
        assert resp.status_code == http.HTTPStatus.CREATED
        assert models.Job.objects.count() == 10
        assert models.Job.objects.first().title == 'Hello world 0'

    def test_create_draft_success(
            self, company_user_client, job_base_data):
        data = copy.deepcopy(job_base_data)
        data['status'] = enums.JobStatusEnum.DRAFT.name
        resp = api_requests.create_job(
            company_user_client,
            data)
        assert resp.status_code == http.HTTPStatus.CREATED
        assert resp.json()['status'] == data['status']

    def test_publish_job_immediately(
            self, company_user_client, job_base_data):
        date = utils.date(2018, 10, 1)
        with mock.patch('django.utils.timezone.now', new=lambda: date):
            resp = api_requests.create_job(
                company_user_client,
                job_base_data)
            active = enums.JobStatusEnum.ACTIVE.name
            assert resp.status_code == http.HTTPStatus.CREATED
            assert resp.json()['status'] == active
            valid_date = timezone.now().strftime('%Y-%m-%dT%H:%M:%SZ')
            assert resp.json()['publish_date'] == valid_date

    def test_jobs_balance_decreased_when_create_active_job(
            self, company_user_client, job_base_data, company):
        current_jobs_balance = company.customer.balance.jobs_remain
        data = copy.deepcopy(job_base_data)
        data['status'] = enums.JobStatusEnum.ACTIVE.name
        resp = api_requests.create_job(company_user_client, data)
        assert resp.status_code == http.HTTPStatus.CREATED
        company.customer.balance.refresh_from_db()
        assert company.customer.balance.jobs_remain == current_jobs_balance - 1

    def test_jobs_balance_decreased_when_create_delayed_job(
            self, company_user_client, job_base_data, company):
        current_jobs_balance = company.customer.balance.jobs_remain
        data = copy.deepcopy(job_base_data)
        data['status'] = enums.JobStatusEnum.DELAYED.name
        today = utils.date(2019, 1, 28)
        date = utils.date(2019, 1, 29)
        data['publish_date'] = str(date)
        with mock.patch('django.utils.timezone.now', new=lambda: today):
            resp = api_requests.create_job(company_user_client, data)
        assert resp.status_code == http.HTTPStatus.CREATED
        company.customer.balance.refresh_from_db()
        assert company.customer.balance.jobs_remain == current_jobs_balance - 1

    def test_create_job_with_schedule_without_date(
            self, company_user_client, job_base_data):
        data = copy.deepcopy(job_base_data)
        data['status'] = enums.JobStatusEnum.DELAYED.name
        date = utils.date(2018, 10, 1)
        with mock.patch('django.utils.timezone.now', new=lambda: date):
            resp = api_requests.create_job(company_user_client, data)
            assert resp.status_code == http.HTTPStatus.CREATED
            active_status = enums.JobStatusEnum.ACTIVE.name
            assert resp.json()['status'] == active_status
            valid_date = timezone.now().strftime('%Y-%m-%dT%H:%M:%SZ')
            assert resp.json()['publish_date'] == valid_date

    def test_create_job_with_schedule_with_date_today(
            self, company_user_client, job_base_data):
        data = copy.deepcopy(job_base_data)
        data['status'] = enums.JobStatusEnum.DELAYED.name
        date = utils.date(2018, 10, 1)
        data['publish_date'] = str(date)
        with mock.patch('django.utils.timezone.now', new=lambda: date):
            resp = api_requests.create_job(company_user_client, data)
            assert resp.status_code == http.HTTPStatus.CREATED
            active_status = enums.JobStatusEnum.ACTIVE.name
            assert resp.json()['status'] == active_status
            valid_date = timezone.now().strftime('%Y-%m-%dT%H:%M:%SZ')
            assert resp.json()['publish_date'] == valid_date

    def test_create_job_no_opt_skills(
            self, company_user_client, job_base_data):
        data = copy.deepcopy(job_base_data)
        data.pop('optional_skills')
        resp = api_requests.create_job(company_user_client, data)
        assert resp.status_code == http.HTTPStatus.CREATED
        assert resp.json()['optional_skills'] == []

    def test_create_job_with_schedule(
            self, company_user_client, job_base_data):
        data = copy.deepcopy(job_base_data)
        data['status'] = enums.JobStatusEnum.DELAYED.name
        today = utils.date(2018, 10, 1)
        date = utils.date(2018, 10, 2)
        data['publish_date'] = str(date)
        with mock.patch('django.utils.timezone.now', new=lambda: today):
            resp = api_requests.create_job(company_user_client, data)
            assert resp.status_code == http.HTTPStatus.CREATED
            assert resp.json()['status'] == data['status']
            valid_date = date.strftime('%Y-%m-%dT%H:%M:%SZ')
            assert resp.json()['publish_date'] == valid_date

    def test_publish_delayed_jobs(
            self, company_user_client, anonym_client, job_delayed):
        date = timezone.now() + datetime.timedelta(days=1)
        with mock.patch('django.utils.timezone.now', new=lambda: date):
            tasks.publish_jobs.delay()
            resp = api_requests.get_job_unauthorized(
                anonym_client,
                job_delayed['id'])
            assert resp.status_code == http.HTTPStatus.OK

    def test_publish_delayed_job_date_did_not_come(
            self, company_user_client,
            anonym_client, job_delayed):
        with mock.patch(
                'django.utils.timezone.now', return_value=timezone.now()):
            tasks.publish_jobs.delay()
            resp = api_requests.get_job_unauthorized(
                anonym_client,
                job_delayed['id'])
            assert resp.status_code == http.HTTPStatus.NOT_FOUND

    def test_create_job_with_questions(
            self, company_user_client, job_base_data):
        data = copy.deepcopy(job_base_data)
        data['questions'] = [
            {'body': 'question1'},
            {'body': 'question2'}
        ]
        resp = api_requests.create_job(company_user_client, data)
        assert resp.status_code == http.HTTPStatus.CREATED
        assert resp.json()['questions']

    def test_create_job_with_questions_add_to_saved_is_diff_questions(
            self, company_user_client, job_base_data):
        data = copy.deepcopy(job_base_data)
        data['questions'] = [
            {'body': 'question', 'add_to_saved_questions': True}
        ]
        resp = api_requests.create_job(company_user_client, data)
        assert resp.status_code == http.HTTPStatus.CREATED
        job = resp.json()
        assert job['questions'][0]['body'] == data['questions'][0]['body']

        resp = api_requests.get_saved_questions(company_user_client)
        assert resp.status_code == http.HTTPStatus.OK
        question = resp.json()['results'][0]

        # change saved question
        data = {'body': 'new question'}
        resp = api_requests.edit_saved_question(
            company_user_client,
            question['id'],
            data)
        assert resp.status_code == http.HTTPStatus.OK
        saved_question_body = resp.json()['body']
        assert saved_question_body == data['body']

        resp = api_requests.get_job(company_user_client, job['id'])
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['questions'][0]['body'] != saved_question_body

    def test_create_job_with_cover_letter_required_success(
            self, company_user_client, job_base_data):
        data = copy.deepcopy(job_base_data)
        data['is_cover_letter_required'] = True
        resp = api_requests.create_job(company_user_client, data)
        assert resp.status_code == http.HTTPStatus.CREATED
        assert resp.json()['is_cover_letter_required']

    def test_get_job_with_applied_candidate(
            self, company_user_client, job1, apply):
        resp = api_requests.get_job(company_user_client, job1['id'])
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['candidates_count']['all'] == 1
        assert resp.json()['candidates_count']['applied'] == 1

    # TODO (i.bogretsov) added celery worker fixture for correct check
    def test_job_with_closing_date_already_closed(
            self, company_user_client,
            job_base_data, job1, candidate, cand_status_rejected):
        data = copy.deepcopy(job_base_data)
        closing_date = timezone.now() + datetime.timedelta(days=1)
        data['closing_date'] = str(closing_date)
        resp = api_requests.update_job(company_user_client, job1['id'], data)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['closing_date']

        with mock.patch('django.utils.timezone.now', new=lambda: closing_date):
            tasks.close_expired_jobs.delay()
            # check status
            resp = api_requests.get_job(company_user_client, job1['id'])
            assert resp.status_code == http.HTTPStatus.OK
            assert resp.json()['status'] == enums.JobStatusEnum.CLOSED.name
            # check candidate
            resp = api_requests.get_candidate(
                company_user_client, candidate['id'])
            assert resp.status_code == http.HTTPStatus.OK
            assert resp.json()['status']['id'] == cand_status_rejected['id']

    def test_send_job_owner_notifications_about_closing_jobs(
            self, jobs_with_closing_dates, mock_tomorrow, mailoutbox):
        mailoutbox.clear()
        tasks.notify_job_owners_about_closing_date.delay()
        interval = settings.COUNT_OF_DAYS_FOR_SENDING_EMAIL_BEFORE_CLOSING_JOBS
        expected_date = (
            mock_tomorrow.date() + datetime.timedelta(days=interval)
        )
        expected_date = expected_date.strftime(
            settings.DATE_FORMAT_FOR_CLOSING_JOBS_EMAIL_TEMPLATE)
        assert len(mailoutbox) == 2
        for email in mailoutbox:
            assert expected_date in email.subject

    def test_send_job_owner_notifications_about_closing_jobs_no_jobs(
            self, jobs_with_closing_dates, mailoutbox):
        mailoutbox.clear()
        tasks.notify_job_owners_about_closing_date.delay()
        assert len(mailoutbox) == 0

    def test_can_update_job_with_published_date(
            self, company_user_client, job, job_base_data):
        mock_date = timezone.now() + datetime.timedelta(days=1)
        data = job_base_data.copy()
        data['publish_date'] = job['publish_date']
        with mock.patch.object(timezone, 'now', new=lambda: mock_date):
            resp = api_requests.update_job(
                company_user_client,
                job['id'],
                data)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['publish_date'] == job['publish_date']

    def test_job_with_draft_status_does_not_rejected_candidates(
            self, company_user_client, job1,
            candidate, job_base_data, cand_status_rejected):
        data = job_base_data.copy()
        data['status'] = enums.JobStatusEnum.DRAFT.name
        resp = api_requests.update_job(company_user_client, job1['id'], data)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['status'] == data['status']

        resp = api_requests.get_candidate(company_user_client, candidate['id'])
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['status']['id'] != cand_status_rejected['id']

    def test_create_job_success_closing_date_is_none(
            self, company_user_client, job_base_data):
        data = job_base_data.copy()
        data['closing_date'] = None
        resp = api_requests.create_job(company_user_client, data)
        assert resp.status_code == http.HTTPStatus.CREATED

    def test_update_job_success_closing_date_is_none(
            self, company_user_client, job, job_base_data):
        data = job_base_data.copy()
        data['closing_date'] = None
        resp = api_requests.update_job(
            company_user_client,
            job['id'],
            data)
        assert resp.status_code == http.HTTPStatus.OK

    def test_create_draft_job_success_when_no_balance_left(
            self, subscription_basic_package_3,
            company_user_client, job_base_data, company):
        for _ in range(subscription_basic_package_3['balance']['jobs_remain']):
            resp = api_requests.create_job(company_user_client, job_base_data)
            assert resp.status_code == http.HTTPStatus.CREATED
        data = job_base_data.copy()
        data['status'] = enums.JobStatusEnum.DRAFT.name
        resp = api_requests.create_job(company_user_client, data)
        assert resp.status_code == http.HTTPStatus.CREATED

    def test_update_success(self, company_user_client, job, job_base_data):
        data = copy.deepcopy(job_base_data)
        data['title'] = 'update worker'
        resp = api_requests.update_job(
            company_user_client,
            job['id'],
            data)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['title'] == 'update worker'

    @pytest.mark.parametrize(('status',), (
            (enums.JobStatusEnum.DRAFT.name,),
            (enums.JobStatusEnum.CLOSED.name,)
    ))
    def test_jobs_balance_increased_when_update_active_job_status_to_inactive(
            self, status, company_user_client, job, company, job_base_data):
        current_jobs_balance = company.customer.balance.jobs_remain
        data = copy.deepcopy(job_base_data)
        data['status'] = status
        resp = api_requests.update_job(company_user_client, job['id'], data)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['status'] == status
        company.customer.balance.refresh_from_db()
        assert company.customer.balance.jobs_remain == current_jobs_balance + 1

    def test_jobs_balance_decreased_when_update_inactive_job_status_to_active(
            self, company_user_client, job_draft, company, job_base_data):
        current_jobs_balance = company.customer.balance.jobs_remain
        data = copy.deepcopy(job_base_data)
        data['status'] = enums.JobStatusEnum.ACTIVE.name
        resp = api_requests.update_job(
            company_user_client, job_draft['id'], data
        )
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['status'] == enums.JobStatusEnum.ACTIVE.name
        company.customer.balance.refresh_from_db()
        assert company.customer.balance.jobs_remain == current_jobs_balance - 1

    def test_jobs_balance_doesnt_change_when_update_delayed_job_status_to_active(
            self, company_user_client, job_delayed, company, job_base_data):
        current_jobs_balance = company.customer.balance.jobs_remain
        data = copy.deepcopy(job_base_data)
        data['status'] = enums.JobStatusEnum.ACTIVE.name
        resp = api_requests.update_job(
            company_user_client, job_delayed['id'], data
        )
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['status'] == enums.JobStatusEnum.ACTIVE.name
        company.customer.balance.refresh_from_db()
        assert company.customer.balance.jobs_remain == current_jobs_balance

    def test_update_job_questions(
            self, company_user_client, job, job_base_data):
        data = copy.deepcopy(job_base_data)
        data['questions'] = [{
            'body': 'question'
        }]
        resp = api_requests.update_job(
            company_user_client,
            job['id'],
            data)
        assert resp.status_code == http.HTTPStatus.OK
        question = resp.json()['questions'][0]
        assert question['body'] == data['questions'][0]['body']

    def test_update_job_salary_null(
            self, company_user_client, job, job_base_data):
        data = copy.deepcopy(job_base_data)
        data['salary_max'] = None
        data['salary_min'] = None
        resp = api_requests.update_job(
            company_user_client,
            job['id'],
            data)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['salary_max'] is None
        assert resp.json()['salary_min'] is None


class TestJobValidate:

    def test_create_fails_if_skills_intersect(
            self, company_user_client,
            job_base_data, required_skills):
        data = copy.deepcopy(job_base_data)
        data['optional_skills'] = required_skills
        data['required_skills'] = required_skills
        resp = api_requests.create_job(company_user_client, data)
        assert resp.status_code == http.HTTPStatus.BAD_REQUEST

    @pytest.mark.parametrize(('field',), (
        ('salary_max',), ('salary_min',)
    ))
    def test_create_salary_more_than_max_salary(
            self, company_user_client, job_base_data, field):
        job_base_data[field] = settings.MAX_SALARY + 1
        resp = api_requests.create_job(company_user_client, job_base_data)
        emsg = constants.MAX_SALARY_VALUE_ERROR
        validators.validate_error_message(resp, emsg, field)

    def test_create_with_invalid_salaries_fail(
            self, company_user_client, job_base_data):
        data = copy.deepcopy(job_base_data)
        data['salary_max'] = 100
        data['salary_min'] = 1000
        resp = api_requests.create_job(company_user_client, data)
        emsg = constants.MIN_SALARY_MORE_THAN_MAX_SALARY_ERROR
        validators.validate_error_message(resp, emsg)

    @pytest.mark.parametrize(('field',), (
        (
            'location',
        ),
        (
            'title',
        ),
        (
            'position_type',
        ),
        (
            'industry',
        ),
        (
            'description',
        ),
        (
            'status',
        ),
        (
            'required_skills',
        ),
    ))
    def test_create_job_required_fields(
            self, company_user_client, job_base_data, field):
        data = copy.deepcopy(job_base_data)
        data.pop(field)
        resp = api_requests.create_job(company_user_client, data)
        assert resp.status_code == http.HTTPStatus.BAD_REQUEST

    def test_create_job_strict_education(
            self, company_user_client, job_base_data):
        data = copy.deepcopy(job_base_data)
        data.pop('education')
        data['education_strict'] = True
        resp = api_requests.create_job(company_user_client, data)
        emsg = 'This field is required.'
        validators.validate_error_message(resp, emsg, 'education')

    def test_create_and_publish_date_in_past(
            self, company_user_client, job_base_data):
        data = copy.deepcopy(job_base_data)
        data['publish_date'] = str(
            timezone.now() - datetime.timedelta(days=1))
        data['status'] = enums.JobStatusEnum.DELAYED.name
        resp = api_requests.create_job(company_user_client, data)
        emsg = constants.PUBLISH_DATE_IN_PAST_ERROR
        validators.validate_error_message(resp, emsg, 'publish_date')

    def test_create_job_skill_not_exist(
            self, company_user_client, job_base_data):
        data = copy.deepcopy(job_base_data)
        data['optional_skills'] = [9999999]
        resp = api_requests.create_job(
            company_user_client,
            data)
        assert resp.status_code == http.HTTPStatus.BAD_REQUEST

    def test_create_job_more_than_20_required_skills(
            self, company_user_client, job_base_data):
        skills = models.Skill.objects.all()[:21]
        data = copy.deepcopy(job_base_data)
        data['required_skills'] = [s.id for s in skills]
        resp = api_requests.create_job(company_user_client, data)
        emsg = constants.MORE_20_SKILLS_ERROR
        validators.validate_error_message(resp, emsg, 'required_skills')

    def test_create_job_more_than_20_optional_skills(
            self, company_user_client, job_base_data):
        skills = models.Skill.objects.all()[:21]
        data = copy.deepcopy(job_base_data)
        data['optional_skills'] = [s.id for s in skills]
        resp = api_requests.create_job(company_user_client, data)
        emsg = constants.MORE_20_SKILLS_ERROR
        validators.validate_error_message(resp, emsg, 'optional_skills')

    def test_create_job_with_questions_add_to_saved_max_count(
            self, company_user_client, job_base_data,
            saved_question_base_data):

        for _ in range(30):
            data = saved_question_base_data.copy()
            resp = api_requests.create_saved_question(
                company_user_client,
                data)
            assert resp.status_code == http.HTTPStatus.CREATED

        data = copy.deepcopy(job_base_data)
        data['questions'] = [
            {'body': 'question1'},
            {'body': 'question2', 'add_to_saved_questions': True}
        ]
        resp = api_requests.create_job(company_user_client, data)
        emsg = survey_constants.MAX_COUNT_SAVED_QUESTIONS_ERROR
        validators.validate_error_message(resp, emsg, 'questions')

    def test_create_job_with_questions_more_than_ten_questions(
            self, company_user_client, job_base_data):
        data = copy.deepcopy(job_base_data)
        data['questions'] = [{'body': 'question'} for _ in range(11)]
        resp = api_requests.create_job(company_user_client, data)
        emsg = survey_constants.MAX_COUNT_QUESTIONS_IN_SURVEY_ERROR
        validators.validate_error_message(resp, emsg, 'questions')

    def test_create_job_with_questions_invalid_disqualifying_question(
            self, company_user_client, job_base_data):
        data = copy.deepcopy(job_base_data)
        data['questions'] = [
            {
                'body': 'question',
                'disqualifying_answer': 'BOO'
            }
        ]
        resp = api_requests.create_job(company_user_client, data)
        assert resp.status_code == http.HTTPStatus.BAD_REQUEST
        questions = resp.json()['field_errors']['questions']
        assert (questions[0]['disqualifying_answer'][0] ==
                survey_constants.INVALID_DISQUALIFYING_ANSWER)

    def test_create_job_closing_date_in_past(
            self, company_user_client, job_base_data):
        date = timezone.now() - datetime.timedelta(days=1)
        job_base_data['closing_date'] = str(date)
        resp = api_requests.create_job(company_user_client, job_base_data)
        emsg = constants.CLOSING_DATE_IN_THE_PAST_ERROR
        validators.validate_error_message(resp, emsg, 'closing_date')

    def test_create_job_publish_date_great_than_closing_in_past(
            self, company_user_client, job_base_data):
        closing_date = timezone.now()
        publish_date = timezone.now() + datetime.timedelta(days=1)
        job_base_data['closing_date'] = str(closing_date)
        job_base_data['publish_date'] = str(publish_date)
        resp = api_requests.create_job(company_user_client, job_base_data)
        emsg = constants.PUBLISH_DATE_GREAT_THAN_CLOSING_DATE_ERROR
        validators.validate_error_message(resp, emsg)

    def test_create_job_publish_equal_closing_date(
            self, company_user_client, job_base_data):
        closing_date = timezone.now()
        publish_date = timezone.now()
        job_base_data['closing_date'] = str(closing_date)
        job_base_data['publish_date'] = str(publish_date)
        resp = api_requests.create_job(company_user_client, job_base_data)
        emsg = constants.PUBLISH_DATE_GREAT_THAN_CLOSING_DATE_ERROR
        validators.validate_error_message(resp, emsg)

    def test_create_job_with_status_closed(
            self, company_user_client, job_base_data):
        job_base_data['status'] = enums.JobStatusEnum.CLOSED.name
        resp = api_requests.create_job(company_user_client, job_base_data)
        emsg = constants.NOT_VALID_STATUS_FOR_CREATING_JOB
        validators.validate_error_message(resp, emsg, 'status')

    @pytest.mark.parametrize(('job_fixture',), (
        (
            'job_draft',
        ),
        (
            'job_delayed',
        ),
        (
            'job_closed',
        )
    ))
    def test_set_close_status_to_job_not_valid_current_job_status(
            self, request, company_user_client, job_fixture, job_base_data):
        job = request.getfixturevalue(job_fixture)
        job_base_data['status'] = enums.JobStatusEnum.CLOSED.name
        resp = api_requests.update_job(
            company_user_client,
            job['id'],
            job_base_data)
        emsg = constants.NOT_VALID_STATUS_TO_CLOSING_JOB
        validators.validate_error_message(resp, emsg, 'status')

    def test_job_update_can_not_set_publish_date_in_the_past(
            self, company_user_client, job, job_base_data):
        mock_date = timezone.now() + datetime.timedelta(days=1)
        data = job_base_data.copy()
        data['publish_date'] = str(timezone.now() - datetime.timedelta(days=1))
        with mock.patch.object(timezone, 'now', new=lambda: mock_date):
            resp = api_requests.update_job(
                company_user_client,
                job['id'],
                data)
        emsg = constants.PUBLISH_DATE_IN_PAST_ERROR
        validators.validate_error_message(resp, emsg, 'publish_date')

    def test_update_job_skills_intersect(
            self, company_user_client,
            job, job_base_data):
        data = copy.deepcopy(job_base_data)
        data['required_skills'] = job_base_data['optional_skills']
        resp = api_requests.update_job(
            company_user_client,
            job['id'],
            data)
        emsg = constants.SKILLS_INTERSECT_ERROR
        validators.validate_error_message(resp, emsg)

    def test_update_job_invalid_salary(
            self, company_user_client,
            job, job_base_data):
        data = copy.deepcopy(job_base_data)
        data['salary_max'] = 100
        data['salary_min'] = 200
        resp = api_requests.update_job(
            company_user_client,
            job['id'],
            data)
        emsg = constants.MIN_SALARY_MORE_THAN_MAX_SALARY_ERROR
        validators.validate_error_message(resp, emsg)

    def test_create_active_job_fails_when_no_balance_left(
            self, subscription_basic_package_3,
            company_user_client, job_base_data, company):
        for _ in range(subscription_basic_package_3['balance']['jobs_remain']):
            resp = api_requests.create_job(company_user_client, job_base_data)
            assert resp.status_code == http.HTTPStatus.CREATED
        resp = api_requests.create_job(company_user_client, job_base_data)
        emsg = constants.OUT_OF_JOB_ERROR
        validators.validate_error_message(resp, emsg)


class TestJobApiPublic:
    def test_get_job_hides_salary_if_negotiable(
            self, job_seeker_client, company_user_client,
            job_base_data):
        data = copy.deepcopy(job_base_data)
        data['salary_negotiable'] = True
        data['status'] = enums.JobStatusEnum.ACTIVE.name
        resp = api_requests.create_job(company_user_client, data)
        assert resp.status_code == http.HTTPStatus.CREATED
        resp = api_requests.get_job(
            job_seeker_client,
            resp.json()['id'])
        assert resp.status_code == http.HTTPStatus.OK
        assert 'salary_min' not in resp.json()
        assert 'salary_max' not in resp.json()
        assert 'owner' not in resp.json()
        assert 'status' not in resp.json()

    @pytest.mark.parametrize(('job_fixture', 'status'), (
        (
            'job_draft',
            http.HTTPStatus.NOT_FOUND
        ),
        (
            'job',
            http.HTTPStatus.OK
        ),
        (
            'job_delayed',
            http.HTTPStatus.NOT_FOUND
        )
    ))
    def test_job_seeker_cannot_see_not_published_jobs(
            self, request, anonym_client, job_fixture, status):
        job = request.getfixturevalue(job_fixture)
        resp = api_requests.get_job_unauthorized(
            anonym_client,
            job['id'])
        assert resp.status_code == status


class TestRetrieveJobApi:

    def test_retrieve_job_for_company_user(
            self, company_user_client, job_with_questions):
        resp = api_requests.get_job(
            company_user_client,
            job_with_questions['id']
        )
        assert resp.status_code == http.HTTPStatus.OK
        assert (resp.json() ==
                expected.COMPANY_USER_EXPECTED_JOB_DETAILS)

    def test_retrieve_job_for_job_seeker(
            self, job_seeker_client, job_with_questions):
        resp = api_requests.get_job(
            job_seeker_client,
            job_with_questions['id']
        )
        assert resp.status_code == http.HTTPStatus.OK
        assert (resp.json() ==
                expected.JOB_SEEKER_EXPECTED_JOB_DETAILS)


class TestJobViewers:

    @pytest.mark.parametrize(('client', 'count'), (
        (
            'company_user_client',
            0,
        ),
        (
            'job_seeker_client',
            1,
        )
    ))
    def test_job_views_only_job_seeker_add_view_entry(
            self, request, client, job,
            company_user_client, count):
        client = request.getfixturevalue(client)
        resp = api_requests.get_job(
            client,
            job['id'])
        assert resp.status_code == http.HTTPStatus.OK

        resp = api_requests.get_job_list(company_user_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['results'][0]['views_count'] == count

    def test_list_of_jobs_views_count_applies_count(
            self, job_seeker_client, company_user_client,
            job, started_autoapply):
        resp = api_requests.get_job(
            job_seeker_client,
            job['id'])
        assert resp.status_code == http.HTTPStatus.OK

        resp = api_requests.get_job_list(company_user_client)
        assert resp.status_code == http.HTTPStatus.OK
        job = next(j for j in resp.json()['results']
                   if j['views_count'] > 0 and j['applies_count'] > 0)
        assert job['views_count'] == 1
        assert job['applies_count'] == 1

    def test_get_job_viewers(
            self, job_seeker_client, company_user_client,
            job, job_seeker):
        resp = api_requests.get_job(
            job_seeker_client,
            job['id'])
        assert resp.status_code == http.HTTPStatus.OK

        resp = api_requests.get_job_viewers(
            company_user_client,
            job['id'])
        assert resp.status_code == http.HTTPStatus.OK
        data = resp.json()['results'][0]
        assert data['viewer']['id'] == job_seeker.id
        assert data['viewer']['name'] == job_seeker.user.get_full_name()

    @pytest.mark.parametrize(('client', 'status'), (
        (
            'anonym_client',
            http.HTTPStatus.UNAUTHORIZED
        ),
        (
            'job_seeker_client',
            http.HTTPStatus.FORBIDDEN
        ),
        (
            'company_user_client',
            http.HTTPStatus.OK
        ),
        (
            'company_2_user_client',
            http.HTTPStatus.NOT_FOUND
        ),
    ))
    def test_get_job_viewers_permissions(
            self, request, job_seeker_client,
            job, job_seeker, client, status):
        resp = api_requests.get_job(
            job_seeker_client,
            job['id'])
        assert resp.status_code == http.HTTPStatus.OK

        client = request.getfixturevalue(client)
        resp = api_requests.get_job_viewers(client, job['id'])
        assert resp.status_code == status


class TestSoftDeleteJobApi:

    @pytest.mark.usefixtures(
        'job', 'company_deleted_job')
    def test_job_seeker_cant_see_deleted_job_in_job_list(
            self, job_seeker_client):
        resp = api_requests.get_job_list(
            job_seeker_client
        )
        assert resp.status_code == http.HTTPStatus.OK
        assert len(resp.json()['results']) == 1

    def test_job_seeker_cant_see_deleted_job_details(
            self, job_seeker_client, company_deleted_job):
        resp = api_requests.get_job(
            job_seeker_client, company_deleted_job['id']
        )
        assert resp.status_code == http.HTTPStatus.NOT_FOUND

    def test_job_seeker_can_see_deleted_job_title_if_he_has_been_applied_for_this_job(
            self, company_user_client, job_seeker_client, job1):
        resp = api_requests.apply_to_job(
            job_seeker_client, data={'job': job1['id']}
        )
        assert resp.status_code == http.HTTPStatus.CREATED
        resp = api_requests.delete_job(company_user_client, job1['id'])
        assert resp.status_code == http.HTTPStatus.NO_CONTENT
        resp = api_requests.get_applied_jobs(job_seeker_client)
        assert resp.status_code == http.HTTPStatus.OK
        assert len(resp.json()['results']) == 1
        job = resp.json()['results'][0]
        assert job == expected.DELETED_JOB_EXPECTED_DETAILS

    def test_job_seeker_can_see_deleted_job_title_if_job_was_saved(
            self, company_user_client, job_seeker, job_seeker_client,
            job):
        resp = api_requests.add_remove_to_saved(
            job_seeker_client,
            job_seeker.id,
            data={
                'add': True,
                'job': job['id']
            }
        )
        assert resp.status_code == http.HTTPStatus.OK
        resp = api_requests.delete_job(company_user_client, job['id'])
        assert resp.status_code == http.HTTPStatus.NO_CONTENT
        resp = api_requests.get_saved_jobs(
            job_seeker_client, job_seeker.id
        )
        assert resp.status_code == http.HTTPStatus.OK
        assert len(resp.json()['results']) == 1
        job = resp.json()['results'][0]
        assert job == expected.DELETED_JOB_EXPECTED_DETAILS

    def test_soft_delete_success(self, company_user_client, job):
        resp = api_requests.delete_job(company_user_client, job['id'])
        assert resp.status_code == http.HTTPStatus.NO_CONTENT
        assert models.Job.objects.get(id=job['id']).is_deleted
        assert not models.Job.objects.get(id=job['id']).status

    def test_company_user_cant_delete_job_that_doesnt_belong_his_company(
            self, company_user_client, company_2_job):
        resp = api_requests.delete_job(
            company_user_client, company_2_job['id']
        )
        assert resp.status_code == http.HTTPStatus.NOT_FOUND
        assert not models.Job.objects.get(id=company_2_job['id']).is_deleted

    def test_soft_delete_jobs_list(self, company_user_client, jobs):
        job_ids = [j['id'] for j in jobs]
        resp = api_requests.delete_job_list(
            company_user_client, data={'jobs': job_ids}
        )
        assert resp.status_code == http.HTTPStatus.NO_CONTENT
        for job in models.Job.objects.filter(id__in=job_ids):
            assert job.is_deleted
            assert not job.status

    def test_company_user_cant_delete_job_list_that_doesnt_belong_his_company(
            self, company_2_user_client, jobs):
        job_ids = [j['id'] for j in jobs]
        resp = api_requests.delete_job_list(
            company_2_user_client, data={'jobs': job_ids}
        )
        assert resp.status_code == http.HTTPStatus.FORBIDDEN

    def test_company_user_cant_delete_already_deleted_job(
            self, company_user_client, company_deleted_job):
        resp = api_requests.delete_job(
            company_user_client, company_deleted_job['id']
        )
        emsg = constants.JOB_ALREADY_DELETED
        validators.validate_error_message(resp, emsg)

    def test_delete_jobs_candidates_are_rejected(
            self, company_user_client, job1, candidate, cand_status_rejected):
        resp = api_requests.delete_job(company_user_client, job1['id'])
        assert resp.status_code == http.HTTPStatus.NO_CONTENT
        resp = api_requests.get_candidate(company_user_client, candidate['id'])
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['status']['id'] == cand_status_rejected['id']


class TestRestoreDeletedJobAPI:

    def test_restore_deleted_job_success(
            self, company_user_client, company_deleted_job):
        resp = api_requests.restore_job(
            company_user_client, company_deleted_job['id'])
        assert resp.status_code == http.HTTPStatus.OK
        assert not resp.json()['is_deleted']
        assert resp.json()['status'] == enums.JobStatusEnum.DRAFT.name

    def test_restore_nondeleted_job_fails(
            self, company_user_client, job):
        resp = api_requests.restore_job(
            company_user_client, job['id'])
        emsg = constants.JOB_IS_NOT_DELETED
        validators.validate_error_message(resp, emsg)

    def test_company_user_cant_restore_not_own_job(
            self, company_2_user_client, company_deleted_job):
        resp = api_requests.restore_job(
            company_2_user_client, company_deleted_job['id'])
        assert resp.status_code == http.HTTPStatus.NOT_FOUND


class TestHardDeleteJobAPI:

    def test_company_user_cant_see_inactive_job_in_job_list(
            self, company_user_client, company_inactive_job_id):
        resp = api_requests.get_job_list(
            company_user_client
        )
        assert resp.status_code == http.HTTPStatus.OK
        assert not len(resp.json()['results'])

    def test_company_user_cant_see_inactive_job_details(
            self, company_user_client, company_inactive_job_id):
        resp = api_requests.get_job(
            company_user_client, company_inactive_job_id
        )
        assert resp.status_code == http.HTTPStatus.NOT_FOUND

    def test_job_seeker_cant_see_inactive_job_in_job_list(
            self, job_seeker_client, company_inactive_job_id):
        resp = api_requests.get_job_list(
            job_seeker_client
        )
        assert resp.status_code == http.HTTPStatus.OK
        assert not len(resp.json()['results'])

    def test_job_seeker_cant_see_inactive_job_details(
            self, job_seeker_client, company_inactive_job_id):
        resp = api_requests.get_job(
            job_seeker_client, company_inactive_job_id
        )
        assert resp.status_code == http.HTTPStatus.NOT_FOUND


class TestJobApiPermissions:

    @pytest.mark.parametrize(('client', 'status'), (
        (
            'anonym_client',
            http.HTTPStatus.UNAUTHORIZED
        ),
        (
            'job_seeker_client',
            http.HTTPStatus.OK
        ),
        (
            'company_user_client',
            http.HTTPStatus.OK
        ),
    ))
    def test_job_list(self, request, client, status, job):
        client = request.getfixturevalue(client)
        resp = api_requests.get_job_list(client)
        assert resp.status_code == status

    @pytest.mark.parametrize(('client', 'count'), (
        (
            'company_user_client',
            1
        ),
        (
            'company_2_user_client',
            0
        ),
    ))
    def test_company_user_see_only_his_company_jobs(
            self, request, client, count, job):
        client = request.getfixturevalue(client)
        resp = api_requests.get_job_list(client)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == count

    @pytest.mark.parametrize(('client', 'status'), (
        (
            'anonym_client',
            http.HTTPStatus.UNAUTHORIZED
        ),
        (
            'job_seeker_client',
            http.HTTPStatus.FORBIDDEN
        ),
        (
            'company_user_client',
            http.HTTPStatus.CREATED
        ),
    ))
    def test_create_job(self, request, client, status, job_base_data):
        client = request.getfixturevalue(client)
        resp = api_requests.create_job(client, job_base_data)
        assert resp.status_code == status

    @pytest.mark.parametrize(('client', 'status'), (
        (
            'anonym_client',
            http.HTTPStatus.UNAUTHORIZED
        ),
        (
            'job_seeker_client',
            http.HTTPStatus.OK
        ),
        (
            'company_user_client',
            http.HTTPStatus.OK
        ),
        (
            'company_2_user_client',
            http.HTTPStatus.NOT_FOUND
        ),
    ))
    def test_get_job_details(
            self, request, client, status, job):
        client = request.getfixturevalue(client)
        resp = api_requests.get_job(client, job['id'])
        assert resp.status_code == status

    @pytest.mark.parametrize(('client', 'status'), (
        (
            'anonym_client',
            http.HTTPStatus.UNAUTHORIZED
        ),
        (
            'job_seeker_client',
            http.HTTPStatus.FORBIDDEN
        ),
        (
            'company_user_client',
            http.HTTPStatus.OK
        ),
        (
            'company_2_user_client',
            http.HTTPStatus.NOT_FOUND
        ),
    ))
    def test_update_job(
            self, request, client, status, job, job_base_data):
        client = request.getfixturevalue(client)
        data = copy.deepcopy(job_base_data)
        data['fail'] = 'fail'
        resp = api_requests.update_job(
            client,
            job['id'],
            data)
        assert resp.status_code == status


class TestShareJobViaEmail:

    def test_share_job_success(self, job_seeker_client, job, mailoutbox):
        mailoutbox.clear()
        email_to = 'valid@email.com'
        resp = api_requests.share_job(
            job_seeker_client,
            job_id=job['id'],
            data={
                'email': email_to,
                'url': 'http://link-to-job.com/job'
            }
        )
        assert resp.status_code == http.HTTPStatus.OK
        assert len(mailoutbox) == 1
        assert mailoutbox[0].to[0] == email_to

    @pytest.mark.parametrize(('field', 'data'), (
            (
                    'email',
                    {
                        'email': 'invalidemail.com',
                        'url': 'http://link-to-job.com/job'
                    },
            ),
            (
                    'url',
                    {
                        'email': 'valid@email.com',
                        'url': 'invalidlink'
                    },
            )
    ))
    def test_share_job_fails_with_invalid_data(
            self, job_seeker_client, job, field, data, mailoutbox):
        mailoutbox.clear()
        resp = api_requests.share_job(
            job_seeker_client,
            job_id=job['id'],
            data=data
        )
        assert resp.status_code == http.HTTPStatus.BAD_REQUEST
        assert resp.json()['field_errors'][field]
        assert not len(mailoutbox)

    def test_share_job_fails_with_invalid_url(
            self, job_seeker_client, job, mailoutbox
    ):
        mailoutbox.clear()
        resp = api_requests.share_job(
            job_seeker_client,
            job_id=job['id'],
            data={
                'email': 'valid@email.com',
                'url': 'http://invalid-link-to-job'
            }
        )
        assert resp.status_code == http.HTTPStatus.BAD_REQUEST
        assert resp.json()['field_errors']['url']
        assert not len(mailoutbox)
