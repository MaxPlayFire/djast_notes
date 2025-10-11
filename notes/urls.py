from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from . import views
app_name = "tasks"
urlpatterns = [
path("", views.TaskListView.as_view(), name="task_list"),
path("<int:pk>/", views.TaskDetailView.as_view(), name="task_detail"),
path("add/", views.TaskCreateView.as_view(), name="task_create"),
]