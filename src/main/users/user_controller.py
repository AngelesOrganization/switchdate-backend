from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.main.auth.auth_controller import get_current_user
from src.main.auth.logic import encrypt_password
from src.main.groups.models import UserGroup, Group
from src.main.users.models import User
from src.main.commons.db_configuration import get_db
from src.main.users.schemas import CreateUserRequest, ShiftSwapList

router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.post("")
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
    db.refresh(create_user_model)

    return create_user_model


@router.get("/requested-swaps", response_model=ShiftSwapList)
async def get_user_requested_swaps(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    swaps = user.requested_shifts
    return ShiftSwapList(swaps=swaps)


@router.get("/requester-swaps", response_model=ShiftSwapList)
async def get_user_requester_swaps(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    swaps = user.requester_shifts
    return ShiftSwapList(swaps=swaps)


@router.get("/{group_id}")
async def get_users_by_group(group_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    users: list[User] = db.query(User). \
        join(UserGroup, User.id == UserGroup.user_id). \
        join(Group, Group.id == UserGroup.group_id). \
        filter(Group.id == group_id). \
        all()

    return users
