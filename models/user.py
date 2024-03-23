from pydantic import BaseModel, Field, EmailStr

class ModelUser(BaseModel):
    id: int | None = None
    name: str = Field(min_length=3, max_length=64)
    surname: str = Field(min_length=3, max_length=64)
    email: EmailStr
    password: str = Field(min_length=5, max_length=128)
