import http

import pytest

from leet import constants
from tests import api_requests
from tests import validators


class TestUploadPhotoApi:

    @pytest.mark.parametrize(('fixture_file', 'exp_extension'), (
            ('photo_bmp', 'bmp'),
            ('photo_gif', 'gif'),
            ('photo_jpg', 'jpg'),
            ('photo_png', 'png'),
            ('photo_tiff', 'tiff'),
    ))
    def test_upload_photo_different_extensions(
            self, request, photo_data, fixture_file,
            job_seeker_client, job_seeker, exp_extension):
        fixture_file = request.getfixturevalue(fixture_file)
        photo_data['photo'] = fixture_file
        resp = api_requests.upload_photo(
            job_seeker_client, job_seeker.id, photo_data)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['photo']['original'].endswith(exp_extension)

    def test_upload_photo_fake_extension(
            self, photo_data, photo_wrong_extension,
            job_seeker_client, job_seeker):
        photo_data['photo'] = photo_wrong_extension
        resp = api_requests.upload_photo(
            job_seeker_client, job_seeker.id, photo_data)
        emsg = constants.NOT_VALID_PHOTO_EXTENSION_ERROR
        validators.validate_error_message(resp, emsg, field='photo')


    def test_upload_photo_big_file(
            self, photo_data, job_seeker_client, job_seeker):
        old_max_file_size = constants.PHOTO_MAX_SIZE_MB
        constants.PHOTO_MAX_SIZE_MB = 0
        resp = api_requests.upload_photo(
            job_seeker_client, job_seeker.id, photo_data)
        emsg = constants.PHOTO_FILE_SIZE_ERROR
        validators.validate_error_message(resp, emsg, field='photo')
        constants.PHOTO_MAX_SIZE_MB = old_max_file_size
