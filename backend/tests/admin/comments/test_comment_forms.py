import pytest

from tests.admin.comments import constants


class TestCommentForms:

    @pytest.mark.parametrize(('form', 'commented_obj', 'key_name'), (
        (
            'job_comment_creation_form',
            'job_obj',
            'job'
        ),
        (
            'job_seeker_comment_creation_form',
            'job_seeker',
            'job_seeker'
        ),
    ))
    def test_creation_comments_form_success(
            self, request, form, commented_obj, key_name, admin_user):
        form_class = request.getfixturevalue(form)
        obj = request.getfixturevalue(commented_obj)
        data = constants.COMMENT_INITIAL_DATA.copy()
        data.update({key_name: obj.id})
        form_instance = form_class(data)

        assert form_instance.is_valid()
        comment = form_instance.save(admin_user)
        assert comment.title == data['title']
        assert comment.comment == data['comment']
        assert comment.object_pk == obj.id

    @pytest.mark.parametrize(('form',), (
        (
            'job_comment_creation_form',
        ),
        (
            'job_seeker_comment_creation_form',
        ),
    ))
    def test_cant_create_comment_without_obj(
            self, request, form, admin_user):
        form_class = request.getfixturevalue(form)
        data = constants.COMMENT_INITIAL_DATA.copy()
        form_instance = form_class(data)

        assert not form_instance.is_valid()
        with pytest.raises(ValueError) as e:
            form_instance.save(admin_user)

    @pytest.mark.parametrize(('form', 'obj', 'key_name'), (
        (
            'job_comment_change_form',
            'job_comment',
            'job',
        ),
        (
            'job_seeker_comment_change_form',
            'job_seeker_comment',
            'job_seeker'
        ),
    ))
    def test_change_comments_form_success(
            self, request, form, obj, admin_user, key_name):
        form_class = request.getfixturevalue(form)
        initial_obj = request.getfixturevalue(obj)
        form_instance = form_class(
            data=constants.COMMENT_CHANGE_DATA,
            instance=initial_obj)

        assert form_instance.initial[key_name].id == initial_obj.object_pk
        form_instance.is_valid()
        comment = form_instance.save()
        assert comment.title == constants.COMMENT_CHANGE_DATA['title']
        assert comment.comment == constants.COMMENT_CHANGE_DATA['comment']
        assert comment.user == initial_obj.user
