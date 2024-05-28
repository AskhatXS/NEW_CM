from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Course, Connect, Assignment, Grade
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import LoginForm, RegistrationForm, AssignmentForm, AnswerForm


#@login_required(login_url='unauthenticated')
def student_main(request):
    courses = Course.objects.all()
    return render(request, 'students/student_main.html', {'courses': courses})


def teacher_main(request):
    courses = Course.objects.all()
    return render(request, 'teachers/teacher_main.html', {'courses': courses})


def unauthenticated(request):
    return render(request, 'accounts/unauthenticated.html')


def layout(request):
    username = request.user.username
    return render(request, 'layout.html', {'username': username})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                user_status = Connect.objects.filter(user=user).first()
                if user_status and user_status.status == 'teacher':
                    return redirect('teacher_main')
                else:
                    return redirect('student_main')
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            status = form.cleaned_data.get('status')
            Connect.objects.create(user=user, status=status)
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


#@login_required(login_url='unauthenticated')
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'common/course_list.html', {'courses': courses})


#@login_required(login_url='unauthenticated')
def course_detail(request, pk):
    course = Course.objects.get(id=pk)
    return render(request, 'common/course_detail_for_teachers.html', {'course': course})


#@login_required(login_url='unauthenticated')
def lecture_list(request, course_pk):
    course = Course.objects.get(id=course_pk)
    lectures = course.lectures.all()
    return render(request, 'common/lecture_list.html', {'lectures': lectures})


#@login_required(login_url='unauthenticated')
def assignment_list_for_students(request, course_id):
    course = Course.objects.get(id=course_pk)
    assignments = Assignment.objects.filter(course=course)
    return render(request, 'students/assignment_list_for_students.html', {'assignments': assignments})

#
#@login_required(login_url='unauthenticated')
def grade_assignment(request, assignment_pk):
    assignment = Assignment.objects.get(id=assignment_pk)
    if request.method == 'POST':
        grade = request.POST['grade']
        comment = request.POST['comment']
        Grade.objects.create(assignment=assignment, student=request.user, grade=grade, comment=comment)
    return render(request, 'students/grade_assignment_students.html', {'assignment': assignment})


# Добавить задании(учитель)
#@login_required(login_url='unauthenticated')
def add_assignment_to_course(request, course_id):
    course = Course.objects.get(pk=course_id)
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.course = course
            assignment.teacher = request.user
            assignment.save()
            return redirect('course_detail', course_id=course_id)
    else:
        form = AssignmentForm()
    return render(request, 'common/add_assignment.html', {'form': form, 'course': course})

#  Просмотреть задания(ученик)
@login_required
def view_grades(request):
    student = request.user
    grades = Grade.objects.filter(student=student)
    return render(request, 'grades.html', {'grades': grades})


def add_answer(request, assignment_id):
    assignment = Assignment.objects.get(pk=assignment_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST, request.FILES)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.assignment = assignment
            answer.student = request.user
            answer.save()
            return redirect('assignment_list')
    else:
        form = AnswerForm()
    return render(request, 'add_answer.html', {'form': form})

