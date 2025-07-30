# 🎂 DelightAPI - Cake Management System
![Python](https://img.shields.io/badge/Python-3.10-blue)
![Django](https://img.shields.io/badge/Django-5.0-green)
![DRF](https://img.shields.io/badge/DRF-3.14-orange)
![Swagger](https://img.shields.io/badge/Swagger-Enabled-brightgreen)

DelightAPI is a RESTful backend service designed to support a cake delivery platform. It handles user authentication, cake listings, and administrative operations to streamline online cake ordering and management.



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

🎂 Cake API
| Method | Endpoint           | Description              | Auth Required |
| ------ | ------------------ | ------------------------ | ------------- |
| GET    | `/api/cakes/`      | List all cakes           | ✅ Yes         |
| POST   | `/api/cakes/`      | Add a new cake           | ✅ Yes         |
| GET    | `/api/cakes/<id>/` | Retrieve a specific cake | ✅ Yes         |
| PUT    | `/api/cakes/<id>/` | Update a cake            | ✅ Yes         |
| DELETE | `/api/cakes/<id>/` | Delete a cake            | ✅ Yes         |

---

🏬 Store API
| Method | Endpoint       | Description     | Auth Required |
| ------ | -------------- | --------------- | ------------- |
| GET    | `/api/stores/` | List all stores | ✅ Yes         |
| POST   | `/api/stores/` | Add a new store | ✅ Yes         |
| ...    | etc.           |                 |               |

---

🛒 Cart Management (User)
| Method | Endpoint                 | Description                        | Access |
| ------ | ------------------------ | ---------------------------------- | ------ |
| GET    | `/api/cart/`             | Get current user's cart            | ✅ Yes  |
| POST   | `/api/cart/add/`         | Add item to cart                   | ✅ Yes  |
| DELETE | `/api/cart/remove/<id>/` | Remove item from cart              | ✅ Yes  |
| PUT    | `/api/cart/update/<id>/` | Update item quantity/customization | ✅ Yes  |

---

## 📝 Notes

- Make sure to include `Authorization: Token <your_token>` in headers for authenticated endpoints.
- All API docs are auto-generated using **drf-yasg** (Swagger for Django REST Framework).
- Only authenticated users can interact with the Cake API.
- Use TokenAuthentication to access secured endpoints.
- Admin dashboard helps manage users, cakes, and store inventory.
- Swagger and ReDoc docs are auto-generated using drf-yasg.

---
