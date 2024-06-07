from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Course, Connect, Assignment, Grade
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .forms import LoginForm, UserCreation, AssignmentForm, AnswerForm


@login_required(login_url='unauthenticated')
def main(request):
    courses = Course.objects.all()
    username = request.user.username
    return render(request, 'view/main.html', {'courses': courses, 'username': username})


def unauthenticated(request):
    return render(request, 'accounts/unauthenticated.html')


def layout(request):
    return render(request, 'layout.html', )


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password1'])
            if user is not None:
                login(request, user)
                return redirect('main')
            else:
                form.add_error(None, 'Ошибка в имени или пароле!')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserCreation(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = UserCreation()
    return render(request, 'accounts/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')


@login_required(login_url='unauthenticated')
def about_us(request):
    return render(request, template_name='common/about us.html')


@login_required(login_url='unauthenticated')
def course_detail(request, pk):
    course = Course.objects.get(id=pk)
    return render(request, 'view/course_detail.html', {'course': course})


@login_required(login_url='unauthenticated')
def lecture_list(request, course_pk):
    course = Course.objects.get(id=course_pk)
    lectures = course.lectures.all()
    return render(request, 'common/lecture_list.html', {'lectures': lectures})


@login_required(login_url='unauthenticated')
def assignment_list(request, course_id):
    course = Course.objects.get(id=course_id)
    assignments = Assignment.objects.filter(course=course)
    return render(request, 'view/assignment_list.html', {'assignments': assignments})

#
#@login_required(login_url='unauthenticated')
def grade_assignment(request, assignment_pk):
    assignment = Assignment.objects.get(id=assignment_pk)
    if request.method == 'POST':
        grade = request.POST['grade']
        comment = request.POST['comment']
        Grade.objects.create(assignment=assignment, student=request.user, grade=grade, comment=comment)
    return render(request, 'view/grade_assignment.html', {'assignment': assignment})



@login_required(login_url='unauthenticated')
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
    return render(request, 'teachers/add_assignment.html', {'form': form, 'course': course})


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
