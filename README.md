## FoodApp API

A production-style RESTful backend built with Django REST Framework.
The project demonstrates secure authentication, REST architecture,
database design, automatic API documentation, filtering,
pagination, search, and CRUD operations.

## Features

# Authentication

- JWT-based authentication
- Access and refresh token workflow
- Protected API endpoints
- Secure user authentication using `djangorestframework-simplejwt`

Implemented endpoints:

| Method | Endpoint | Description |
|---|---|---|
| POST | `/foodapp/api/token/` | Obtain access and refresh tokens |
| POST | `/foodapp/api/token/refresh/` | Refresh access token |

---

# Food Item Management

Users can manage food items through a complete CRUD API.

Features:

- Create food items
- Retrieve item lists
- Retrieve individual items
- Update existing items
- Delete items
- Search items
- Order results
- Pagination support
- Image URL support

Endpoints:

| Method | Endpoint | Description |
|-|-|-|
| GET | `/foodapp/api/items/` | List all food items |
| POST | `/foodapp/api/items/` | Create a new item |
| GET | `/foodapp/api/items/{id}/` | Retrieve item details |
| PUT | `/foodapp/api/items/{id}/` | Update item |
| PATCH | `/foodapp/api/items/{id}/` | Partial update |
| DELETE | `/foodapp/api/items/{id}/` | Delete item |

---

# Order Management

The order system allows users to manage customer orders.

Features:

- Create orders
- Retrieve order history
- Update orders
- Delete orders
- Automatic timestamps
- User-order relationships
- Connected food items

Endpoints:

| Method | Endpoint | Description |
|-|-|-|
| GET | `/foodapp/api/orders/` | List orders |
| POST | `/foodapp/api/orders/` | Create order |
| GET | `/foodapp/api/orders/{id}/` | Retrieve order |
| PUT | `/foodapp/api/orders/{id}/` | Update order |
| PATCH | `/foodapp/api/orders/{id}/` | Partial update |
| DELETE | `/foodapp/api/orders/{id}/` | Delete order |

---



## Architecture

                    Client
                       │
         Authorization: Bearer JWT
                       │
                       ▼
              Django REST Framework
                       │
         ┌─────────────┼──────────────┐
         ▼             ▼              ▼
   Authentication  ViewSets     Permissions
         │             │
         ▼             ▼
      Serializers ──► Models
                       │
                       ▼
                  PostgreSQL



## API Documentation

The project uses:
- OpenAPI 3.0
- drf-spectacular
- Swagger UI
- ReDoc

Interactive documentation:
/api/schema/
/api/docs/
/api/redoc/


## Tech Stack
- Python
- Django 6.0
- Django REST Framework
- JWT
- Simple JWT
- PostgreSQL
- Django ORM
- Psycopg 3
- drf-spectacular
- OpenAPI 3.0
- django-filter
- Pillow
- python-dotenv



## Installation

git clone https://github.com/yourusername/FoodApp.git
cd FoodApp

venv\Scripts\activate
pip install -r requirements.txt

create .env file and paste it:
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_NAME=foodapp
DATABASE_USER=postgres
DATABASE_PASSWORD=password
DATABASE_HOST=localhost
DATABASE_PORT=5432

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

API available at: http://127.0.0.1:8000/
