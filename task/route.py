# #app/urls.py
# from . import views
# # from rest_framework.routers import DefaultRouter
# from .views import TaskViewSet, CategoryViewSet , NotesViewSet
# from  rest_framework_nested.routers import DefaultRouter,NestedDefaultRouter
#
#
# task_sub_route = NestedDefaultRouter(DefaultRouter, r'tasks', lookup='task')
#
# router = DefaultRouter()
# router.register(r'tasks', TaskViewSet)
# router.register(r'categories', CategoryViewSet)
# router.register(r'tags', views.TagViewSet)  # Assuming you have a TagViewSet defined
# router.register(r'notes', views.NotesViewSet)  # Assuming you have a NotesViewSet defined
# urlpatterns = [
#     path('', include(router.urls)),
#     # path('all/', views.index),
#     # path('create/', views.Tasklist.as_view()),
#     # path('', views.Tasklist.as_view()),
#     # path('<id>/',views.TaskDetail.as_view()),
#     # path('<id>/', views.task)
# ]


from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from django.urls import path, include
from task import views

router = DefaultRouter()
router.register('tasks', views.TaskViewSet)
# router.register('notes', views.NoteViewSet)

tasks_router = NestedDefaultRouter(router, 'tasks', lookup='task')
tasks_router.register('notes', views.NotesViewSet, basename='task-notes')
tasks_router.register('categories', views.CategoryViewSet, basename='task-categories')
tasks_router.register('tags', views.TagViewSet, basename='task-tags')

# urlpatterns = router.urls + tasks_router.urls

urlpatterns = [
    path('', include(router.urls)),
    path('', include(tasks_router.urls)),
]