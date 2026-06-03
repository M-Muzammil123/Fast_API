# todo app crud operations
import os
from fastapi import FastAPI
from pymongo import MongoClient
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

client = MongoClient(os.getenv("Data_url"))
db = client["todo_db"]
collection = db["todos"]

class TodoItem(BaseModel):
   title: str
   description: str 
   completed: bool
   created_at: str

# use try exception error
@app.post("/new_todos/")
def create_todo(todo: TodoItem):
    try:
        todo_dict = todo.dict()
        result = collection.insert_one(todo_dict)
        return {
            "id": str(result.inserted_id),
            "status": "success"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
# get todo all
@app.get("/todos/")
def get_todos():
    try:
        todos = collection.find()
        return [
            {
                "id": str(todo["_id"]),
                "title": todo["title"],
                "description": todo["description"],
                "completed": todo["completed"],
                "created_at": todo["created_at"]
            }
            for todo in todos
        ]
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@app.put("/update_todo/{title}")
def update_todo(title: str, todo: TodoItem):
    try:
        result = collection.update_one({"title": title}, {"$set": todo.dict()})
        if result.modified_count > 0:
            return {
                "status": "success"
            }
        else:
            return {
                "status": "error",
                "message": "Todo not found"
            }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
