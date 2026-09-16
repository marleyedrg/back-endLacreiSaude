import json

from django.http import JsonResponse
from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt

from .models import Task

# Create your views here.

#GET
def list_tasks(request):
    tasks = Task.objects.all()

    print(tasks)

    data = list(
        tasks.values(
            "id",
            "title",
            "description",
            "completed",
            "created_at",
        )
    )

    return JsonResponse(data, safe=False)

#POST
@csrf_exempt
def create_task(request):
    if request.method == "POST":
        data = json.loads(request.body)

        task = Task.objects.create(
            title=data["title"],
            description=data.get("description", ""),
            completed=data.get("completed", False),
        )

        return JsonResponse(
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
            },
            status=201,
        )

    return JsonResponse({"error": "Method not allowed"}, status=405)

#UPDATE
@csrf_exempt
def update_task(request, task_id):
    if request.method == "PUT":
        data = json.loads(request.body)

    try:
         task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return JsonResponse(
            {"error": "Task not found"},
            status=404
        )

    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)
    task.completed = data.get("completed", task.completed)

    task.save()

    return JsonResponse({
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "completed": task.completed,
    })

#DELETE
@csrf_exempt
def delete_task(request, task_id):
    if request.method == "DELETE":
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return JsonResponse(
                {"error": "Task not found"},
                status=404
            )

        task.delete()

        return JsonResponse(
            {"message": "Task deleted successfully"},
            status=200
        )

    return JsonResponse(
        {"error": "Method not allowed"},
        status=405
    )