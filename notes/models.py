from django.db import models

# Create your models here.

class Task(models.Model):
    STATUS_CHOICES = [
        ("todo", "To Do"),
        ("in_progres", "In Progres"),
        ("done", "Done"),
        ("failled", "Failled"),
    ]
    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]
    title = models.CharField(max_length=64)
    description = models.TextField()

    date = models.DateField(null=True, blank=True)
    priority = models.CharField(choices=PRIORITY_CHOICES, default="medium")
    status = models.CharField(choices=STATUS_CHOICES, default="todo")

    def __str__(self):
        return self.title