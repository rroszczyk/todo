from db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    todos = relationship("TodoModel", back_populates="owner", cascade="all, delete-orphan")

