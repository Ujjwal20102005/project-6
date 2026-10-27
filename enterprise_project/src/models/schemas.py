from typing import List

from pydantic import BaseModel, Field, field_validator


class UserCreate(BaseModel):
    email: str
    password: str = Field(min_length=8)

    @field_validator("email")
    @classmethod
    def valid_email(cls, v):
        if "@" not in v or "." not in v.split("@")[-1]:
            raise ValueError("invalid email")
        return v.lower()


class Login(BaseModel):
    email: str
    password: str


class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    price: float = Field(gt=0)
    stock: int = Field(ge=0, default=0)


class OrderItemIn(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)


class OrderCreate(BaseModel):
    items: List[OrderItemIn] = Field(min_length=1)
