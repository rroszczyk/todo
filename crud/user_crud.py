import logging
from typing import List, Optional

from fastapi import HTTPException
from fastapi.params import Depends
from jose.constants import ALGORITHMS
from sqlalchemy.orm import Session

from db import get_db
from models import UserModel
from schemas.user_schemas import UserCreateSchema, UserSchema
from utils.security import hash_password, SECRET_KEY

from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

logger = logging.getLogger()

def get_all_users(db: Session) -> List[UserModel]:
    return db.query(UserModel).filter().all()

def get_user_by_email(db: Session, email: str) -> Optional[UserModel]:
    return db.query(UserModel).filter(UserModel.email == email).first()

def add_user(db: Session, user_data: UserCreateSchema) -> UserSchema:
    db_user = UserModel(
        email = user_data.email,
        last_name = user_data.last_name,
        first_name = user_data.first_name,
        hashed_password = hash_password(user_data.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_current_user(token: str = Depends(OAuth2PasswordBearer(tokenUrl="/users/login")), db: Session = Depends(get_db)) -> UserModel:
    JWT_exception = HTTPException(
        401,
        detail="błędny token JWT",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHMS.HS256])
        email: str = payload.get('sub')
        if email is None:
            raise JWT_exception

    except JWTError:
        raise JWT_exception

    user = get_user_by_email(db, email)
    if user is None:
        raise JWT_exception

    return user