from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.auth.auth_controller import get_current_user
from src.commons.db_utils import get_db
from src.groups.models import Group, UserGroup, UserGroupRole
from src.groups.schemes import CreateGroup, JoinUserToGroup
from src.shifts.models import Shift
from src.shifts.schemes import CreateShift
from src.users.models import User

router = APIRouter(
    prefix='/shifts',
    tags=['shifts']
)


@router.get("/{group_id}")
async def get_shifts(group_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Shift).filter(Shift.user_id == user.id, Shift.group_id == group_id).first()


@router.post("/")
async def create_shift(request: CreateShift, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if db.query(Group).filter(Group.id == request.group_id).first() is None:
        return "Tu eres tonto"

    shift: Shift = Shift(
        group_id=request.group_id,
        user_id=user.id,
        start_time=datetime.fromtimestamp(request.start_time),
        end_time=datetime.fromtimestamp(request.end_time)
    )

    db.add(shift)
    db.commit()
    db.refresh(shift)

    return request


# @router.delete("/{group_id}")
# async def delete_group(group_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
#     group: Group | None = db.query(Group).join(UserGroup, Group.id == UserGroup.group_id).filter(and_(
#         Group.id == group_id,
#         UserGroup.role == UserGroupRole.administrador,
#         UserGroup.user_id == user.id
#     )).first()
#     db.delete(group)
#     db.commit()
#
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
