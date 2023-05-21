from datetime import timedelta

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session
from starlette import status
from starlette.exceptions import HTTPException

from src.main.auth.logic import decode_token, authenticate_user, create_access_token
from src.main.auth.schemas import Token, DecodedToken
from src.main.commons.db_configuration import get_db
from src.main.users.models import User

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


@router.post("/token", response_model=Token)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db),
):
    user: User = authenticate_user(
        username=form_data.username,
        password=form_data.password,
        db=db
    )
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')

    token = create_access_token(
        username=form_data.username,
        user_id=str(user.id),
        role=user.role,
        expires_delta=timedelta(minutes=200)
    )

    return {
        'access_token': token,
        'token_type': 'bearer'
    }


async def get_current_user(token: str = Depends(oauth2_bearer), db: Session = Depends(get_db)) -> User:
    try:
        decoded_token: DecodedToken = decode_token(token)
        if decoded_token.username is None or decoded_token.user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZEED, detail='Could not validate user')

        user: User = db.query(User).filter_by(id=decoded_token.user_id).first()

        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZEED, detail='Could not validate user')
        else:
            return user
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate user')
