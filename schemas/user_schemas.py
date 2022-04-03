from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr

class UserSchema(UserBase):
    first_name: str
    last_name: str

    class Config:
        orm_mod = True

class UserCreateSchema(UserSchema):
    password: str

    class Config:
        orm_mod = True