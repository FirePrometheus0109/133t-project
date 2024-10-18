from permission import permissions


class CommentPermission(permissions.BaseModelPermissions):

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            user_company = request.user.company_user.company
            return user_company == obj.user.company_user.company
        return request.user == obj.user
