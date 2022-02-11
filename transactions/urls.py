from django.urls import path
from .import views


app_name = 'transactions'

urlpatterns = [
    path('create/', views.create_transaction, name='create'),
]