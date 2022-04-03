from datetime import datetime, timedelta

from typing import Union

from jose.constants import ALGORITHMS
from passlib.context import CryptContext

from sqlalchemy.orm import Session

from models import UserModel
from crud import user_crud
from jose import jwt

SECRET_KEY = "phoosh7ootheeSh4Ees5"

TOKEN_EXPIRES_MINUTES = 15

crypt_context = CryptContext(schemes=['bcrypt'])

def hash_password(password: str) -> str:
    return crypt_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return crypt_context.verify(password, hashed_password)

def authenticate_user(db: Session, email: str, password: str) -> Union[bool, UserModel]:
    user: UserModel = user_crud.get_user_by_email(db, email)

    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_token(payload: dict):
    data = payload.copy()
    expires = datetime.utcnow() + timedelta(TOKEN_EXPIRES_MINUTES)
    data.update({'exp': expires})
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHMS.HS256)
    return token