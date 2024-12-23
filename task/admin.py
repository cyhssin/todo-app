from django.contrib import admin

from .models import Task, Category,Favorite

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "completed", "created", "notification"]
    list_filter = ["completed", "created"]
    search_fields = ["title", "description"]
    prepopulated_fields = {"slug":("title",)}
    ordering = ["created", "completed"]

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_select_related = ["user", "task"]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_select_related = ["user"]
    list_display = ["title", "slug", "created"]
    prepopulated_fields = {"slug":("title",)}