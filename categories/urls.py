from django.urls import path
from . import views 


app_name = 'categories'

urlpatterns = [
    path('create/', views.create_category, name='create'),
    path('delete/<str:slug>/', views.delete_category, name='delete'),
]