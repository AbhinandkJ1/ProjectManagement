# Project Management System

## Overview

This project is a Project Management System built with Django. It includes models for users, projects, tasks, milestones, and notifications. 
The system supports role-based access control, token-based authentication, and provides real-time notifications. 
Additionally, it utilizes Celery for asynchronous tasks.

## Setup

### Prerequisites

- Python 3.x
- Django
- Celery
- Redis (for Celery message broker)
- SQLite (for database)

### Installation

1. **Clone the repository**:
    ```
    git clone https://github.com/AbhinandkJ1/ProjectManagement.git

    ```
2. **Create a virtual environment**:

3. **Install dependencies**:
    ```
    pip install -r requirements.txt
    ```

4. **Set up the database**:
    - Configure your database settings in `settings.py`.
    - Run migrations:
      ```
      python manage.py migrate
      ```

5. **Create a superuser**:
    ```
    python manage.py createsuperuser
    ```

6. **Run the development server**:
    ```
    python manage.py runserver
    ```

7. **Start the Celery worker**:
    ```
    celery -A projectmanagement worker --loglevel=info
    ```

### Configuration

- **Environment Variables**: Use a `.env` file to set environment-specific settings such as database celery, email and redis.
- **Celery Configuration**: Ensure Celery and Redis configurations are properly set in `settings.py`.


