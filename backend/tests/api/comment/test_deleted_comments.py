import http

import pytest

from tests import api_requests
from tests.factories import comment as comment_factory


class TestDeletedComments:

    @pytest.mark.parametrize(('create_comment', 'get_comment'), (
            (
                    comment_factory.create_job_comment,
                    api_requests.get_job_comment
            ),
            (
                    comment_factory.create_job_seeker_comment,
                    api_requests.get_job_seeker_comment
            )
    ))
    def test_company_user_cant_view_deleted_comment(
            self, create_comment, get_comment,
            company_user, company_user_client):
        comment = create_comment(company_user)
        comment.is_removed = True
        comment.save()
        resp = get_comment(company_user_client, comment.id)
        assert resp.status_code == http.HTTPStatus.NOT_FOUND
