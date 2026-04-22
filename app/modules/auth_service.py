from ..core.exceptions import (
    BadRequestException,
    ConflictException,
    InternalServerException,
    UnauthorizedException,
    ForbiddenException,
    NotFoundException,
)
from ..core import (
    hash_password,
    verify_password,
    create_access_token,
    verify_access_token,
    generate_refresh_token,
)
from ..db.models import User, RefreshToken
from ..schemas.user import UserCreate, UserResponse
from datetime import timedelta, datetime, timezone
from sqlalchemy.orm import Session


def register(user: UserCreate, db: Session) -> dict:
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise ConflictException("User with this email already exists", error_detail={"email": user.email})
    hashed_password = hash_password(user.password)
    try:
        new_user = User(name=user.name, email=user.email,
                        password_hash=hashed_password)
    except ValueError as e:
        raise BadRequestException(str(e), error_detail={"email": user.email})
    refresh_token = generate_refresh_token()
    db.add(new_user)
    db.flush()  # Flush to get the new user's ID for the refresh token
    db_refresh_token = RefreshToken(
        user_id=new_user.id,
        token=refresh_token,
        # Refresh token valid for 7 days
        expires_at=datetime.now(timezone.utc) + timedelta(days=7),
    )
    access_token = create_access_token({"sub": str(new_user.id)})
    db.add(db_refresh_token)
    db.commit()
    db.refresh(new_user)
    return {
        "user": UserResponse.model_validate(new_user),
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


def login(email: str, password: str, db: Session) -> dict:
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise UnauthorizedException("Invalid email or password")

    if not verify_password(password, user.password_hash):
        raise UnauthorizedException("Invalid email or password")

    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = generate_refresh_token()
    db_refresh_token = RefreshToken(
        user_id=user.id,
        token=refresh_token,
        # Refresh token valid for 7 days
        expires_at=datetime.now(timezone.utc) + timedelta(days=7),
    )
    db.add(db_refresh_token)
    db.commit()
    user_response = UserResponse.model_validate(user)
    return {
        "user": user_response,
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


def refresh_access_token(refresh_token: str, db: Session) -> dict:
    db_token = db.query(RefreshToken).filter(
        RefreshToken.token == refresh_token,
        RefreshToken.is_revoked.is_(False),
        RefreshToken.expires_at > datetime.now(timezone.utc)
    ).first()

    if not db_token:
        raise UnauthorizedException("Invalid or expired refresh token", error_detail={"reason": "Token is invalid, revoked, or expired"})

    user = db.query(User).filter(User.id == db_token.user_id).first()
    if not user:
        raise NotFoundException("User not found", error_detail={"user_id": str(db_token.user_id)})
    
    db_token.is_revoked = True
    
    new_refresh_token = generate_refresh_token()
    new_db_token = RefreshToken(
        user_id=user.id,
        token=new_refresh_token,
        expires_at=datetime.now(timezone.utc) + timedelta(days=7),
    )
    db.add(new_db_token)
    db.commit()
    
    access_token = create_access_token({"sub": str(user.id)})
    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "user": UserResponse.model_validate(user),
    }
    
    
def revoke_refresh_token(refresh_token: str, db: Session):
    db_token = db.query(RefreshToken).filter(
        RefreshToken.token == refresh_token,
        RefreshToken.is_revoked.is_(False)
    ).first()

    if not db_token:
        raise NotFoundException("Refresh token not found or already revoked", error_detail={"reason": "Token does not exist or has been revoked"})

    db_token.is_revoked = True
    db.commit()
    
    return {"message": "Refresh token revoked"}


def logout(user_id: str, db: Session):
    db.query(RefreshToken).filter(
        RefreshToken.user_id == user_id,
        RefreshToken.is_revoked.is_(False)
    ).update({"is_revoked": True})
    db.commit()
    return {"message": "Logged out successfully"}