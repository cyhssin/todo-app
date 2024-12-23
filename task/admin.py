from django.contrib import admin

from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["title", "completed", "created", "notification"]
    list_filter = ["completed", "created"]
    search_fields = ["title", "description"]
    prepopulated_fields = {"slug":("title",)}
    ordering = ["created", "completed"]