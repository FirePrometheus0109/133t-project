import http

from django.conf import settings
import pytest

from candidate import models
from tests import api_requests
from tests import constants
from tests import utils
from tests.api.candidate import expected


class TestExportCandidatesToCsv:

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
            http.HTTPStatus.OK),
        )
    )
    def test_get_csv(self, request, client, status, job1):
        client = request.getfixturevalue(client)
        query_params = {'candidates': job1['id']}
        resp = api_requests.export_candidates_to_csv(client, query_params)
        assert resp.status_code == status

    def test_get_csv_data(self, company_user_client, candidate, educations,
                          certifications, job_experience, candidate_good_rate):
        data = {'candidates': [candidate['id']]}
        resp = api_requests.export_candidates_to_csv(company_user_client, data)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp._headers.get('content-type')[
                   1] == constants.CSV_EXPECTED_CONTENT_TYPE

        headers, body = utils.get_csv_response_data(resp)
        candidate_row = body.pop(0)

        assert set(headers) == expected.CSV_EXPECTED_HEADERS

        candidate_obj = models.Candidate.objects.get(id=candidate['id'])
        location = '{} ({})'.format(
            candidate_obj.job_seeker.address.city.name,
            candidate_obj.job_seeker.address.city.state.abbreviation
        )
        industries = ','.join(
            [industry.name for industry in candidate_obj.job_seeker.industries.all()]
        )
        skills = ','.join(
            [skill.name for skill in candidate_obj.job_seeker.skills.all()]
        )
        educations_formatted = ','.join([
            'education1 study 2018',
            'education2 study',
            'education3 study 2018',
            'certification1 study 2018',
            'certification2 study',
            'certification3 study 2018',
        ])
        experience_formatted = 'title at job seeker company 2018 - Now'
        assert candidate_obj.job_seeker.user.first_name in candidate_row
        assert candidate_obj.job_seeker.user.last_name in candidate_row
        assert candidate_obj.job.title in candidate_row
        assert candidate_obj.apply.applied_at.strftime(
            settings.DEFAULT_SERVER_DATE_FORMAT) in candidate_row
        assert location in candidate_row
        assert candidate_obj.job_seeker.modified_at.strftime(
            settings.DEFAULT_SERVER_DATE_FORMAT) in candidate_row
        assert candidate_obj.job_seeker.user.email in candidate_row
        assert candidate_obj.job_seeker.phone in candidate_row
        assert candidate_obj.job_seeker.address.address in candidate_row
        assert industries in candidate_row
        assert candidate_obj.job_seeker.get_position_type_display() in candidate_row
        assert candidate_obj.job_seeker.get_education_display() in candidate_row
        assert candidate_obj.job_seeker.get_experience_display() in candidate_row
        assert candidate_obj.job_seeker.get_travel_display() in candidate_row
        assert str(candidate_obj.job_seeker.salary_max) in candidate_row
        assert str(candidate_obj.job_seeker.salary_min) in candidate_row
        assert candidate_obj.job_seeker.get_clearance_display() in candidate_row
        assert candidate_obj.job_seeker.get_benefits_display() in candidate_row
        assert skills in candidate_row
        assert educations_formatted in candidate_row
        assert experience_formatted in candidate_row
        assert candidate_obj.status.name in candidate_row
        assert candidate_obj.rating.get_rating_display() in candidate_row
