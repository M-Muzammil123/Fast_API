from fastapi import FastAPI

app = FastAPI()
# simple route
@app.get("/")
def root():
    return {
        "message": "Hello, World!",
        "status": "success"
    }

# poetry run uvicorn app:main --reload
# routes
@app.get("/abc")
def abc():
    return {
        "message": "Hello from abc!",
        "status": "success"
    }

# path parameters
@app.get("/users/{user_id}")
def read_user(user_id: int):
    return {
        "message": f"User ID: {user_id}",
        "status": "success"
    }
