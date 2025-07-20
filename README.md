# 🎂 DelightAPI - Cake Management System

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

## Authentication

| Method | Endpoint              | Access        | Description              |
| ------ | --------------------- | ------------- | ------------------------ |
| POST   | `/api/auth/register/` | Public        | Register a new user      |
| POST   | `/api/auth/login/`    | Public        | Login and get auth token |
| POST   | `/api/auth/logout/`   | Authenticated | Logout and delete token  |
| GET    | `/api/auth/user/`     | Authenticated | Get current user info    |


