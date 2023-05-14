from datetime import timedelta, datetime

from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from src.main.users.models import User
from src.main.auth.schemas import DecodedToken

SECRET_KEY = 'ASDASD'
ALGORITHM = 'HS256'
bcrypt_context: CryptContext = CryptContext(schemes=['bcrypt'], deprecated='auto')


def authenticate_user(
        username: str,
        password: str,
        db: Session
) -> User | bool:
    user: User = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(
        username: str,
        user_id: str,
        role: str,
        expires_delta: timedelta
):
    encode: dict = {
        'sub': username,
        'id': user_id,
        'exp': datetime.utcnow() + expires_delta,
        'role': role
    }
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> DecodedToken:
    payload: dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return DecodedToken(
        username=payload.get('sub'),
        user_id=payload.get('id'),
        role=payload.get('role')
    )


def encrypt_password(password: str) -> str:
    return bcrypt_context.hash(password)
