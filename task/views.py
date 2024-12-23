from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils.text import slugify

from .models import Task, Favorite
from .serializers import TaskSerializer

class TaskView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(user=request.user)
        ser_tasks = TaskSerializer(instance=tasks, many=True)
        return Response(ser_tasks.data)


class TaskDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, slug):
        task = get_object_or_404(Task, user=request.user, slug=slug)
        ser_tasks = TaskSerializer(instance=task)
        return Response(ser_tasks.data)

    def post(self, request, slug):
        task = get_object_or_404(Task, user=request.user, slug=slug)
        ser_data = TaskSerializer(instance=task, data=request.data)
        
        if ser_data.is_valid():
            updated_task = ser_data.save()
            updated_task.slug = slugify(updated_task.title)
            updated_task.save()
            return Response(TaskSerializer(updated_task).data, status=status.HTTP_200_OK)

        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, slug):
        task = get_object_or_404(Task, user=request.user, slug=slug)
        task.delete()
        return Response("The task was successfully deleted", status=status.HTTP_202_ACCEPTED)

class TaskFavoriteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, slug):
        task = get_object_or_404(Task, user=request.user, slug=slug)
        favorite = Favorite.objects.filter(user=request.user, task=task)

        if favorite.exists():
            favorite.delete()
            return Response("Removed task")
        Favorite.objects.create(user=request.user, task=task)
        return Response("Added task")