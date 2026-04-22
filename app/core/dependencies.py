from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from ..core.security import verify_access_token
from ..core.config import SECRET_KEY, ALGORITHM
from ..core.exceptions import NotFoundException, UnauthorizedException
from ..db.database import get_db
from ..db.models import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

DB = Annotated[Session, Depends(get_db)]
Token = Annotated[str, Depends(oauth2_scheme)]


def get_current_user(token: Token, db: DB) -> User:
    payload = verify_access_token(token, SECRET_KEY, [ALGORITHM])
    user_id = payload.get("sub")
    if not user_id:
        raise UnauthorizedException("Invalid token", error_detail={"reason": "Token payload missing user ID"})
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise NotFoundException("User not found", error_detail={"user_id": str(user_id)})
    return user

CurrentUser = Annotated[User, Depends(get_current_user)]
