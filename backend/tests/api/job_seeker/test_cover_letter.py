import http

import pytest

from job_seeker import constants
from job_seeker import models
from tests import api_requests
from tests import validators
from tests.api.job_seeker import expected


class TestCoverLetterApi:

    def test_create_cover_letter_success(
            self, job_seeker_client, job_seeker, cover_letter_data):
        resp = api_requests.create_cover_letter(
            job_seeker_client,
            job_seeker_id=job_seeker.id,
            data=cover_letter_data
        )
        assert resp.status_code == http.HTTPStatus.CREATED
        result = resp.json()
        assert result == expected.EXPECTED_COVER_LETTER

    @pytest.mark.parametrize(('field', 'value'), (
            ('title', 'new title'),
            ('body', 'new body'),
            ('is_default', True)
    ))
    def test_update_cover_letter_success(
            self, field, value, job_seeker_client, job_seeker,
            cover_letter, cover_letter_data):
        update_cover_letter_data = cover_letter_data.copy()
        update_cover_letter_data[field] = value
        resp = api_requests.update_cover_letter(
            job_seeker_client,
            job_seeker_id=job_seeker.id,
            pk=cover_letter['id'],
            data=update_cover_letter_data
        )
        assert resp.status_code == http.HTTPStatus.OK
        result = resp.json()
        assert result[field] == value

    def test_get_cover_letters_success(
            self, job_seeker_client, job_seeker, cover_letter):
        resp = api_requests.get_cover_letters(job_seeker_client, job_seeker.id)
        assert resp.status_code == http.HTTPStatus.OK
        assert len(resp.json()['results']) == 1

    def test_delete_cover_letters_success(
            self, job_seeker_client, job_seeker, cover_letter):
        resp = api_requests.delete_cover_letter(
            job_seeker_client, job_seeker.id, cover_letter['id']
        )
        assert resp.status_code == http.HTTPStatus.NO_CONTENT

    def test_create_cover_letter_with_existing_title_fails(
            self, job_seeker_client, job_seeker, cover_letter,
            cover_letter_data):
        resp = api_requests.create_cover_letter(
            job_seeker_client,
            job_seeker_id=job_seeker.id,
            data=cover_letter_data
        )
        emsg = constants.COVER_LETTER_TITLE_SHOULD_BE_UNIQUE
        validators.validate_error_message(resp, emsg, 'title')

    def test_only_one_default_cover_letter_can_exist(
            self, job_seeker_client, job_seeker, cover_letter_data):
        data = cover_letter_data.copy()
        data['is_default'] = True
        resp = api_requests.create_cover_letter(
            job_seeker_client,
            job_seeker_id=job_seeker.id,
            data=data
        )
        assert resp.status_code == http.HTTPStatus.CREATED
        default_cover_letter = models.CoverLetter.objects.get(id=resp.json()['id'])
        assert default_cover_letter.is_default
        data['title'] = 'New title'
        resp = api_requests.create_cover_letter(
            job_seeker_client,
            job_seeker_id=job_seeker.id,
            data=data
        )
        assert resp.status_code == http.HTTPStatus.CREATED
        new_default_cover_letter = models.CoverLetter.objects.get(id=resp.json()['id'])
        assert new_default_cover_letter.is_default
        default_cover_letter.refresh_from_db()
        assert not default_cover_letter.is_default

    @pytest.mark.usefixtures('cover_letters')
    def test_maximum_cover_letter_number(
            self, job_seeker_client, job_seeker, cover_letter_data):
        data = cover_letter_data.copy()
        resp = api_requests.create_cover_letter(
            job_seeker_client,
            job_seeker_id=job_seeker.id,
            data=data
        )
        emsg = constants.MAXIMUM_OF_COVER_LETTER_ENTRIES_ERROR
        validators.validate_error_message(resp, emsg)
