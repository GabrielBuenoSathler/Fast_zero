from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schema import (
    UserList,
    UserPublic,
    UserSchema,
)
from fast_zero.security import (
    get_current_user,
    get_password_hash,
)

router = APIRouter(prefix='/users', tags=['users'])

                                                                                                                                              
                                                                                                                                              
@router.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)                                                               
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

@router.get('/users_teste/',status_code = HTTPStatus.OK ,response_model=UserList)          
def read_users(                                                                         
        limit : int = 10,                                                               
        offset: int =0,                                                                 
        session: Session = Depends(get_session),                                        
        current_user= Depends(get_current_user),                                        
):                                                                                      
    users = session.scalars(select(User).limit(limit).offset(offset))                   
    return {'users': users}                                                             
                                                                                        
                                                                                        
@router.put('/users/{user_id}', response_model=UserPublic)                                 
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
                                                                                        

