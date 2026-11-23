from django.contrib import admin
from .models import CustomUser, Profile, Role


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'fullname', 'role', 'task_count', 'phone')
    list_filter = ('role',)
    search_fields = ('fullname', 'user__username')


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'role_name')
        