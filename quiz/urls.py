from django.urls import path
from .views import *


urlpatterns = [
    path('courses/', CourseCreateList.as_view()),
    path('courses/<int:pk>/', Coursedetail.as_view()),
    path('modules/', ModuleCreateList.as_view()),
    path('modules/<int:pk>/', Moduledetail.as_view()),
    path('tasks/', TaskCreateList.as_view()),
    path('tasks/<int:pk>/', Taskdetail.as_view()),
    path('submissions/', SubmissionCreateView.as_view()),
    path('taskcases/', TaskCaseListCreate.as_view()),      
    path('taskcases/<int:pk>/', TaskCaseDetail.as_view()),
    path('statistics/', StatisticView.as_view()),
]