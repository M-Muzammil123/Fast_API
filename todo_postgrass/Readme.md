# Todo PostgreSQL API

A FastAPI-based Todo application using PostgreSQL, SQLAlchemy, Alembic, and Poetry for dependency management.

## Prerequisites

Before running the application, make sure the following tools are installed:

* Python 3.10+
* PostgreSQL
* Poetry

---

# Installation

## 1. Clone the Repository

```bash
git clone <repository-url>
cd todo_postgrass
```

## 2. Install Project Dependencies

```bash
poetry install
```

---

# Database Setup

## 1. Install SQLAlchemy

```bash
poetry add sqlalchemy
```

## 2. Create Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://user:password@localhost/dbname
```

Example:

```env
DATABASE_URL=postgresql://postgres:password@localhost/todo_db
```

---

## 3. Configure Database Settings

In `config.py`:

```python
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
```

---

## 4. Define Database Models

Create your SQLAlchemy models inside the `models` folder.

Example:

```python
from sqlalchemy import Column, Integer, String
from app.database import Base

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
```

---

# Alembic Migration Setup

## 1. Install Required Packages

```bash
poetry add alembic
poetry add psycopg2
poetry add python-dotenv
```

If you're using macOS and encounter psycopg2 build errors:

```bash
poetry add psycopg2-binary
```

---

## 2. Initialize Alembic

```bash
poetry run alembic init alembic
```

This creates:

```text
alembic/
├── versions/
├── env.py
alembic.ini
```

---

## 3. Configure Alembic

Update the database URL in `alembic.ini`:

```ini
sqlalchemy.url = postgresql://user:password@localhost/dbname
```

Or load it dynamically from `.env` inside `env.py`.

---

## 4. Configure Metadata in env.py

```python
from app.database import Base
from app.models import *

target_metadata = Base.metadata
```

---

# Create and Apply Migrations

## Generate Migration

```bash
poetry run alembic revision --autogenerate -m "Initial migration"
```

## Apply Migration

```bash
poetry run alembic upgrade head
```

---

# Run the Application

Start the FastAPI server:

```bash
poetry run uvicorn app.main:app --reload
```

Application URL:

```text
http://127.0.0.1:8000
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

ReDoc Documentation:

```text
http://127.0.0.1:8000/redoc
```

---

# Useful Alembic Commands

### Create a New Migration

```bash
poetry run alembic revision --autogenerate -m "Add new table"
```

### Upgrade Database

```bash
poetry run alembic upgrade head
```

### Downgrade One Migration

```bash
poetry run alembic downgrade -1
```

### View Migration History

```bash
poetry run alembic history
```

### Check Current Version

```bash
poetry run alembic current
```

---

# Project Structure

```text
todo_postgrass/
├── alembic/
│   └── versions/
├── app/
│   ├── config.py
│   ├── database.py
│   ├── models/
│   └── main.py
├── .env
├── alembic.ini
├── pyproject.toml
└── README.md
```

---

# Tech Stack

* FastAPI
* PostgreSQL
* SQLAlchemy
* Alembic
* Poetry
* Python Dotenv
* Uvicorn
