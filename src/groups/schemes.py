from pydantic import BaseModel


class CreateGroup(BaseModel):
    name: str
    description: str


class JoinUserToGroup(BaseModel):
    candidate_user_id: str
    group_id: str
