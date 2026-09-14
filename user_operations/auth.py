from pydantic import BaseModel, EmailStr
from fastapi import APIRouter, Depends
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from user_database.database import get_db
from user_database.user_repository import UserRepository
from user_database.user_db_model import User

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)
router = APIRouter()


class UserData(BaseModel):
    email: EmailStr
    password: str
    list_of_stocks: list[str]

@router.post("/register")
def register_user(
        user_data: UserData,
        db_session: Session = Depends(get_db)
):
    repository = UserRepository(db_session)

    hashed_password = hash_password(user_data.password)
    user = User(
        email=user_data.email,
        password_hash=hashed_password,
    )

    repository.add_user(user)

    return {"email": user.email, "id": user.id}

@router.post("/login")
def log_user_in(
    user_data: UserData,
    db_session: Session = Depends(get_db)
):
    repository = UserRepository(db_session)

    user = repository.get_by_email(user_data.email)

    if user is None:
        return False

    return verify_password(
        user_data.password,
        user.password_hash
    )


def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)
