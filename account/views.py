from django.shortcuts import render, redirect
from django.contrib.auth import login as login_user, logout as logout_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from account.forms import RegisterForm, ChangeUsernameForm
from transactions.models import Transaction

# Create your views here.

@login_required
def home(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('date_created').reverse()[:5]
    return render(request, 'home.html', {'transactions': transactions})


def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('account:login')
    return render(request, 'form.html', {'form': form, 'title': 'Register', 'btn_text': 'Register'})


def login(request):
    if request.user.is_authenticated:
        return redirect('account:home')
    
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login_user(request, form.get_user())
            return redirect('account:home')
    return render(request, 'form.html', {'form': form, 'title': 'Login', 'btn_text': 'Login'})

@login_required
def logout(request):
    logout_user(request)
    return redirect('account:login')


@login_required
def change_username(request):
    form = ChangeUsernameForm(user=request.user)
    if request.method == 'POST':
        form = ChangeUsernameForm(request.POST, user=request.user)
        if form.is_valid():
            form.save(request.user)
            return redirect('account:home')
    return render(request, 'form.html', {'form': form, 'title': 'Change Username', 'btn_text': 'Change'})


@login_required
def change_password(request):
    user = request.user
    form = PasswordChangeForm(user)
    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            login_user(request, user)
            return redirect('account:home')
    return render(request, 'form.html', {'form': form, 'title': 'Change Password', 'btn_text': 'Change'})