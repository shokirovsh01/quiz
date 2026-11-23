from rest_framework import serializers
from .models import Course, Module, Task, TaskCase, Submission

class TaskCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskCase
        fields = ['id','task','input_data','expected_output']
        read_only_fields = ['id']

class TaskSerializer(serializers.ModelSerializer):
    is_solved_by_me = serializers.SerializerMethodField()
    module = serializers.PrimaryKeyRelatedField(
        queryset = Module.objects.all(),write_only = True
    ) 
    class Meta:
        model = Task
        fields = ['id','title','description','module','is_solved_by_me']
        read_only_fields = ['id','is_solved_by_me']

    def get_is_solved_by_me(self,obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        return obj.submissions.filter(
            user= request.user,status = 'accepted'
        ).exists()

class ModuleSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many = True,read_only=True)
    
    class Meta:
        model = Module
        fields = ['id','title','position','course','tasks']

class CourseSerializer(serializers.ModelSerializer):
    modules = ModuleSerializer(many=True,read_only=True)

    class Meta:
        model = Course
        fields = ['id','title','description','author','created_at','modules']
        read_only_fields = ['id','author','created_at']

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ['id','user','task','code','status','created_at']
        read_only_fields = ['id','user','status','created_at']


class SubmissionCreateSerializer(serializers.ModelSerializer):
    task_id = serializers.PrimaryKeyRelatedField(
        queryset = Task.objects.all(),source='task',
    )
    class Meta:
        model = Submission
        fields = ['id','task_id','code','status']
        read_only_fields = ['id','status']
        