from typing import List

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from db import get_db
from schemas.user_schemas import UserSchema, UserCreateSchema

user_router = APIRouter()

@user_router.get("", response_model=List[UserSchema])
def users(db: Session = Depends(get_db)):
    '''
    Funkcja zwracająca listę wszystkich użytkowników systemu
    '''
    pass

@user_router.get("/{email:str}", response_model=UserSchema)
def get_user(email: str, db: Session = Depends(get_db)) -> UserSchema:
    '''
    Funkcja zwracająca informacje o użytkowniku o podanym adresie email
    '''
    pass

@user_router.post("", response_model=UserSchema)
def sign_up(user_data: UserCreateSchema, db: Session = Depends(get_db)):
    '''
    Funkcja tworząca użytkownika w systemie bazodanowym
    '''
    pass