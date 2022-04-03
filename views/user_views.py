import logging
from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from crud import user_crud
from crud.user_crud import get_current_user
from db import get_db
from models import UserModel
from schemas.token_schemas import TokenSchema
from schemas.user_schemas import UserSchema, UserCreateSchema
from utils.security import authenticate_user, create_token

user_router = APIRouter()
logger = logging.getLogger()

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
    user = user_crud.get_user_by_email(db, user_data.email)
    logger.info("Sprawdzenie czy użytkownik istnieje w bazie")
    if user:
        raise HTTPException(status_code=409, detail="adres email istnieje w bazie")
    new_user = user_crud.add_user(db, user_data)
    logger.info("Utworzenie nowego użytkownika")
    return new_user

@user_router.post("/login", response_model=TokenSchema)
def login(db: Session = Depends(get_db), form: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form.username, form.password)
    if not user:
        raise HTTPException(
            401,
            detail="błędna nazwa użytkownika lub hasło",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_token(payload={'sub': user.email})

    return {'access_token': token, 'token_type': 'bearer'}

@user_router.get("info", response_model=UserSchema)
def get_current_user(user: UserModel = Depends(get_current_user)):
    return user