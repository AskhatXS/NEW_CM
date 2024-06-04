from django.urls import path
from . import views
from .views import unauthenticated

urlpatterns = [
    path('main/', views.main, name='main'),
    path('unauthenticated/', unauthenticated, name='unauthenticated'),
    path('about_us/', views.about_us, name='about us'),
    path('', views.layout, name='layout'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('courses/<int:course_pk>/lectures/', views.lecture_list, name='lecture_list'),
    path('courses/<int:course_pk>/assignments/', views.assignment_list, name='assignment_list'),
    path('assignments/<int:assignment_pk>/grade/', views.grade_assignment, name='grade_assignment'),
    path('courses/<int:course_id>/add/', views.add_assignment_to_course, name='add_assignment_to_course'),
    path('courses/<int:pk>/', views.course_detail, name='course_detail'),
]


