# Django-crud
Backend project built with Django and Docker.

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
- `.` tells Docker to use the current directory as the build context.

### 3. Run database migrations

```bash
docker run --rm -v "$PWD":/app django-crud python manage.py migrate
```

This command:

- `--rm` removes the container after the command finishes.
- `-v "$PWD":/app` mounts the current project directory inside the container.
- `django-crud` is the Docker image.
- `python manage.py migrate` creates and updates the Django database tables.

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

## Creating a Django App

To create a new Django app:

```bash
docker run --rm -v "$PWD":/app django-crud python manage.py startapp app
```

Replace `app` with the name of the Django app you want to create.

## Development

Because the project directory is mounted into the container, changes made to the source code on your computer are available inside the container without rebuilding the image.

If you change dependencies or the `Dockerfile`, rebuild the image:

```bash
docker build -t django-crud .
```
