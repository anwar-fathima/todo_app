from django.urls import path
from .import views

urlpatterns = [
    path('todo/', views.task, name='task'),
    path('todo/<int:task_id>/', views.task, name='task'),
]