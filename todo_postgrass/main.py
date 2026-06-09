from fastapi import FastAPI
from database import engine
from models.model import Base

app = FastAPI()
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"Hello": "World"}



