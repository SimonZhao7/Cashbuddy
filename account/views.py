from django.shortcuts import render, redirect
from django.contrib.auth import login as login_user, logout as logout_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from .models import CustomUser
from .forms import RegisterForm, ChangeUsernameForm, ChangeBudgetForm, ResetPasswordForm
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


def forgot_password(request):
    form = PasswordResetForm()
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request, 
                subject_template_name="forgot_subject.txt",
                email_template_name='forgot_subject.txt',
                from_email='emails.cashbuddy@gmail.com',
                html_email_template_name='forgot_password.html',
            )
            return redirect('account:login')
    return render(request, 'form.html', {'form': form, 'title': 'Forgot Password', 'btn_text': 'Send Email'})


def forgot_password_reset(request, slug, token):
    try: 
        user = CustomUser.objects.get(pk=CustomUser.get_id(slug))
    except CustomUser.DoesNotExist:
        return render(request, '404.html')
    
    # Token doesn't match
    if not default_token_generator.check_token(user, token):
        return render(request, '404.html')
    
    form = ResetPasswordForm(user)
    if request.method == 'POST':
        form = ResetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('account:login')
    return render(request, 'form.html', {'form': form, 'title': 'Reset Password', 'btn_text': 'Reset Password'})


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
            form.save()
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


@login_required
def change_budget(request):
    form = ChangeBudgetForm(user=request.user, initial={'budget': request.user.budget})
    if request.method == 'POST':
        form = ChangeBudgetForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('account:home')
    return render(request, 'form.html', {'form': form, 'title': 'Change Budget', 'btn_text': 'Change'})