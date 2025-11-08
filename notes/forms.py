from django import forms
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from .models import Task, TaskImage, Comment, Profile

class RegisterForm(forms.Form): 
    username = forms.CharField(label="Логін", max_length=100)
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

    def clean_password(self):
        password = self.cleaned_data['password']

        if len(password) < 8:
            raise ValidationError("Пароль повинен містити щонайменше 8 символів.\nПароль повинен містити хоча б одну велику літеру.\nПароль повинен містити хоча б одну цифру.")
        if not re.search(r'[A-Z]', password):
            raise ValidationError("Пароль повинен містити хоча б одну велику літеру.\nПароль повинен містити хоча б одну цифру.")
        if not re.search(r'\d', password):
            raise ValidationError("Пароль повинен містити хоча б одну цифру.")

        return password

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'priority', 'date']
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }

class TaskFilterForm(forms.Form):
    status = forms.ChoiceField(
        choices=[('', 'All')] + Task.STATUS_CHOICES,
        required=False,
        label='Status'
    )
    priority = forms.ChoiceField(
        choices=[('', 'All')] + Task.PRIORITY_CHOICES,
        required=False,
        label='Priority'
    )
    date = forms.DateField(
        required=False,
        label='Date',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

class TaskImageForm(forms.ModelForm):
    class Meta:
        model = TaskImage
        fields = ['image']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 3, "placeholder": "Write a comment..."}),
        }
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'bio', 'avatar']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 5}),
        }