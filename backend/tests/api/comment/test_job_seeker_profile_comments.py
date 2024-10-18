import http
import pytest

from job_seeker.models import JobSeeker
from tests.factories.comment import create_job_seeker_comment
from tests import api_requests, utils


DEFAULT_COMMENT_DATA = {'title': 'what', 'comment': 'ever'}


class TestCreateJobSeekerComment:
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
    def test_create_job_seeker_comment(self, request, job_seeker, client,
                                       status):
        client = request.getfixturevalue(client)
        DEFAULT_COMMENT_DATA.update({'source': job_seeker.id})
        resp = api_requests.create_job_seeker_comment(client,
                                                      DEFAULT_COMMENT_DATA)
        assert resp.status_code == status

    @pytest.mark.parametrize(('client',), (
            (
                'company_user_client',
            ),
            (
                'company_user_2_client',
            ),
            (
                'company_2_user_client',
            ),
    ))
    def test_any_company_user_cancreate_job_seeker_comment(
            self, request, job_seeker, client):
        client = request.getfixturevalue(client)
        DEFAULT_COMMENT_DATA.update({'source': job_seeker.id})
        resp = api_requests.create_job_seeker_comment(client,
                                                      DEFAULT_COMMENT_DATA)
        assert resp.status_code == http.HTTPStatus.CREATED

    @pytest.mark.parametrize(('title', 'comment'), (
            (
                'cool title',
                'not less cool comment'
            ),
            (
                'foo',
                'bar'
            ),
            (
                'my fantasy',
                'is over'
            ),
    ))
    def test_job_seeker_comment_correct_data(self, job_seeker, title, comment,
                                             company_user_client):
        data = {
            'source': job_seeker.id,
            'title': title,
            'comment': comment
        }
        resp = api_requests.create_job_seeker_comment(company_user_client,
                                                      data)
        assert resp.status_code == http.HTTPStatus.CREATED
        response_data = resp.json()
        assert response_data['title'] == data['title']
        assert response_data['comment'] == data['comment']

    def test_create_job_seeker_comment_without_source(self,
                                                      company_user_client):
        resp = api_requests.create_job_seeker_comment(company_user_client,
                                                      DEFAULT_COMMENT_DATA)
        assert resp.status_code == http.HTTPStatus.BAD_REQUEST

    def test_create_job_seeker_comment_with_invalid_source(
            self, company_user_client):
        job_seeker_invalid_id = 999999
        # make sure we don't have job_seeker with `job_seeker_invalid_id`
        assert JobSeeker.objects.filter(id=job_seeker_invalid_id).count() == 0
        DEFAULT_COMMENT_DATA.update({'source': str(job_seeker_invalid_id)})
        resp = api_requests.create_job_seeker_comment(company_user_client,
                                                      DEFAULT_COMMENT_DATA)
        assert resp.status_code == http.HTTPStatus.BAD_REQUEST


class TestGetJobSeekerComment:
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
    ))
    def test_get_job_seeker_comment(self, request, client, status,
                                    company_user, job_seeker):
        comment = create_job_seeker_comment(company_user, job_seeker)
        client = request.getfixturevalue(client)
        resp = api_requests.get_job_seeker_comment(client, comment.id)
        assert resp.status_code == status

    def test_company_users_cant_see_comments_from_different_companies(
            self, company_user, job_seeker, company_user_client,
            company_2_user_client, company_2_user):
        comment = create_job_seeker_comment(company_user, job_seeker)
        resp_1 = api_requests.get_job_seeker_comment(company_user_client,
                                                     comment.id)
        assert resp_1.status_code == http.HTTPStatus.OK
        resp_2 = api_requests.get_job_seeker_comment(company_2_user_client,
                                                     comment.id)
        assert resp_2.status_code == http.HTTPStatus.NOT_FOUND
        assert company_user.company != company_2_user.company

    def test_company_user_can_view_mate_comments(
            self, company_user, company_user_client,
            company_user_2_client, job_seeker):
        comment = create_job_seeker_comment(company_user, job_seeker)
        resp_1 = api_requests.get_job_seeker_comment(company_user_client,
                                                     comment.id)
        assert resp_1.status_code == http.HTTPStatus.OK
        resp_2 = api_requests.get_job_seeker_comment(company_user_2_client,
                                                     comment.id)
        assert resp_2.status_code == http.HTTPStatus.OK


class TestUpdateJobSeekerComment:

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
    ))
    def test_update_job_seeker_comment(
            self, request, client, status, company_user, job_seeker,
            comment_base_data):
        comment = create_job_seeker_comment(company_user, job_seeker)
        client = request.getfixturevalue(client)
        resp = api_requests.update_job_seeker_comment(client, comment.id,
                                                      comment_base_data)
        assert resp.status_code == status

    def test_company_users_cant_update_comments_from_different_companies(
            self, company_user, job_seeker, company_user_client,
            company_2_user_client, company_2_user, comment_base_data):
        comment = create_job_seeker_comment(company_user, job_seeker)
        resp_1 = api_requests.update_job_seeker_comment(
            company_user_client, comment.id, comment_base_data)
        assert resp_1.status_code == http.HTTPStatus.OK

        resp_2 = api_requests.update_job_seeker_comment(
            company_2_user_client, comment.id, comment_base_data)
        assert resp_2.status_code == http.HTTPStatus.NOT_FOUND

        assert company_user.company != company_2_user.company

    def test_company_user_cant_update_mate_comments(
            self, company_user, company_user_client, company_user_2_client,
            job_seeker, comment_base_data):
        comment = create_job_seeker_comment(company_user, job_seeker)

        resp_1 = api_requests.update_job_seeker_comment(
            company_user_client, comment.id, comment_base_data)
        assert resp_1.status_code == http.HTTPStatus.OK

        resp_2 = api_requests.update_job_seeker_comment(
            company_user_2_client, comment.id, comment_base_data)
        assert resp_2.status_code == http.HTTPStatus.FORBIDDEN


class TestPartialUpdateJobSeekerComment:

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
    ))
    def test_update_job_seeker_comment(
            self, request, client, status, company_user, job_seeker,
            comment_base_data):
        comment = create_job_seeker_comment(company_user, job_seeker)
        client = request.getfixturevalue(client)
        resp = api_requests.partial_update_job_seeker_comment(
            client, comment.id, comment_base_data)
        assert resp.status_code == status

    def test_company_users_cant_update_comments_from_different_companies(
            self, company_user, job_seeker, company_user_client,
            company_2_user_client, company_2_user, comment_base_data):
        comment = create_job_seeker_comment(company_user, job_seeker)
        resp_1 = api_requests.partial_update_job_seeker_comment(
            company_user_client, comment.id, comment_base_data)
        assert resp_1.status_code == http.HTTPStatus.OK

        resp_2 = api_requests.partial_update_job_seeker_comment(
            company_2_user_client, comment.id, comment_base_data)
        assert resp_2.status_code == http.HTTPStatus.NOT_FOUND

        assert company_user.company != company_2_user.company

    def test_company_user_cant_update_mate_comments(
            self, company_user, company_user_client, company_user_2_client,
            job_seeker, comment_base_data):
        comment = create_job_seeker_comment(company_user, job_seeker)

        resp_1 = api_requests.partial_update_job_seeker_comment(
            company_user_client, comment.id, comment_base_data)
        assert resp_1.status_code == http.HTTPStatus.OK

        resp_2 = api_requests.partial_update_job_seeker_comment(
            company_user_2_client, comment.id, comment_base_data)
        assert resp_2.status_code == http.HTTPStatus.FORBIDDEN


class TestDeleteJobSeekerComment:
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
                    http.HTTPStatus.NO_CONTENT
                ),
        ))
    def test_delete_job_seeker_comment(
            self, request, client, status, company_user, job_seeker):
        comment = create_job_seeker_comment(company_user, job_seeker)
        client = request.getfixturevalue(client)
        resp = api_requests.delete_job_seeker_comment(client, comment.id)
        assert resp.status_code == status

    def test_company_users_cant_delete_comments_from_different_companies(
            self, company_user, job_seeker, company_user_client,
            company_2_user_client, company_2_user):
        comment = create_job_seeker_comment(company_user, job_seeker)

        resp_1 = api_requests.delete_job_seeker_comment(company_2_user_client,
                                                        comment.id)
        assert resp_1.status_code == http.HTTPStatus.NOT_FOUND

        resp_2 = api_requests.delete_job_seeker_comment(company_user_client,
                                                        comment.id)
        assert resp_2.status_code == http.HTTPStatus.NO_CONTENT

        assert company_user.company != company_2_user.company

    def test_company_user_cant_delete_mate_comments(
            self, company_user, company_user_client, company_user_2_client,
            job_seeker):
        comment = create_job_seeker_comment(company_user, job_seeker)

        resp_1 = api_requests.delete_job_seeker_comment(company_user_2_client,
                                                        comment.id)
        assert resp_1.status_code == http.HTTPStatus.FORBIDDEN

        resp_2 = api_requests.delete_job_seeker_comment(company_user_client,
                                                        comment.id)
        assert resp_2.status_code == http.HTTPStatus.NO_CONTENT


class TestGetJobSeekerCommentList:
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
    ))
    def test_get_job_seeker_comment_list(self, request, client, status,
                                         company_user, job_seeker):
        create_job_seeker_comment(company_user, job_seeker)
        client = request.getfixturevalue(client)
        resp = api_requests.get_job_seeker_comment_list(client, job_seeker.id)
        assert resp.status_code == status

    def test_get_comment_in_job_seeker_comment_list(
            self, company_user_client, company_user, job_seeker):
        data = {
            'title': 'no',
            'comment': 'way'
        }
        create_job_seeker_comment(company_user, job_seeker, **data)
        resp = api_requests.get_job_seeker_comment_list(company_user_client,
                                                        job_seeker.id)
        assert resp.status_code == http.HTTPStatus.OK
        resp_data = resp.json()['results'][0]
        assert resp_data['title'] == data['title']
        assert resp_data['comment'] == data['comment']
        assert resp_data['user']['name'] == \
               company_user.user.get_full_name()

    def test_company_users_cant_get_comments_from_different_companies(
            self, company_user, job_seeker, company_user_client,
            company_2_user_client, company_2_user):
        create_job_seeker_comment(company_user, job_seeker)

        resp_1 = api_requests.get_job_seeker_comment_list(
            company_user_client, job_seeker.id)
        assert resp_1.status_code == http.HTTPStatus.OK
        assert resp_1.json()['count'] == 1

        resp_2 = api_requests.get_job_seeker_comment_list(
            company_2_user_client, job_seeker.id)
        assert resp_2.status_code == http.HTTPStatus.OK

        assert company_user.company != company_2_user.company
        assert resp_2.json()['count'] == 0

    def test_company_user_can_get_all_company_comments(
            self, company_user, company_user_client, company_user_2_client,
            job_seeker):
        create_job_seeker_comment(company_user, job_seeker)

        resp_1 = api_requests.get_job_seeker_comment_list(
            company_user_client, job_seeker.id)
        assert resp_1.status_code == http.HTTPStatus.OK
        assert resp_1.json()['count'] == 1

        resp_2 = api_requests.get_job_seeker_comment_list(
            company_user_2_client, job_seeker.id)
        assert resp_2.status_code == http.HTTPStatus.OK
        assert resp_2.json()['count'] == 1

    def test_js_comment_list_new_comments(
            self, company_user, company_user_client, company_user_2_client,
            job_seeker):
        resp = api_requests.get_job_seeker_comment_list(company_user_client,
                                                        job_seeker.id)
        assert resp.status_code == http.HTTPStatus.OK
        resp_data = resp.json()
        assert resp_data['count'] == 0
        assert resp_data['new_comments'] == 0

        DEFAULT_COMMENT_DATA.update({'source': job_seeker.id})
        api_requests.create_job_seeker_comment(company_user_client,
                                               DEFAULT_COMMENT_DATA)
        resp = api_requests.get_job_seeker_comment_list(company_user_client,
                                                        job_seeker.id)
        assert resp.status_code == http.HTTPStatus.OK
        resp_data = resp.json()
        assert resp_data['count'] == 1
        # make sure that created object by ourselves doesn't count as `new`
        assert resp_data['new_comments'] == 0

        api_requests.create_job_seeker_comment(company_user_2_client,
                                               DEFAULT_COMMENT_DATA)
        resp = api_requests.get_job_seeker_comment_list(company_user_client,
                                                        job_seeker.id)
        assert resp.status_code == http.HTTPStatus.OK
        resp_data = resp.json()
        assert resp_data['count'] == 2
        assert resp_data['new_comments'] == 1


class TestBannedJobSeekerComments:

    def test_company_users_cant_see_banned_comment(
            self, company_user, company_user_client, job_seeker):
        comment = create_job_seeker_comment(company_user, job_seeker)
        resp = api_requests.get_job_seeker_comment(
            company_user_client, comment.id)
        assert resp.status_code == http.HTTPStatus.OK

        utils.ban_entity(comment)
        resp = api_requests.get_job_seeker_comment(
            company_user_client, comment.id)
        assert resp.status_code == http.HTTPStatus.NOT_FOUND

    def test_company_users_cant_see_banned_comments(
            self, company_user_client, company_user, job_seeker):
        comment = create_job_seeker_comment(company_user, job_seeker)
        create_job_seeker_comment(company_user, job_seeker)
        resp = api_requests.get_job_seeker_comment_list(
            company_user_client, job_seeker.id)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == 2

        utils.ban_entity(comment)
        resp = api_requests.get_job_seeker_comment_list(
            company_user_client, job_seeker.id)
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json()['count'] == 1
