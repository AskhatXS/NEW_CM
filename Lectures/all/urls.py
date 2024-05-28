from django.urls import path
from . import views
from .views import unauthenticated

urlpatterns = [
    # Общий
    path('student_main/', views.student_main, name='student_main'),
    path('teacher_main/', views.teacher_main, name='teacher_main'),

    # Auth and Reg
    path('unauthenticated/', unauthenticated, name='unauthenticated'),
    path('layout/', views.layout, name='layout'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),

    # Общий 2
    path('courses/<int:course_pk>/lectures/', views.lecture_list, name='lecture_list'),
    path('courses/', views.course_list, name='course_list'),

    path('courses/<int:course_pk>/assignments/', views.assignment_list_for_students, name='assignment_list_for_students'),


    path('assignments/<int:assignment_pk>/grade/', views.grade_assignment, name='grade_assignment'),
    path('courses/<int:course_id>/add/', views.add_assignment_to_course, name='add_assignment_to_course'),
    path('courses/<int:pk>/for_teachers/', views.course_detail, name='course_detail'),
]


