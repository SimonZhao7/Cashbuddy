from django.shortcuts import render, redirect
from django.contrib.auth import login as login_user, logout as logout_user
from django.contrib.auth.forms import AuthenticationForm
from account.forms import RegisterForm

# Create your views here.


def home(request):
    return render(request, 'home.html')


def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('account:login')
    return render(request, 'register.html', {'form': form})


def login(request):
    if request.user.is_authenticated:
        return redirect('account:home')
    
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login_user(request, form.get_user())
            return redirect('account:home')
    return render(request, 'login.html', {'form': form})

def logout(request):
    logout_user(request)
    return redirect('account:login')