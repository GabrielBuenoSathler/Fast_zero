from fastapi import FastAPI
from http import HTTPStatus
from fastapi.responses import HTMLResponse
from fast_zero.schemas import Message, UserSchema, UserPublic, UserDB

app = FastAPI()
database = []


@app.get('/', response_class=HTMLResponse)
def read_root():
    return """
    <html>
      <head>
        <title> Nosso olá mundo!</title>
      </head>
      <body>
        <h1> Olá Mundo </h1>
      </body>
    </html>"""


@app.get('/home', response_class=HTMLResponse)
def home():
    return """
    <html>
      <head>
        <title> Nossa home</title>
      </head>
      <body>
        <h1> Olá home </h1>
      </body>
    </html>"""


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=len(database) + 1)
    database.append(user_with_id)
    return user_with_id
from fastapi import FastAPI, HTTPException


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
    if user_id > len(database) or user_id < 1: 
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        ) 

    user_with_id = UserDB(**user.model_dump(), id=user_id)
    database[user_id - 1] = user_with_id 

    return user_with_id
