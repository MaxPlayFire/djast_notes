from .models import Task
from django.shortcuts import render, redirect
from django.urls import path, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, TaskForm
class TaskListView(ListView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'
class TaskDetailView(DetailView):
    model = Task
    template_name = 'task_detail.html'
    context_object_name = 'task'
class TaskCreateView(CreateView):
    model = Task
    form_class = TaskForm
    template_name = "task_form.html"
    success_url = reverse_lazy("tasks:task_list")