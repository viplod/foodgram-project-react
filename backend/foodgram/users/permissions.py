from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class AdminOrReadonly(permissions.BasePermission):
    """
    Права доступа:
    чтение для всех
    изменения только для администратора
    """

    # def has_permission(self, request, view):
    #     return (request.method in SAFE_METHODS) or (
    #         (request.user.is_authenticated and (
    #             (request.user.is_admin or request.user.is_staff)))
    #     )

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS) or (
            (request.user.is_authenticated))
