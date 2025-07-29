# from django.shortcuts import render
#
# # Create your views here.
from django.db.models import Count
from django.shortcuts import get_object_or_404
#app/view.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .serializers import TaskSerializer, CategorySerializer, TagSerializer, NotesSerializer
from rest_framework import status
from .models import Task, Category, Tag, Notes
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import viewsets


# Create your views here.

class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.all()
        category_id = self.request.query_params.get('category')
        tag_id = self.request.query_params.get('tag')
        if category_id is not None:
            queryset = queryset.filter(category_id=category_id)
        if tag_id is not None:
            queryset = queryset.filter(tags__id=tag_id)  # M2M filter
        return queryset


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(
        task_count=Count('tasks')  # Count distinct tasks in each category
    )
    serializer_class = CategorySerializer


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.annotate(
        task_count=Count('tasks')  # Count related tasks
    )
    serializer_class = TagSerializer


class NotesViewSet(ModelViewSet):
    queryset = Notes.objects.all()
    serializer_class = NotesSerializer

    def get_queryset(self):
        print("KWARGS:", self.kwargs)
        return Notes.objects.filter(task_id=self.kwargs['task_pk'])

    def perform_create(self, serializer):
        task = Task.objects.get(pk=self.kwargs['task_pk'])
        serializer.save(task=task)

# class Tasklist(ListCreateAPIView):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer
# class TaskDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer
#     lookup_field = 'id'


# def get_queryset(self):
#     return Task.objects.all()
#
#     def get_serializer_class(self):
# return TaskSerializer
# def get(self, request, *args, **kwargs):
#     return super().get(request, *args, **kwargs)
#
# def post(self, request, *args, **kwargs):
#     return super().post(request, *args, **kwargs)


# old system


# @api_view(['GET','POST'])
# def index(request) :
#     if request.method == 'GET':
#         all_task = Task.objects.all()
#         obj = TaskSerializer(all_task, many=True)
#         return Response(obj.data)
#     elif request.method == 'POST' :
#         obj = TaskSerializer(data=request.data)
#         if obj.is_valid() :
#             newTask = obj.save()
#             return Response(TaskSerializer(newTask).data,
#                             status=status.HTTP_201_CREATED)
#         else : return Response(obj.errors,
#                                status=status.HTTP_400_BAD_REQUEST)
# @api_view(['GET','PUT','PATCH','DELETE'])
# def task(request,id) :
#     task = get_object_or_404(Task, id=id) #Task.objects.get(id=id)
#     if request.method == 'GET':
#         serializer = TaskSerializer(task)
#         return Response(serializer.data)
#     elif request.method in ['PUT', 'PATCH']:
#         partial = request.method == 'PATCH'
#         serializer = TaskSerializer(task, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'PATCH':
#         serializer = TaskSerializer(task, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'DELETE':
#         task.delete()
#         return Response({"message": "Task deleted successfully."},
#                         status=status.HTTP_204_NO_CONTENT)
