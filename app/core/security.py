from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import jwt
from jwt.exceptions import PyJWTError, InvalidTokenError
from datetime import datetime, timedelta, timezone
import secrets
from typing import Optional
from .config import SECRET_KEY, ALGORITHM

from .exceptions import UnauthorizedException

def hash_password(password: str) -> str:
    return PasswordHasher().hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    try:
        PasswordHasher().verify(hashed_password, password)
        return True
    except VerifyMismatchError:
        return False
    
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None, secret_key: str = SECRET_KEY, algorithm: str = ALGORITHM) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt


def verify_access_token(token: str, secret_key: str = SECRET_KEY, algorithms: list = [ALGORITHM]) -> Optional[dict]:
    try:
        payload = jwt.decode(token, secret_key, algorithms=algorithms)
        return payload
    except (InvalidTokenError, PyJWTError):
        raise UnauthorizedException("Invalid or expired token", error_detail={"reason": "Token could not be decoded or has expired"})
    
    return None


def generate_refresh_token() -> str:
    return secrets.token_urlsafe(64)