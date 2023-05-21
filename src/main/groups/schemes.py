from pydantic import BaseModel


class CreateGroup(BaseModel):
    name: str
    description: str


class JoinUserToGroup(BaseModel):
    candidate_username: str
    group_id: str
