import http

import pytest

from apply import constants
from apply.models import Apply
from job.models import Job
from leet import enums
from tests import api_requests
from tests import validators
from tests import utils


class TestManualApplyApi:
    def test_create_success(
            self, job_seeker_client, job_seeker, job1):
        resp = api_requests.apply_to_job(
            job_seeker_client, data={'job': job1['id']}
        )
        assert resp.status_code == http.HTTPStatus.CREATED
        assert resp.json()['status'] == enums.ApplyStatusEnum.APPLIED.name
        assert resp.json()['job'] == job1['id']
        assert resp.json()['owner'] == job_seeker.id
        assert resp.json()['applied_at'] == utils.Any(str)

    def test_create_success_if_user_has_gt_clearance(
            self, job_seeker_client, job_seeker, job1):
        job_seeker.clearance = enums.ClearanceTypesEnum.TOP_SECRET.name
        job_seeker.save()
        resp = api_requests.apply_to_job(
            job_seeker_client, data={'job': job1['id']}
        )
        assert resp.status_code == http.HTTPStatus.CREATED
        assert resp.json()['status'] == enums.ApplyStatusEnum.APPLIED.name
        assert resp.json()['job'] == job1['id']
        assert resp.json()['owner'] == job_seeker.id
        assert resp.json()['applied_at'] == utils.Any(str)

    def test_manual_apply_fails_if_clearance_doesnt_match(
            self, job_seeker_client, job_seeker, job1):
        job_seeker.clearance = enums.ClearanceTypesEnum.UNCLASSIFIED.name
        job_seeker.save()
        resp = api_requests.apply_to_job(
            job_seeker_client, data={'job': job1['id']}
        )
        validators.validate_error_message(
            resp,
            constants.CLEARANCE_DOESNT_MATCH_ERROR)

    def test_manual_apply_fails_if_job_has_already_applied(
            self, job_seeker_client, job_seeker, job1):
        Apply.objects.create(owner=job_seeker, job_id=job1['id'])
        resp = api_requests.apply_to_job(
            job_seeker_client, data={'job': job1['id']}
        )
        validators.validate_error_message(
            resp,
            constants.YOU_CANT_APPLY_FOR_ALREADY_APPLIED_JOB_ERROR)

    def test_manual_apply_fails_if_profile_hidded(
            self, job_seeker_client, job_seeker, job1):
        job_seeker.is_public = False
        job_seeker.save()
        resp = api_requests.apply_to_job(
            job_seeker_client, data={'job': job1['id']}
        )
        validators.validate_error_message(
            resp,
            constants.PROFILE_ISNT_PUBLIC_ERROR,
            error_code=http.HTTPStatus.FORBIDDEN)

    def test_manual_apply_fails_if_questionnaire_isnt_answered(
            self, job_seeker_client, job_with_questions):
        resp = api_requests.apply_to_job(
            job_seeker_client, data={'job': job_with_questions['id']}
        )
        validators.validate_error_message(
            resp,
            constants.ANSWER_QUESTIONNAIRE_BEFORE_APPLYING_ERROR)

    def test_manual_apply_fails_if_required_skills_not_match(
            self, job_seeker_client, job1):
        job = Job.objects.get(id=job1['id'])
        job.manual_apply_strict_required_skills_matching = True
        job.save()
        resp = api_requests.apply_to_job(
            job_seeker_client, data={'job': job1['id']}
        )
        validators.validate_error_message(
            resp,
            constants.REQUIRED_SKILLS_MATCH_ERROR)


    def test_manual_apply_success_if_required_skills_match(
            self, job_seeker_client, job_seeker, job3):
        job = Job.objects.get(id=job3['id'])
        job.manual_apply_strict_required_skills_matching = True
        job.save()
        resp = api_requests.apply_to_job(
            job_seeker_client, data={'job': job3['id']}
        )
        assert resp.status_code == http.HTTPStatus.CREATED
        assert resp.json()['status'] == enums.ApplyStatusEnum.APPLIED.name
        assert resp.json()['job'] == job3['id']
        assert resp.json()['owner'] == job_seeker.id
        assert resp.json()['applied_at'] == utils.Any(str)

    @pytest.mark.parametrize(('answers_fixture',), (
            ('job_survey_answers',),
            ('job_survey_only_required_answers',),
    ))
    def test_manual_apply_success_if_questionaire_answered(
            self, answers_fixture, job_seeker_client, job_with_questions,
            job_seeker, request):
        request.getfixturevalue(answers_fixture)
        resp = api_requests.apply_to_job(
            job_seeker_client, data={'job': job_with_questions['id']}
        )
        assert resp.status_code == http.HTTPStatus.CREATED
        assert resp.json()['status'] == enums.ApplyStatusEnum.APPLIED.name
        assert resp.json()['job'] == job_with_questions['id']
        assert resp.json()['owner'] == job_seeker.id
        assert resp.json()['applied_at'] == utils.Any(str)

    @pytest.mark.parametrize(('client', 'status'), (
        (
            'anonym_client',
            http.HTTPStatus.UNAUTHORIZED,
        ),
        (
            'job_seeker_client',
            http.HTTPStatus.CREATED,
        ),
        (
            'company_user_client',
            http.HTTPStatus.FORBIDDEN,
        ),
    ))
    def test_manual_apply_permissions(
            self, request, client, status, job1):
        client = request.getfixturevalue(client)
        resp = api_requests.apply_to_job(
            client,
            data={'job': job1['id']}
        )
        assert resp.status_code == status
