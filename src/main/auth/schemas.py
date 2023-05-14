from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class DecodedToken(BaseModel):
    username: str
    user_id: str
    role: str
