from django.contrib import admin
from .models import Task, TaskImage, Comment, CommentLike

# Register your models here.

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "status", "priority", "date", "creator")
    search_fields = ("title", "description")
    list_filter = ("status", "priority")
    list_editable = ("status", "priority")

admin.site.register(TaskImage)
admin.site.register(Comment)
admin.site.register(CommentLike)