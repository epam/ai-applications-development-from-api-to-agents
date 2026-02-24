from typing import Optional

from pydantic import BaseModel


class Address(BaseModel):
    country: str
    city: str
    street: str
    flat_house: str


class CreditCard(BaseModel):
    num: str
    cvv: str
    exp_date: str


class UserCreate(BaseModel):
    name: str
    surname: str
    email: str
    phone: Optional[str] = None
    date_of_birth: Optional[str] = None
    address: Optional[Address] = None
    gender: Optional[str] = None
    company: Optional[str] = None
    salary: Optional[float] = None
    about_me: str
    credit_card: Optional[CreditCard] = None


class UserUpdate(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: Optional[str] = None
    address: Optional[Address] = None
    gender: Optional[str] = None
    company: Optional[str] = None
    salary: Optional[float] = None
    credit_card: Optional[UserCreate] = None