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
app = FastAPI()  



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
                                                                                                                           
@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)                                            
def create_user(user: UserSchema, session: Session = Depends(get_session)):                                                
                                                                                                                           
                                                                                                                           
    db_user = session.scalar(                                                                                              
        select(User).where(                                                                                                
            (User.username == user.username) | (User.email == user.email)                                                  
                                                                                                                           
        )                                                                                                                  
    )                                                                                                                      
                                                                                                                           
    if db_user:                                                                                                            
        if db_user.username == user.username:                                                                              
                                                                                                                           
                                                                                                                           
            raise HTTPException(                                                                                           
                status_code=HTTPStatus.CONFLICT,                                                                           
                detail='Username already exists',                                                                          
            )                                                                                                              
        elif db_user.email == user.email:                                                                                  
            raise HTTPException(                                                                                           
                status_code=HTTPStatus.CONFLICT,                                                                           
                detail='Email already exists',                                                                             
            )                                                                                                              
                                                                                                                           
    db_user = User(                                                                                                        
        username=user.username, password=get_password_hash(user.password), email=user.email                                
    )                                                                                                                      
    session.add(db_user)                                                                                                   
    session.commit()                                                                                                       
    session.refresh(db_user)                                                                                               
                                                                                                                           
    return db_user  


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session = Depends(get_session)):


    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)

        )
    )

    if db_user:
        if db_user.username == user.username:


            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Username already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Email already exists',
            )

    db_user = User(
        username=user.username, password=get_password_hash(user.password), email=user.email
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user

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


@app.get('/users_teste/',status_code = HTTPStatus.OK ,response_model=UserList)
def read_users(
        limit : int = 10,
        offset: int =0,
        session: Session = Depends(get_session),
        current_user= Depends(get_current_user),
):
    users = session.scalars(select(User).limit(limit).offset(offset))
    return {'users': users}


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int,
    user: UserSchema,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )
    try:
        current_user.username = user.username
        current_user.password = get_password_hash(user.password)
        current_user.email = user.email
        session.commit()
        session.refresh(current_user)

        return current_user
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or Email already exists',
        )



@app.post('/livros/', status_code=HTTPStatus.CREATED, response_model=BookPublic)                                           
def post_book(book: BookSchema, session: Session = Depends(get_session), current_user= Depends(get_current_user),
):                                                                                                                                                                                                                           
    db_book = Book(book_name =book.book_name, book_description = book.description, user_id=current_user.id )                                                                                                                    
    session.add(db_book)                                                                                                  
    session.commit()                                                                                                      
    session.refresh(db_book)                                                                                              
    return db_book
