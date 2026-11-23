from django.shortcuts import render
from rest_framework import generics,filters
from .serializers import *
from .check import *
from rest_framework.permissions import IsAuthenticated
from acounts.permissions import IsAdmin,IsAdminOrReadOnly,IsStudent,get_role
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q,Avg,Sum,Count,Max,Min
from django.contrib.auth import get_user_model

# Create your views here.

class CourseCreateList(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['title','description']
    ordering = ['title']

    def get_queryset(self):
        qs = super().get_queryset()
        title= self.request.query_params.get('title')
        if title:
            qs = qs.filter(title__icontains=title)
        return qs


    def perform_create(self, serializer):
        serializer.save(author=self.request.user)



class Coursedetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAdminOrReadOnly]



class ModuleCreateList(generics.ListCreateAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['title','position']
    ordering = ['position']

    def get_queryset(self):
        qs = super().get_queryset()
        course = self.request.query_params.get('course')
        if course:
            qs = qs.filter(course_id=course)
        return qs

class Moduledetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [IsAdminOrReadOnly]

class TaskCreateList(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['title','description']
    ordering_fields = ['title','id']
    ordering = ['id']

    def get_queryset(self):
        qs = super().get_queryset()
        module = self.request.query_params.get('module')
        if module:
            qs = qs.filter(module_id=module)
        return qs

class Taskdetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAdminOrReadOnly]


class SubmissionCreateView(generics.ListCreateAPIView):
    queryset = Submission.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SubmissionCreateSerializer
        return SubmissionSerializer

    def get_queryset(self):
        user = self.request.user
        if get_role(user) == 'admin':
            return Submission.objects.all()
        qs = Submission.objects.filter(user=user)
        status = self.request.query_params.get('status')

        if status:
            qs = qs.filter(status=status)
        return qs

    def perform_create(self, serializer):
        task = serializer.validated_data['task']
        code = serializer.validated_data['code']
        status = run_code(code,task.test_cases.all())
        serializer.save(user=self.request.user,status=status)


class TaskCaseListCreate(generics.ListCreateAPIView):
    queryset = TaskCase.objects.all()
    serializer_class = TaskCaseSerializer
    permission_classes = [IsAdmin]

class TaskCaseDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TaskCase.objects.all()
    serializer_class = TaskCaseSerializer
    permission_classes = [IsAdmin]

class StatisticView(APIView):
    permission_classes = [IsAdmin]

    def get(self,request):
        User = get_user_model()
        totals = Submission.objects.aggregate(
            total = Count('id'),
            accepted = Count('id',filter=Q(status='accepted')),
        )
        task_avg = Task.objects.annotate(n=Count('submissions')).aggregate(
            avg_submissions = Avg('n'),
        )
        
        total_tests = Task.objects.annotate(n=Count('test_cases')).aggregate(
            s = Sum('n'),
        )
        return Response(
            {
                'platform':{
                    'users':User.objects.count(),
                    'courses':Course.objects.count(),
                    'tasks':Task.objects.count(), 
                    'submissions':totals['total'],
                    'accepted':totals['accepted'],
                    'test_cases':total_tests['s'],
                    'avg_submissions_per_task':task_avg['avg_submissions'],
                },
             })

# print(map(sum(int,input())))  


    