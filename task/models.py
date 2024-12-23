from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="todo_items")
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    notification = models.DateTimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} created by {self.user}"

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="task_favorite")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="favorite_by")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.task.title} favorite by {self.user.username}"    