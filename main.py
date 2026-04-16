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
