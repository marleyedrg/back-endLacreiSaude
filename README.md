# back-endLacreiSaude

Django backend project running with Docker, with a simple `Task` CRUD available through HTTP endpoints and the Django Admin.

## Requirements

Before starting, make sure you have installed:

- Docker
- Git

## Getting Started

### 1. Clone the repository

```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Build the Docker image

```bash
docker build -t django-crud .
```

This command:

- `docker build` builds a Docker image using the `Dockerfile`.
- `-t django-crud` gives the image the name `django-crud`.
- `.` uses the current directory as the build context.

### 3. Run database migrations

```bash
docker run --rm -v "$PWD":/app django-crud python manage.py migrate
```

This command:

- `--rm` removes the container after the command finishes.
- `-v "$PWD":/app` mounts the current project directory inside the container.
- `django-crud` is the Docker image.
- `python manage.py migrate` applies the database migrations.

If you change a model, create the migration first:

```bash
docker run --rm -v "$PWD":/app django-crud python manage.py makemigrations
```

Then apply it:

```bash
docker run --rm -v "$PWD":/app django-crud python manage.py migrate
```

### 4. Start the development server

```bash
docker run --rm -p 8000:8000 -v "$PWD":/app django-crud python manage.py runserver 0.0.0.0:8000
```

This command:

- `-p 8000:8000` maps port `8000` from the container to your computer.
- `-v "$PWD":/app` mounts the source code inside the container.
- `runserver 0.0.0.0:8000` allows Django to receive connections from outside the container.

Open:

```text
http://localhost:8000
```

## Tasks App

The project uses a Django app called `tasks`.

To create it in a new setup:

```bash
docker run --rm -v "$PWD":/app django-crud python manage.py startapp tasks
```

Then add it to `INSTALLED_APPS` in `config/settings.py`:

```python
INSTALLED_APPS = [
    "tasks",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
```

The `Task` model is defined in `tasks/models.py`.

## Using the CRUD with cURL

Start the Django server before running the following commands.

### List tasks — GET

```bash
curl http://localhost:8000/tasks/
```

Example response:

```json
[
  {
    "id": 1,
    "title": "Study Django",
    "description": "Practice Django CRUD",
    "completed": false,
    "created_at": "2026-09-16T19:00:00Z"
  }
]
```

### Create a task — POST

```bash
curl -X POST http://localhost:8000/tasks/create/ \
  -H "Content-Type: application/json" \
  -d '{"title":"Study Django","description":"Practice POST"}'
```

Example response:

```json
{
  "id": 1,
  "title": "Study Django",
  "description": "Practice POST",
  "completed": false
}
```

### Update a task — PUT

Replace `1` with the ID of the task you want to update.

```bash
curl -X PUT http://localhost:8000/tasks/1/ \
  -H "Content-Type: application/json" \
  -d '{"completed":true}'
```

You can also update other fields:

```bash
curl -X PUT http://localhost:8000/tasks/1/ \
  -H "Content-Type: application/json" \
  -d '{"title":"Study Docker","description":"Updated task","completed":true}'
```

### Delete a task — DELETE

Replace `1` with the ID of the task you want to delete.

```bash
curl -X DELETE http://localhost:8000/tasks/1/delete/
```

Example response:

```json
{
  "message": "Task deleted successfully"
}
```

## Using the CRUD with Django Admin

Django Admin provides a web interface for creating, reading, updating, and deleting tasks.

### 1. Task model in Django Admin

The `Task` model is already registered in Django Admin in this repository, so you do not need to configure this manually after cloning the project.

The configuration is located in `tasks/admin.py`:

```python
from django.contrib import admin
from .models import Task

admin.site.register(Task)
```

`from .models import Task` imports the `Task` model from the same Django app, and `admin.site.register(Task)` registers it with Django Admin. This is what makes the `Task` model appear in the `/admin/` interface and allows tasks to be created, viewed, edited, and deleted there.

### 2. Create a superuser with Docker

Run:

```bash
docker run --rm -it -v "$PWD":/app django-crud python manage.py createsuperuser
```

The command will ask for:

```text
Username:
Email address:
Password:
Password (again):
```

The `-it` option keeps the terminal interactive so you can answer these prompts.

### 3. Start the server

```bash
docker run --rm -p 8000:8000 -v "$PWD":/app django-crud python manage.py runserver 0.0.0.0:8000
```

### 4. Open Django Admin

Open:

```text
http://localhost:8000/admin/
```

Log in with the superuser credentials you created. If `Task` is registered correctly, the `Tasks` section will appear in the admin panel.

From there you can:

- create tasks;
- view existing tasks;
- edit tasks;
- delete tasks.

## Development

Because the project directory is mounted into the container with:

```bash
-v "$PWD":/app
```

changes made to the source code on your computer are immediately available inside the container. You do not need to rebuild the image after every code change.

Rebuild the image when you change something that belongs to the image itself, such as:

- `Dockerfile`;
- Python dependencies;
- `requirements.txt`;
- system packages installed by the image.

Rebuild with:

```bash
docker build -t django-crud .
```

## Useful Commands

Open the Django shell:

```bash
docker run --rm -it -v "$PWD":/app django-crud python manage.py shell
```

Create migrations:

```bash
docker run --rm -v "$PWD":/app django-crud python manage.py makemigrations
```

Apply migrations:

```bash
docker run --rm -v "$PWD":/app django-crud python manage.py migrate
```

Start the server:

```bash
docker run --rm -p 8000:8000 -v "$PWD":/app django-crud python manage.py runserver 0.0.0.0:8000
```
