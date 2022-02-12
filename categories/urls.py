from django.urls import path
from . import views 


app_name = 'categories'

urlpatterns = [
    path('', views.view, name='view'),
    path('create/', views.create_category, name='create'),
    path('delete/<str:slug>/', views.delete_category, name='delete'),
    path('edit/<str:slug>/', views.edit, name='edit'),
]