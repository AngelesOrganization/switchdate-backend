from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import extract
from sqlalchemy.orm import Session

from src.main.auth.auth_controller import get_current_user
from src.main.commons.db_configuration import get_db
from src.main.groups.models import Group, UserGroupRole
from src.main.shifts.models import Shift
from src.main.shifts.schemes import CreateShift
from src.main.users.models import User

router = APIRouter(
    prefix='/shifts',
    tags=['shifts']
)


@router.get("")
async def get_shifts(month: int, year: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if month > 12 or month < 1:
        return "Invalid month"

    return db.query(Shift).filter(Shift.user_id == user.id, extract('month', Shift.start_time) == month,
                                  extract('year', Shift.start_time) == year).all()


@router.post("")
async def create_shift(request: CreateShift, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    shift: Shift = Shift(
        user_id=user.id,
        start_time=request.start_time,
        end_time=request.end_time
    )

    db.add(shift)
    db.commit()
    db.refresh(shift)

    return request


@router.delete("/{shift_id}")
async def delete_group(shift_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    shift: Shift | None = db.query(Shift).filter(Shift.id == shift_id, Shift.user_id == user.id).first()
    db.delete(shift)
    db.commit()

#
# @router.post("/join")
# async def join_user_to_group(join_user_to_group_scheme: JoinUserToGroup, db: Session = Depends(get_db),
#                              user: User = Depends(get_current_user)):
#     user_group: UserGroup | None = db.query(UserGroup).filter(
#         UserGroup.user_id == user.id,
#         UserGroup.role == UserGroupRole.administrador,
#         UserGroup.group_id == join_user_to_group_scheme.group_id
#     ).first()
#
#     if user_group is None:
#         return "Tu lo que eres es un hijo de puta"
#
#     candidate_user: User | None = db.query(User).filter(User.id == join_user_to_group_scheme.candidate_user_id).first()
#
#     if user is None:
#         return "Lo siento amigo ese pana no existe"
#
#     user_group: UserGroup = UserGroup(
#         user_id=candidate_user.id,
#         group_id=user_group.group_id,
#     )
#
#     db.add(user_group)
#     db.commit()