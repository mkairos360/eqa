import json

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import Group
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import Student
from .forms import StudentRegisterForm, StudentProfileForm

# Create your views here.
from django.contrib.auth import get_user_model

# Register your models here.
User = get_user_model()


def register_student(request):
    form = StudentRegisterForm()

    if request.method == 'POST':
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            student_group = Group.objects.get(name='student')
            student_group.user_set.add(user)
            login(request, user)
            return redirect('student_profile_create', pk=user.id)
        else:
            form = StudentRegisterForm(request.POST)

    context = {"form": form}
    return render(request, 'registration/register.html', context)


def student_profile_create(request, pk):
    user = get_object_or_404(User, pk=pk)
    form = StudentProfileForm(initial={'user': user})
    context = {
        'form': form,
        'page_title': 'Extra Registration'
    }
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, initial={'user': user})
        if form.is_valid():
            Student(user=user, **form.cleaned_data).save()
            return redirect('evaluations')
        else:
            context['error'] = form.errors.as_json()
            print(form.errors.as_json())
            return render(request, 'registration/register-extra.html', context)
    return render(request, 'registration/register-extra.html', context)


def login_qadmin(request):
    page_title = 'Admin Login/Register'
    context = {'page_title': page_title,
               'bg': 'bg-dark',
               'admin': True
               }

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        # this would have to become a custom user (e.g. student)
        qadmin = authenticate(username=username, password=password)
        if qadmin is not None:
            login(request, qadmin)
            messages.success(request, 'Welcome ')
            return redirect('view_all_evaluations')
        else:
            print('login error')
            context['login_error'] = 'Username or password is incorrect.'
            messages.error(request, 'Login error, credentials invalid')
            return render(request, 'accounts/auth/auth_login_boxed.html', context)

    return render(request, 'accounts/auth/auth_login_boxed.html', context)


def login_student(request):
    page_title = 'Login/Register'
    context = {'page_title': page_title}
    print("logged in view")
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        # this would have to become a custom user (e.g. student)
        student = authenticate(username=username, password=password)
        if student is not None:
            print(student)
            login(request, student)
            messages.success(request, 'Welcome ')
            return redirect('evaluations')
        else:
            print('login error')
            context['login_error'] = 'Username or password is incorrect.'
            messages.error(request, 'Login error, credentials invalid')
            return render(request, 'accounts/auth/auth_login_boxed.html', context)

    return render(request, 'accounts/auth/auth_login_boxed.html', context)


def logout_student(request):
    logout(request)
    return redirect('login_student')