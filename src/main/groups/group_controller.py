from fastapi import APIRouter, Depends
from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.main.auth.auth_controller import get_current_user
from src.main.commons.db_configuration import get_db
from src.main.groups.models import Group, UserGroup, UserGroupRole
from src.main.groups.schemes import CreateGroup, JoinUserToGroup
from src.main.users.models import User

router = APIRouter(
    prefix='/groups',
    tags=['groups']
)


@router.get("/")
async def get_groups(user: User = Depends(get_current_user)):
    return user.groups


@router.post("/")
async def create_group(request: CreateGroup, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    group: Group = Group(
        name=request.name,
        description=request.description,
        users=[user]
    )
    db.add(group)
    db.flush()
    user_group: UserGroup | None = db.query(UserGroup).filter(UserGroup.user_id == user.id).filter(
        UserGroup.group_id == group.id).first()
    user_group.role = UserGroupRole.administrador
    db.commit()
    db.refresh(group)
    return group


@router.delete("/{group_id}")
async def delete_group(group_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    group: Group | None = db.query(Group).join(UserGroup, Group.id == UserGroup.group_id).filter(and_(
        Group.id == group_id,
        UserGroup.role == UserGroupRole.administrador,
        UserGroup.user_id == user.id
    )).first()
    db.delete(group)
    db.commit()


@router.post("/join")
async def join_user_to_group(request: JoinUserToGroup, db: Session = Depends(get_db),
                             user: User = Depends(get_current_user)):
    user_group: UserGroup | None = db.query(UserGroup).filter(
        UserGroup.user_id == user.id,
        UserGroup.role == UserGroupRole.administrador,
        UserGroup.group_id == request.group_id
    ).first()

    if user_group is None:
        return "No user_group"

    candidate_user: User | None = db.query(User).filter(User.id == request.candidate_user_id).first()

    if user is None:
        return "no user"

    user_group: UserGroup = UserGroup(
        user_id=candidate_user.id,
        group_id=user_group.group_id,
    )

    db.add(user_group)
    db.commit()
