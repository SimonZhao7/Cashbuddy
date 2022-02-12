from django.urls import path
from .import views


app_name = 'transactions'

urlpatterns = [
    path('', views.view, name='view'),
    path('create/', views.create_transaction, name='create'),
    path('delete/<str:slug>/', views.delete_transaction, name='delete'),
]