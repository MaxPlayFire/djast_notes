from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views import View
from django.db.models import Q
from .models import Task, TaskImage, Comment, CommentLike, Profile
from .forms import TaskForm, TaskFilterForm, CommentForm, ProfileForm
from .mixins import UserIsOwnerMixin

class TaskListView(ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 10

    def get_queryset(self):
        queryset = Task.objects.all()
        form = TaskFilterForm(self.request.GET)
        if form.is_valid():
            status = form.cleaned_data.get("status")
            priority = form.cleaned_data.get("priority")
            date = form.cleaned_data.get("date")
            
            if status:
                queryset = queryset.filter(status=status)
            if priority:
                queryset = queryset.filter(priority=priority)
            if date:
                queryset = queryset.filter(date=date)
        
        query = self.request.GET.get('q', '')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
        
        queryset = queryset.order_by('-id')
        
        if not queryset.exists():
            messages.info(self.request, "Задач не знайдено")
        
        return queryset

class TaskDetailView(DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = self.object.comments.all().order_by("-created_at")
        context["form"] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.task = self.object
            comment.save()
            messages.success(request, "Коментар додано!")
        else:
            messages.error(request, "Помилка додавання коментаря.")
        return redirect("task_detail", pk=self.object.pk)

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')
   
    def form_valid(self, form):
        task = form.save(commit=False)
        task.creator = self.request.user
        task.save()
        
        images = self.request.FILES.getlist('images')
        for f in images:
            TaskImage.objects.create(task=task, image=f)
        
        messages.success(self.request, "Задача створена!")
        return super().form_valid(form)

class TaskUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        task = form.save()
        
        images = self.request.FILES.getlist('images')
        for f in images:
            TaskImage.objects.create(task=task, image=f)
        
        messages.success(self.request, "Задача оновлена!")
        return super().form_valid(form)

class TaskDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        messages.success(self.request, "Задача видалена!")
        return super().form_valid(form)

class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy("task_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, "Реєстрація успішна!")
        return response

class CommentEditView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'tasks/comment_form.html'

    def get_success_url(self):
        messages.success(self.request, "Коментар оновлено!")
        return reverse_lazy("task_detail", kwargs={"pk": self.object.task.pk})

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            messages.error(request, "Ви не можете редагувати чужий коментар.")
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'tasks/comment_confirm_delete.html'

    def get_success_url(self):
        messages.success(self.request, "Коментар видалено!")
        return reverse_lazy("task_detail", kwargs={"pk": self.object.task.pk})

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().author != request.user:
            messages.error(request, "Ви не можете видаляти чужий коментар.")
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class ToggleLikeView(LoginRequiredMixin, View):
    def post(self, request, pk):
        comment = Comment.objects.get(pk=pk)
        like, created = CommentLike.objects.get_or_create(comment=comment, user=request.user)
        if not created:
            like.delete()
            messages.info(request, "Лайк видалено.")
        else:
            messages.success(request, "Коментар лайкнуто!")
        return redirect("task_detail", pk=comment.task.pk)
    
class ProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'profile.html'
    context_object_name = 'profile'

    def get_object(self):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile

class EditProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'edit_profile.html'

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)

    def get_success_url(self):
        messages.success(self.request, "Профіль оновлено!")
        return reverse_lazy('profile')