from fastapi import FastAPI

app = FastAPI()
# # simple route
@app.get("/")
def root():
    return {
        "message": "Hello, World!",
        "status": "success"
    }

# # poetry run uvicorn app:main --reload
# # routes
# @app.get("/home")
# def home():
#     return {
#         "message": "Hello from home!",
#         "status": "success"
#     }

# # path parameters
# @app.get("/users/{user_id}")
# def read_user(user_id: int):
#     return {
#         "message": f"User ID: {user_id}",
#         "status": "success"
#     }

# # query parameters
# @app.get("/items/")
# def read_item(item_id: int, q: str = None):
#     return {
#         "item_id": item_id,
#         "q": q
#     }


# @app.post("/items/")
# def read_item(item_id:int, q:str):
#     try:
#         item_id = int(item_id)
#     except Exception as e:
#         return {
#             "error": str(e),
#             "message": "Invalid item_id"
#         }
#     return {
#         "item_id": item_id,
#         "q": q
#     }
 


@app.get("/")
def read_root():
    return {
        "message": "Hello, World!",
        "status": "success"
    }


# path parameters
@app.get("/users/{user_id}")
def read_user(user_id: int):
   return {
       "user_id": user_id,
    #   "image": data:image/png;base64,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,

       "name": "Ali",
       "email": "abc@gmail.com",
       "status": "success"

   }

# query parameters
@app.get("/users/")
def read_user(user_id: int, user_name: str):
   return {
       "user_id": user_id,
       "name": user_name,
       "email": "abc@gmail.com",
       "status": "success"
   }
# path parameters
# http://127.0.0.1:8000/users/4

# query parameters
# http://127.0.0.1:8000/users/?user_id=4&user_name=ali


# https://www.pinterest.com. /

# https://www.pinterest.com/pin/1021894971820017771/
# https://www.pinterest.com/pin/957648308271045467/


