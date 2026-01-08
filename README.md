# 📸 FastAPI Gram

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688)
![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B)
![SQLAlchemy](https://img.shields.io/badge/ORM-SQLAlchemy-red)

A simple social media application (Instagram clone) created to learn the **FastAPI** framework. The project handles the full user registration and login process (JWT), file uploads (photos), and displaying them in a feed.

## 🚀 Features

### For the User:
* 🔐 **Registration & Login:** Secure authentication using JWT.
* 📤 **Photo Upload:** Uploading image files with captions.
* 🖼️ **Feed:** Browsing the latest posts from all users.
* 🗑️ **Management:** Ability to delete your own posts.

### Technology Stack:
* **Backend:** FastAPI (Async endpoints)
* **Database:** SQLite (for simplicity) + SQLAlchemy (Async)
* **Frontend:** Streamlit (Python Interface)
* **Auth:** FastAPI Users (Bearer Token + JWT Strategy)
* **Files:** Local storage in the `uploads/` folder

---

## 🛠️ Installation and Setup

1. Cloning and Environment
It is recommended to use a virtual environment (`venv`) to keep the system clean.

Clone the repository (if downloading from GH) or enter the folder
```text
cd your-folder-name
```

Create a virtual environment
```text
python -m venv .venv
```

Activate the environment:

```text
# Windows:
.venv\Scripts\activate
```

```text
# Linux/Mac:
source .venv/bin/activate
```

2. Install Dependencies
Install all libraries defined in pyproject.toml.
```text
pip install .
```

3. Run Backend (Server)
The server will start on port 8000. Upon the first run, it will automatically create the test.db database file and the uploads folder.
```text
uvicorn src.app:app --reload
```
📄 API Documentation (Swagger): http://127.0.0.1:8000/docs

4. Run Frontend
In a new terminal window (remember to activate .venv there as well), launch the interface:

Bash

streamlit run frontend.py

```text
📂 Project Structure
├── src/
│   ├── app.py       # Main application file, FastAPI config, and endpoints
│   ├── db.py        # Database models and SQLAlchemy configuration
│   ├── schemas.py   # Pydantic schemas (input/output data validation)
│   └── users.py     # Authentication logic and user manager
├── uploads/         # Folder for uploaded photos (created automatically)
├── frontend.py      # User interface in Streamlit
├── pyproject.toml   # Project dependencies list
└── test.db          # SQLite database file (created automatically)
```
## 📝 License 
Project created for educational purposes.
