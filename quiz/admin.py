from django.contrib import admin
from .models import Course, Module, Task, TaskCase, Submission


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at',)


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'course', 'position')
    search_fields = ('title',)
    list_filter = ('course',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'module')
    search_fields = ('title', 'description')
    list_filter = ('module__course',)


@admin.register(TaskCase)
class TestCaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'input_data', 'expected_output')
    search_fields = ('input_data', 'expected_output')


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'task', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'code')