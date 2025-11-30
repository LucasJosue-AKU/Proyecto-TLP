from rest_framework import permissions
class Admin_o_Usuario(permissions.BasePermission):
    def IsAdminUserOrReadOnly(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        
        return request.user and request.user.is_staff