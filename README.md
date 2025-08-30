# Task Manager API (Capstone Project)

## Overview
A simple Django REST API for managing tasks with authentication, task ownership, filtering, and sorting.

## Features
- JWT Authentication (login/register)
- Task CRUD (create, read, update, delete)
- Mark tasks complete/incomplete with timestamps
- Filtering by status, priority, and due date
- Sorting by due date or priority
- Permissions: users only access their own tasks

## Setup

### Installation
```bash
git clone <repo-url>
cd <project-dir>
pip install -r requirements.txt
