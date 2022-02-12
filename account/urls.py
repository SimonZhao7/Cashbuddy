from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('change-username/', views.change_username, name='change_username'),
    path('change-password/', views.change_password, name='change_password'),
    path('change-budget/', views.change_budget, name='change_budget'),
    path('change-email/', views.change_email, name='change_email'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-forgot-password/<str:slug>/<str:token>/', views.forgot_password_reset, name='reset_forgot_password')
]