# 🎂 DelightAPI - Cake Management System
![Python](https://img.shields.io/badge/Python-3.10-blue)
![Django](https://img.shields.io/badge/Django-5.0-green)
![DRF](https://img.shields.io/badge/DRF-3.14-orange)
![Swagger](https://img.shields.io/badge/Swagger-Enabled-brightgreen)

A Django REST API for managing cakes and user authentication.

---

## 🚀 Features

- User Registration, Login, Logout with Token Authentication
- Create, Read, Update, Delete (CRUD) Cakes
- Django Admin Dashboard for staff/superuser
- Token-based Authentication using Django REST Framework

---

## 🔧 Setup Instructions

### 1. Clone the repository (if applicable)

```bash
git clone https://github.com/Sathvika1209/delightapi.git
cd delightapi
```

### 2. Create Virtual Environment (Optional)
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On Linux/macOS
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
or manually install

```bash
pip install django djangorestframework
pip install djangorestframework-simplejwt
```

### 4. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser
```bash
python manage.py createsuperuser
```

### 6. Run the Server
```bash
python manage.py runserver
```

### 7. Access the API Admin
http://127.0.0.1:8000/admin/


## Project Structure

```
delightapi/
├── cakes/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   └── ...
├── delightapi/
│   ├── settings.py
│   └── urls.py
├── manage.py
└── README.md
```

## Authentication API

| Method | Endpoint              | Access        | Description              |
| ------ | --------------------- | ------------- | ------------------------ |
| POST   | `/api/auth/register/` | Public        | Register a new user      |
| POST   | `/api/auth/login/`    | Public        | Login and get auth token |
| POST   | `/api/auth/logout/`   | Authenticated | Logout and delete token  |
| GET    | `/api/auth/user/`     | Authenticated | Get current user info    |


## 📘 API Documentation

The DelightAPI backend provides full REST API documentation for developers and testers.

### 🔗 Swagger UI
Interactive documentation with support for testing endpoints directly in the browser.

- URL: [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)

### 📕 ReDoc
Clean, structured documentation view (read-only).

- URL: [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)

---

## 📦 Postman Collection

You can import the Postman collection file to test all available API endpoints easily.

- File: `delightapi-postman-collection.json` (available in the root or docs folder)

To import into Postman:
1. Open Postman
2. Click **Import**
3. Choose the `.json` file
4. Start testing the endpoints!

---

## ✅ Available Endpoints

Here's a quick summary of key endpoints (full details in Swagger):

| Method | Endpoint                 | Description                     | Auth Required |
|--------|--------------------------|---------------------------------|----------------|
| POST   | `/api/auth/register/`    | Register new user               | ❌ No          |
| POST   | `/api/auth/login/`       | Login & get token               | ❌ No          |
| POST   | `/api/auth/logout/`      | Logout user                     | ✅ Yes         |
| GET    | `/api/auth/user/`        | Get user profile                | ✅ Yes         |
| PUT    | `/api/auth/update/`      | Update user profile             | ✅ Yes         |
| PUT    | `/api/auth/change-password/` | Change user password      | ✅ Yes         |
| DELETE | `/api/auth/delete/`      | Delete user account             | ✅ Yes         |

---

## 💡 Notes

- Make sure to include `Authorization: Token <your_token>` in headers for authenticated endpoints.
- All API docs are auto-generated using **drf-yasg** (Swagger for Django REST Framework).

---
