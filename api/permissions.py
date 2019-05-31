from rest_framework.permissions import BasePermission

class IsOrganiser(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='organiser').exists()