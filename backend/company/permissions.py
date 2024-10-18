from rest_framework import permissions as drf_permissions

from permission import permissions


class CompanyPermission(permissions.BaseModelPermissions):

    def has_object_permission(self, request, view, obj):
        return request.user.company_user.company == obj


class CompanyLogoPermission(CompanyPermission):

    def has_permission(self, request, view):
        return request.user.has_perm('company.change_company_logo')


class CompanyUserRestorePermission(drf_permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.has_perm('company.add_companyuser')


class CompanyReportPermission(drf_permissions.BasePermission):

    def has_permission(self, request, view):
        has_perm = request.user.has_perm('company.view_report')
        if has_perm and view.kwargs:  # fix swagger
            company_pk = view.kwargs.get('pk')
            return request.user.company_user.company.id == company_pk
        return has_perm


class CandidatesStatusesManagePermission(drf_permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.has_perm(
            'company.change_viewed_candidate_statuses')


class CompanyUserEnumPermission(drf_permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.has_perm('company.view_company_user_enum')
