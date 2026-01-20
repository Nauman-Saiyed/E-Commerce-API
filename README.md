# 🛒 E-Commerce API (FastAPI + MongoDB)

A production-ready **E-Commerce Backend API** built using **FastAPI**, **MongoDB (Motor)**, and **JWT Authentication**. This project follows clean architecture, async best practices, and real-world backend patterns.

---

## 🚀 Features

### 🔐 Authentication & Authorization

* Email & Password Login
* JWT-based Authentication
* OTP-based Login (Phone)
* Protected Routes

### 👤 User Management

* User CRUD
* Secure password hashing
* Soft delete support

### 🗂 Category Management

* Category CRUD
* Auto-generated slug
* Soft delete

### 📦 Product Management

* Product CRUD
* Category relationship
* Tags & images
* Slug auto-generation

### 🧾 Order Management

* Place order (Auth required)
* Order status update
* Enum-based order status
* Auto price & total calculation

### 🧱 Common Architecture

* MongoDB ObjectId usage
* Common fields in all collections:

  * `_id`
  * `created_at`
  * `updated_at`
  * `deleted_at`

---

## 🧑‍💻 Tech Stack

* **Python 3.10+**
* **FastAPI**
* **MongoDB + Motor (Async)**
* **Pydantic**
* **JWT (python-jose)**
* **Uvicorn**

---

## 📁 Project Structure

```text
app/
├── core/
│   ├── config.py
│   ├── database.py
│   └── security.py
│
├── middleware/
│   └── auth.py
│
├── models/
│   ├── user.py
│   ├── category.py
│   ├── product.py
│   └── order.py
│
├── routes/
│   ├── auth.py
│   ├── users.py
│   ├── categories.py
│   ├── products.py
│   └── orders.py
│
├── schemas/
│   ├── auth.py
│   ├── user.py
│   ├── category.py
│   ├── product.py
│   └── order.py
│
└── main.py
```

---

## ⚙️ Environment Variables

Create a `.env` file in the root directory:

```env
APP_NAME=E-Commerce API
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=ecommerce_db
```

---

## ▶️ How to Run Locally

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/E-Commerce-API.git
cd E-Commerce-API
```

### 2️⃣ Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the server

```bash
uvicorn app.main:app --reload
```

Server will start at:

```
http://127.0.0.1:8000
```

---

## 📘 API Documentation

FastAPI provides interactive docs:

* **Swagger UI** → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **ReDoc** → [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🔐 Authentication Flow

1. Register User
2. Login with Email/Password or OTP
3. Receive JWT Token
4. Use token in headers:

```http
Authorization: Bearer <access_token>
```

---

## 🧪 Testing

Manual testing via:

* Swagger UI
* Postman

(Automated tests can be added using **pytest**)

---

## 🌱 Future Improvements

* Role-based access (Admin/User)
* Pagination & filtering
* Docker support
* Refresh tokens
* Payment gateway integration

---

## 👨‍💻 Author

**Nauman Saiyed**
Backend Developer | FastAPI | MongoDB

---

## ⭐️ Support

If you like this project, give it a ⭐ on GitHub!
