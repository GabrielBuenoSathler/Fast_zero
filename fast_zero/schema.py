from pydantic import BaseModel, EmailStr, ConfigDict


class Message(BaseModel):
    message: str

class UserSchema(BaseModel):
    email : str 
    username : str
    password : str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]


class Token(BaseModel):
    access_token : str
    token_type: str 

class BookSchema(BaseModel):
    book_name : str
    description : str

class BookPublic(BaseModel):
    user_id : int
    book_name : str
    book_id : int
    book_description : str
 
class BookList(BaseModel):
    books : list[BookPublic]

