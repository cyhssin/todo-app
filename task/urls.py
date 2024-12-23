from django.urls import path

from . import views

app_name = "task"

urlpatterns = [
    path("", views.TaskView.as_view(), name="task_list"),
    path("task/<slug:slug>/", views.TaskDetailView.as_view(), name="task_detail"),
    path("task/delete/<slug:slug>/", views.TaskDeleteView.as_view(), name="task_delete"),
    path("task/favorite/<slug:slug>/", views.TaskFavoriteView.as_view(), name="task_favorite"),
]