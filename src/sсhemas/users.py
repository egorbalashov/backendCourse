from pydantic import BaseModel, ConfigDict, EmailStr


class UserRequestsADD(BaseModel):
    email: EmailStr
    password: str


class UserADD(BaseModel):
    email: EmailStr
    hash_password: str


class User(BaseModel):
    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class UserWithHashedPassword(User):
    hash_password: str
