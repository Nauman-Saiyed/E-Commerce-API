from pydantic import BaseModel , EmailStr
from typing import Optional
from datetime import datetime

class LoginSchema(BaseModel):
    email : EmailStr
    password : str


class TokenResponse(BaseModel):
    access_token : str
    token_type :  str = "bearer"


class OTPRequest(BaseModel):
    phone : str


class OTPVerify(BaseModel):
    phone : str
    otp : str


class CreateUser(BaseModel):
    name : str
    email : EmailStr
    phone : str
    password : str


class UpdateUser(BaseModel):
    name : Optional[str] = None
    phone : Optional[str] = None


class UserResponse(BaseModel):
    user_id : str
    name : str
    email : EmailStr
    phone : str
    created_at : datetime
