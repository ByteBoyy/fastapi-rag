
# 🚀 FastAPI AI-RAG Microservice

## ✨ Overview
This is a full-featured FastAPI microservice that supports:
- ✅ JWT Authentication & User Management
- ✅ Role-Based Access Control (RBAC) using Oso
- ✅ PDF Upload & Retrieval-Augmented Generation (RAG) with OpenAI
- ✅ MongoDB (via PyMongo) for storage
- ✅ Qdrant Vector Database for document chunk storage
- ✅ Pytest-based testing framework

---

## 📂 Folder Structure
```
app/
├── auth/                  # JWT auth handlers
├── config.py              # Environment & app settings
├── crud/                  # User CRUD operations
├── database.py            # MongoDB connection
├── gpt_response/          # OpenAI GPT query handling
├── main.py                # FastAPI entrypoint
├── models/                # User & Resource models
├── oso_rbac/              # Oso RBAC setup and policy
├── prompts/               # System prompt for AI
├── routes/                # API route handlers
├── services/              # PDF processor and RAG service
└── tests/                 # Pytest test files
```

---

## ⚙ Setup Instructions

### 1. 📥 Clone the Repository
```bash
git clone <your-repo-url>
cd fastapi_rag_service
```

### 2. 🐍 Create and Activate Virtual Environment
```bash
conda create -n fastapi_rag_env python=3.10 -y
conda activate fastapi_rag_env
```

### 3. 📦 Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. 📁 Setup .env File
Create a `.env` file in root with the following values:
```
MONGO_URI=<your_mongodb_connection_uri>
DB_NAME=fastapi_rag
QDRANT_HOST=localhost
QDRANT_PORT=6333
OPENAI_API_KEY=your_openai_api_key
SECRET_KEY=your_secret_key
```

---

## ▶ Run the App
```bash
uvicorn app.main:app --reload
```

Open docs at [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🔐 Authentication

### User Registration
``POST /users/register``

### User Login
``POST /users/login`` → Returns JWT access token

Use this token in all secure endpoints:
```
Authorization: Bearer <access_token>
```

---

## 🔐 RBAC Testing Instructions

### ✅ Roles Supported:
- `user`
- `admin`

Use MongoDB or API to assign role values to your users.

### Default Permissions:
| Endpoint | Action | Role Allowed |
|---------|--------|----------------|
| `/users/me` | `read` | user ✅, admin ✅ |
| `/users/delete` | `manage` | admin ✅ only |
| `/rag/query` | `read` | user ✅, admin ✅ |
| `/rag/upload` | `manage` | admin ✅ only |

> 🔸 **Test these roles by registering a user and manually updating their `role` field in MongoDB.**

Example:
```js
db.users.updateOne({username: "john"}, { $set: { role: "admin" } })
```

---

## 🧪 Run Tests
```bash
pytest app/tests/test_all_endpoints.py
```

---

## 👥 Predefined Test Roles
You can test access control using the following roles:
- **`admin`** → Full access to all endpoints including upload & delete
- **`user`** → Can only query and access own profile

---

## 📌 Notes
- All sensitive routes are protected via Oso RBAC.
- `AppResource(name="profile")`, `AppResource(name="rag_query")`, `AppResource(name="rag_upload")` are used to enforce permission logic.
- Policy is located at `app/oso_rbac/oso_policy.py`

---

## 📃 License
MIT License

