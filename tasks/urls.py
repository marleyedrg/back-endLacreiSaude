from django.urls import path
from .views import *

urlpatterns = [
    path("", list_tasks, name="list_tasks"),
    path("create/", create_task, name="create_task"),
    path("<int:task_id>/", update_task, name="update_task"),
    path("<int:task_id>/delete/", delete_task, name="delete_task"),
]