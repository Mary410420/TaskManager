# TaskManager API

A Django REST Framework-based Task Management API that allows users to manage tasks efficiently, including creating, updating, deleting, and marking tasks as complete or incomplete. Each user has their own private task list, with robust authentication and task ownership enforcement.

---

## Features

- User registration, authentication (JWT), and management
- Task CRUD operations (Create, Read, Update, Delete)
- Task completion workflow with timestamp (`completed_at`)
- Task filtering by status, priority, and due date
- Task sorting by due date
- Permissions: users can only access their own tasks
- RESTful API design
- Deployment-ready for PythonAnywhere or other cloud hosting

---

## Tech Stack

- Python 3.10
- Django 5.x
- Django REST Framework
- Django Filters
- Simple JWT (`djangorestframework-simplejwt`)
- PythonAnywhere (deployment)

---

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Mary410420/TaskManager
   cd TaskManager

2. **Create a virtual environment:**
    ```bash
    python -m venv venv
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt

4. **Apply migrations:**
    ```bash
    python manage.py migrate


4. **Apply migrations:**
    ```bash
    python manage.py createsuperuser


4. **Apply migrations:**
    ```bash
    python manage.py runserver

---

## API Endpoints

- Base URL (local): http://127.0.0.1:8000/api/
- Base URL (deployed): https://maryolu.pythonanywhere.com/api/

---

## Authentication

- Register: POST /api/auth/register/
- Login / JWT: POST /api/token/
- Refresh token: POST /api/token/refresh/

---

## Tasks

- GET /api/tasks/ – List all tasks for the logged-in user
- POST /api/tasks/ – Create a new task
- GET /api/tasks/{id}/ – Retrieve a specific task
- PUT /api/tasks/{id}/ – Update a task (cannot update completed tasks unless reverted to pending)
- DELETE /api/tasks/{id}/ – Delete a task
- POST /api/tasks/{id}/complete/ – Mark a task as complete
- POST /api/tasks/{id}/incomplete/ – Revert a completed task to pending

---

## Users

- GET /api/users/ – List all users (admin only)
- GET /api/users/{id}/ – Retrieve a specific user
- PUT /api/users/{id}/ – Update user (admin or self)
- DELETE /api/users/{id}/ – Delete user (admin or self)


---

## Postman Quick Start

- Register a user
- Obtain JWT token
- Add Bearer token to Authorization header
- Test tasks endpoints – create, list, update, delete, complete/incomplete

---

## Deployment

- Create a PythonAnywhere account
- Set up a virtualenv and install dependencies
- Set up WSGI configuration
- Apply migrations and create a superuser
- Access API at https://<username>.pythonanywhere.com/api/

---

## Major Project Structure

    ```bash
    TaskManager/
    ├── core/
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── tasks/
    │   ├── models.py
    │   ├── views.py
    │   ├── serializers.py
    │   └── permissions.py
    ├── manage.py
    └── requirements.txt

---

## Future Enhancements (Maybe one day)

- Task Categories (Work, Personal)
- Recurring tasks
- Collaborative tasks with shared access

---