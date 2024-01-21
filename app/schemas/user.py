from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    name: str = Field(min_length=2)
    surname: str = Field(min_length=2)
    email: EmailStr
    password: str = Field(min_length=8)


class ShowUser(BaseModel):
    id: int
    name: str
    surname: str
    email: EmailStr
    balance: int

    class Config:
        from_attributes = True

