TechForing Project

Description

TechForing is a project management application that helps users create and manage projects, assign tasks, add comments, and manage user roles within projects. It leverages Django and Django REST Framework to provide a backend for handling users, projects, tasks, and comments.

Prerequisites
Make sure you have the following software installed:
Python 3.13.0
Pip (Python package manager)

Django 4.0+

Django REST Framework

PostgreSQL/MySQL/SQLite (or any other database you prefer)

Setup Instructions

1. Clone the Repository

Clone the project from GitHub:
git clone https://github.com/akjabir/techforing_project/tree/jabir/
cd techforing

2. Create and Activate a Virtual Environment

It is recommended to use a virtual environment:

python -m venv venv
source venv/bin/activate 
*but project didn,t use virtual environment*
3. Install Dependencies

Install the required dependencies:
4. Configure Database Settings

In your settings.py file, configure your database connection. If you're using SQLite (default for Django), the configuration looks like this:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

5. Run Database Migrations

Apply the migrations to create the necessary database tables:
python manage.py createsuperuser
Follow the prompts to set up the username, email, and password.
7. Run the Development Server
Start the Django development server:
python manage.py runserver
Now you can access the application at http://127.0.0.1:8000/ in your browser.

Database Schema

Users Table

id: Primary Key

username: String (Unique)

email: String (Unique)

password: String

first_name: String

last_name: String

date_joined: DateTime

Projects Table

id: Primary Key

name: String

description: Text

owner: Foreign Key (to Users)

created_at: DateTime

Project Members Table

id: Primary Key

project: Foreign Key (to Projects)

user: Foreign Key (to Users)

role: String (Admin, Member)

Tasks Table

id: Primary Key

title: String

description: Text

status: String (To Do, In Progress, Done)

priority: String (Low, Medium, High)

assigned_to: Foreign Key (to Users, nullable)

project: Foreign Key (to Projects)

created_at: DateTime

due_date: DateTime

Comments Table

id: Primary Key

content: Text

user: Foreign Key (to Users)

task: Foreign Key (to Tasks)

created_at: DateTime
REST API Endpoints

Now model create as Database Plan

Users

Register User: POST /api/users/register/

Login User: POST /api/users/login/

Get User Details: GET /api/users/{id}/

Update User: PUT/PATCH /api/users/{id}/

Delete User: DELETE /api/users/{id}/

Projects

List Projects: GET /api/projects/

Create Project: POST /api/projects/

Retrieve Project: GET /api/projects/{id}/

Update Project: PUT/PATCH /api/projects/{id}/

Delete Project: DELETE /api/projects/{id}/

Tasks

List Tasks: GET /api/projects/{project_id}/tasks/

Create Task: POST /api/projects/{project_id}/tasks/

Retrieve Task: GET /api/tasks/{id}/

Update Task: PUT/PATCH /api/tasks/{id}/

Delete Task: DELETE /api/tasks/{id}/

Comments

List Comments: GET /api/tasks/{task_id}/comments/

Create Comment: POST /api/tasks/{task_id}/comments/

Retrieve Comment: GET /api/comments/{id}/

Update Comment: PUT/PATCH /api/comments/{id}/

Delete Comment: DELETE /api/comments/{id}/

License

Include the license details here if applicable.


