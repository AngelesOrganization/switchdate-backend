from fastapi import APIRouter
from persistence.group_repository_sqlalchemy import GroupRepositorySqlAlchemy
from persistence.schemes.group_schema import GroupRead, GroupCreate

router = APIRouter()
group_repository: GroupRepositorySqlAlchemy = GroupRepositorySqlAlchemy()


@router.post("/groups/", response_model=GroupRead)
def create_group(group_create: GroupCreate) -> GroupRead:
    return group_repository.create_group(group_create)


@router.get("/groups/{group_id}", response_model=GroupRead)
async def get_group(group_id):
    return group_repository.get_group_by_id(group_id)
