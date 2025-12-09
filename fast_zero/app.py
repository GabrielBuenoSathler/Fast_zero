from fastapi import FastAPI 
from fast_zero.schema import UserSchema, UserPublic,Token,UserList, BookSchema,BookPublic
from http import HTTPStatus
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import Depends, FastAPI, HTTPException
from fast_zero.database import get_session
from fast_zero.models import User,Book 
from fast_zero.security import get_password_hash,verify_password,create_access_token,get_current_user
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm

from fast_zero.routers import users
from fast_zero.schema import Message

app = FastAPI()

app.include_router(users.router)
 


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # depois coloque a URL exata do seu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
                                                                                                                   
@app.get('/')                                                                                                              
def read_root():                                                                                                           
    return {'message': 'Olá Mundo!'}                                                                                       
                                                                                                                                                        
                             


@app.post('/token', response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 


    session: Session = Depends(get_session),
):
    user = session.scalar(select(User).where(User.email == form_data.username)) 



    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password'
        )

    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password'
        )

    access_token = create_access_token(data={'sub': user.email})

    return {'access_token': access_token, 'token_type': 'bearer'}



@app.post('/livros/', status_code=HTTPStatus.CREATED, response_model=BookPublic)                                           
def post_book(book: BookSchema, session: Session = Depends(get_session), current_user= Depends(get_current_user),
):                                                                                                                                                                                                                           
    db_book = Book(book_name =book.book_name, book_description = book.description, user_id=current_user.id )                                                                                                                    
    session.add(db_book)                                                                                                  
    session.commit()                                                                                                      
    session.refresh(db_book)                                                                                              
    return db_book
