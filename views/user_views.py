from typing import List

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from crud import user_crud
from db import get_db
from schemas.user_schemas import UserSchema, UserCreateSchema

user_router = APIRouter()

@user_router.get("", response_model=List[UserSchema])
def users(db: Session = Depends(get_db)):
    '''
    Funkcja zwracająca listę wszystkich użytkowników systemu
    '''
    users = user_crud.get_all_users(db)
    return list(users)

@user_router.get("/{email:str}", response_model=UserSchema)
def get_user(email: str, db: Session = Depends(get_db)) -> UserSchema:
    '''
    Funkcja zwracająca informacje o użytkowniku o podanym adresie email
    '''
    user = user_crud.get_user_by_email(db, email)
    if user:
        return user
    else:
        return {'message': 'użytkownik nie istnieje w naszej bazie'}, 404

@user_router.post("", response_model=UserSchema)
def sign_up(user_data: UserCreateSchema, db: Session = Depends(get_db)):
    '''
    Funkcja tworząca użytkownika w systemie bazodanowym
    '''
    pass