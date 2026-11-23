from django.db import models
from django.conf import settings
# Create your models here.

class Course(models.Model):
    title = models.CharField(max_length=123)
    description = models.TextField(blank=True,null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='courses')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['title']
        permissions = [
            ('can_manage_content', 'Can manage courses, modules, tasks, test cases'),
        ]

    def __str__(self):
        return self.title

class Module(models.Model):
    title = models.CharField(max_length=123)
    position = models.PositiveIntegerField(default=0)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name='modules')

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.title


class Task(models.Model):
    title = models.CharField(max_length=123)
    description = models.TextField(blank=True)
    module = models.ForeignKey(Module,on_delete=models.CASCADE,related_name='tasks')

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.title

class TaskCase(models.Model):
    input_data = models.TextField()
    expected_output = models.TextField()
    task = models.ForeignKey(Task,on_delete=models.CASCADE,related_name='test_cases')

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f'Test {self.pk} for {self.task}'

class Submission(models.Model):
    STATUS_CHOICES = [
        ('accepted', 'accepted'),
        ('wrong_answer', 'wrong_answer'),
        ('error', 'error'),
        ('time_limit', 'time_limit'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='submissions')
    task = models.ForeignKey(Task,on_delete=models.CASCADE,related_name='submissions')
    code = models.TextField()
    status = models.CharField(max_length=123,choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):  
        return f'User: {self.user} - {self.task} - {self.status}'

       