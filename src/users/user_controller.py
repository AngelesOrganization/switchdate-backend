from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.auth.logic import encrypt_password
from src.users.models import User
from src.commons.db_utils import get_db
from src.users.schemas import CreateUserRequest

router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.post("/")
async def create_user(
        create_user_request: CreateUserRequest,
        db: Session = Depends(get_db)
):
    create_user_model: User = User(
        username=create_user_request.username,
        email=create_user_request.email,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        hashed_password=encrypt_password(create_user_request.password),
        role=create_user_request.role
    )

    db.add(create_user_model)
    db.commit()
