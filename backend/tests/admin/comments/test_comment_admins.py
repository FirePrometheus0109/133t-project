import pytest

from tests.admin.comments import expected


class TestCommentsAdmin:

    @pytest.mark.parametrize(('comments_admin_site', 'exp'), (
            (
                'job_comments_admin',
                expected.JOB_COMMENTS_FIELDS,
            ),
            (
                'job_seeker_comments_admin',
                expected.JOB_SEEKER_COMMENTS_FIELDS,
            ),
    ))
    def test_comment_creation_form_fields(
            self, request, comments_admin_site, exp, admin_request):
        site = request.getfixturevalue(comments_admin_site)
        fields = site.get_fields(admin_request)
        assert exp == fields
