import http

import pytest

from job_seeker import constants
from job_seeker import models
from tests import api_requests
from tests import validators
from tests.api.job_seeker import expected


class TestDocumentApi:

    def test_add_document(
            self, job_seeker, job_seeker_client,
            document_data):
        resp = api_requests.add_document(
            job_seeker_client, job_seeker.id, document_data)
        assert resp.status_code == http.HTTPStatus.CREATED
        assert resp.json() == expected.EXPECTED_JOB_DOCUMENT

    def test_get_list_document(
            self, job_seeker, job_seeker_client, document):
        resp = api_requests.get_document(
            job_seeker_client,
            job_seeker.id)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['results']
        assert resp.json()['count'] == 1

    def test_get_document(
            self, job_seeker, job_seeker_client, document):
        resp = api_requests.get_document_details(
            job_seeker_client,
            job_seeker.id,
            document['id'])
        assert resp.status_code == http.HTTPStatus.OK

    def test_delete_document(
            self, job_seeker, job_seeker_client,
            document):
        resp = api_requests.delete_document(
            job_seeker_client,
            job_seeker.id,
            document['id']
        )
        assert resp.status_code == http.HTTPStatus.NO_CONTENT
        assert not models.Document.objects.exists()

    def test_cant_delete_not_owner_document(
            self, job_seeker, job_seeker_2, job_seeker_client,
            document):
        document_obj = models.Document.objects.get(id=document['id'])
        document_obj.owner = job_seeker_2
        document_obj.save()
        resp = api_requests.delete_document(
            job_seeker_client,
            job_seeker_2.id,
            document['id']
        )
        assert resp.status_code == 403
        assert resp.json() == {'errors': ['You do not have permission to perform this action.']}

    def test_cant_get_not_owner_document(
            self, job_seeker, job_seeker_2, job_seeker_client,
            document):
        document_obj = models.Document.objects.get(id=document['id'])
        document_obj.owner = job_seeker_2
        document_obj.save()
        resp = api_requests.delete_document(
            job_seeker_client,
            job_seeker_2.id,
            document['id']
        )
        assert resp.status_code == 403
        assert resp.json() == {'errors': ['You do not have permission to perform this action.']}

    def test_cant_add_not_owner_document(
            self, job_seeker, job_seeker_2, job_seeker_client,
            document_data):
        resp = api_requests.add_document(
            job_seeker_client, job_seeker_2.id, document_data)
        assert resp.json() == {'errors': ['You do not have permission to perform this action.']}

    @pytest.mark.parametrize(('fixture_file', 'exp_extension'), (
            ('document_doc', 'doc'),
            ('document_docx', 'docx'),
            ('document_rtf', 'rtf'),
            ('document_pdf', 'pdf'),
            ('document_txt', 'txt'),
            ('document_odt', 'odt'),
    ))
    def test_add_document_different_extensions(
            self, request, document_data, fixture_file,
            job_seeker_client, job_seeker, exp_extension):
        fixture_file = request.getfixturevalue(fixture_file)
        document_data['file'] = fixture_file
        resp = api_requests.add_document(
            job_seeker_client, job_seeker.id, document_data)
        assert resp.status_code == http.HTTPStatus.CREATED
        assert resp.json()['extension'] == exp_extension

class TestDocumentValidate:

    def test_add_document_required_fields_errors(
            self, job_seeker, job_seeker_client,
            document_data):
        data = document_data.copy()
        data.pop('file')
        resp = api_requests.add_document(
            job_seeker_client, job_seeker.id, data)
        assert resp.status_code == http.HTTPStatus.BAD_REQUEST

    def test_add_document_max_10_entries(
            self, job_seeker, job_seeker_client,
            document_data):
        for _ in range(10):
            resp = api_requests.add_document(
                job_seeker_client, job_seeker.id, document_data)
            document_data['file'].seek(0)
            assert resp.status_code == http.HTTPStatus.CREATED

        resp = api_requests.add_document(
            job_seeker_client, job_seeker.id, document_data)
        emsg = constants.MAXIMUM_OF_DOCUMENTS_ERROR
        validators.validate_error_message(resp, emsg)

    def test_add_document_fake_extension(
            self, document_data, document_wrong_extension,
            job_seeker_client, job_seeker):
        document_data['file'] = document_wrong_extension
        resp = api_requests.add_document(
            job_seeker_client, job_seeker.id, document_data)
        emsg = constants.NOT_VALID_DOCUMENT_EXTENSION_ERROR
        validators.validate_error_message(resp, emsg)

    def test_add_document_big_file(
            self, document_data, job_seeker_client, job_seeker):
        old_max_file_size = constants.DOCUMENT_MAX_FILE_SIZE_MB
        constants.DOCUMENT_MAX_FILE_SIZE_MB = 0
        resp = api_requests.add_document(
            job_seeker_client, job_seeker.id, document_data)
        emsg = constants.DOCUMENT_FILE_SIZE_ERROR
        validators.validate_error_message(resp, emsg)
        constants.DOCUMENT_MAX_FILE_SIZE_MB = old_max_file_size

class TestJobExperiencePermissions:

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
        (
            'job_seeker_2_client',
            http.HTTPStatus.FORBIDDEN,
        )
    ))
    def test_create_job_experience(
            self, request, client, status, job_experience_data, job_seeker):
        client = request.getfixturevalue(client)
        resp = api_requests.add_job_experience(
            client,
            job_seeker.id,
            job_experience_data)
        assert resp.status_code == status

    @pytest.mark.parametrize(('client', 'status'), (
        (
            'anonym_client',
            http.HTTPStatus.UNAUTHORIZED,
        ),
        (
            'job_seeker_client',
            http.HTTPStatus.OK,
        ),
        (
            'company_user_client',
            http.HTTPStatus.OK,
        ),
        (
            'job_seeker_2_client',
            http.HTTPStatus.FORBIDDEN,
        )
    ))
    def test_get_job_experience_details(
            self, request, client, status, job_seeker, job_experience):
        client = request.getfixturevalue(client)
        resp = api_requests.get_job_experience_details(
            client,
            job_seeker.id,
            job_experience['id'])
        assert resp.status_code == status


    @pytest.mark.parametrize(('client', 'status'), (
        (
            'anonym_client',
            http.HTTPStatus.UNAUTHORIZED,
        ),
        (
            'job_seeker_client',
            http.HTTPStatus.OK,
        ),
        (
            'company_user_client',
            http.HTTPStatus.OK,
        ),
        (
            'job_seeker_2_client',
            http.HTTPStatus.FORBIDDEN,
        )
    ))
    def test_get_list_job_experience(
            self, request, client, status, job_seeker):
        client = request.getfixturevalue(client)
        resp = api_requests.get_job_experience(client, job_seeker.id)
        assert resp.status_code == status
