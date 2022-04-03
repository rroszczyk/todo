from typing import List, Optional

from sqlalchemy.orm import Session

from models import UserModel

def get_all_users(db: Session) -> List[UserModel]:
    return db.query(UserModel).filter().all()

def get_user_by_email(db: Session, email: str) -> Optional[UserModel]:
    return db.query(UserModel).filter(UserModel.email == email).first()

