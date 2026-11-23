from rest_framework.permissions import BasePermission,SAFE_METHODS

def get_role(user):
    if not user or not user.is_authenticated:
        return None
    if user.is_superuser:
        return 'admin'
    profile = getattr(user,'profile',None)
    if profile and profile.role_id:
        return profile.role.role_name
    return None

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        return get_role(request.user) == 'admin'

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return get_role(request.user) == 'admin'


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return get_role(request.user) == 'student'


 


