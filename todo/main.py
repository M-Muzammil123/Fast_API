from datetime import datetime, timezone
from typing import List
# pyrefly: ignore [missing-import]
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

# Import our helper modules and database schema
import schemas
import models
from databas import get_db
from auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    decode_access_token
)

app = FastAPI(
    title="Todo SaaS API",
    description="FastAPI Todo application with JWT authentication and PostgreSQL backend",
    version="1.0.0"
)

# Enable CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OAuth2 scheme using standard bearer token auth
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> models.User:
    """
    FastAPI dependency to extract and validate the JWT from the request header,
    retrieving the corresponding user from the database.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
        
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
        
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception
        
    return user


@app.get("/")
def read_root():
    """
    Public root endpoint with a welcome message.
    """
    return {"message": "Welcome to the FastAPI Todo SaaS API!"}


# --- Authentication Routes ---

@app.post("/api/v1/auth/register", status_code=status.HTTP_201_CREATED)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user. Hashes the password and generates an initial JWT token.
    """
    # Check if user already exists
    existing_user = db.query(models.User).filter(models.User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
        
    # Hash password and create user
    hashed_password = get_password_hash(user_in.password)
    timestamp = int(datetime.now(timezone.utc).timestamp())
    
    db_user = models.User(
        email=user_in.email,
        password=hashed_password,
        created_at=timestamp
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Generate token
    access_token = create_access_token(data={"sub": db_user.email})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": db_user.id,
            "email": db_user.email,
            "created_at": db_user.created_at
        }
    }


@app.post("/api/v1/auth/login")
def login(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Authenticate user by email and password, returning a JWT token on success.
    """
    user = db.query(models.User).filter(models.User.email == user_in.email).first()
    if not user or not verify_password(user_in.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )
        
    # Generate token
    access_token = create_access_token(data={"sub": user.email})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "created_at": user.created_at
        }
    }


@app.get("/api/v1/auth/users/me", response_model=schemas.UserResponse)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    """
    Get information about the currently authenticated user.
    """
    return current_user


# --- Todo Routes ---

@app.post("/api/v1/todos", response_model=schemas.TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(
    todo_in: schemas.TodoCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new Todo item owned by the authenticated user.
    """
    timestamp = int(datetime.now(timezone.utc).timestamp())
    db_todo = models.Todo(
        title=todo_in.title,
        description=todo_in.description,
        completed=todo_in.completed,
        created_at=timestamp,
        owner_id=current_user.id
    )
    
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


@app.get("/api/v1/todos", response_model=List[schemas.TodoResponse])
def list_todos(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Retrieve all Todo items belonging to the authenticated user.
    """
    todos = db.query(models.Todo).filter(models.Todo.owner_id == current_user.id).all()
    return todos
