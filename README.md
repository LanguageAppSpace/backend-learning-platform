# Learning Platform – Backend (Django + Docker)

## Overview

This repository contains the backend for the **Learning Platform**, built with **Django** and **Django REST Framework (DRF)**. The application is fully containerized using **Docker** and **Docker Compose**, making local development setup fast and consistent across environments.

The backend provides APIs for user authentication and flashcard-based learning, including progress tracking.

---

## Tech Stack

* **Python** 3.11
* **Django** & **Django REST Framework**
* **MySQL 8.0** (Dockerized)
* **Docker & Docker Compose**
* **Swagger / OpenAPI**

---

## Prerequisites

Make sure you have the following installed:

* Docker (>= 20.x)
* Docker Compose (v2 recommended)
* Git

You do **not** need Python installed locally when using Docker.

---

## Project Structure (simplified)

```text
.
├── backend/
│   ├── Dockerfile.dev
│   ├── django-setup.sh
│   ├── manage.py
│   └── ...
├── docker-compose.dev.yaml
├── .env.example
└── README.md
```

---

## Environment Variables

Create a `.env` file in the project root (next to `docker-compose.dev.yaml`).

You can use the following template as a starting point:

```env
# Django
DJANGO_ENV=development
DJANGO_SECRET_KEY=change-me
DEBUG=True

# Database (MySQL)
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_ROOT_PASSWORD=
DB_HOST=db
DB_PORT=3306

# MySQL container vars
MYSQL_ROOT_PASSWORD=
MYSQL_DATABASE=
MYSQL_PASSWORD=

# App
PORT=8080
```

⚠️ **Never commit real secrets to the repository.**

---

## Running the Project (Docker – Recommended)

### 1. Clone the repository

```bash
git clone <repository-url>
cd backend-learning-platform
```

### 2. Create `.env`

```bash
cp .env.example .env
```

Update values as needed.

### 3. Build the containers

```bash
docker compose -f docker-compose.dev.yaml build
```

### 4. Start the application

```bash
docker compose -f docker-compose.dev.yaml up
```

The application will be available at:

* **Backend API**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
* **Swagger UI**: [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)

---

## What Happens on Startup

The `web` container runs `django-setup.sh`, which typically:

* waits for the database to be ready
* applies migrations
* starts the Django development server

(See `backend/django-setup.sh` for exact behavior.)

---

## Running Django Commands

Run Django management commands inside the `web` container:

```bash
docker compose -f docker-compose.dev.yaml exec web python manage.py migrate
```

Create a superuser:

```bash
docker compose -f docker-compose.dev.yaml exec web python manage.py createsuperuser
```

Run tests:

```bash
docker compose -f docker-compose.dev.yaml exec web python manage.py test
```

---

## Database

* **Engine**: MySQL 8.0
* **Container name**: `mysql_container`
* **Port (local)**: `3306`
* **Data persistence**: Docker volume `mysql_data`

Database data will persist between container restarts.

---

## API Documentation

Interactive API documentation is available via Swagger:

* [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)

---

## License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.
