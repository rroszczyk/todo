from typing import List, Optional

from sqlalchemy.orm import Session

from models import UserModel
from schemas.user_schemas import UserCreateSchema, UserSchema

from passlib.context import CryptContext

crypt_context = CryptContext(schemes=['bcrypt'])

def hash_password(password: str) -> str:
    return crypt_context.hash(password)

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