from pydantic import BaseModel, EmailStr
from fastapi import APIRouter


router = APIRouter()

class UserData(BaseModel):
    email: EmailStr
    password: str
    list_of_stocks: list[str]

@router.post("/register")
def register_user(user_data: UserData):
    return {"email": user_data.email, "password": user_data.password}
