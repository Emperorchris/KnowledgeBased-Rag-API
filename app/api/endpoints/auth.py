from fastapi import APIRouter
from ...core.dependencies import DB, CurrentUser
from ...schemas import UserCreate, UserLogin, RefreshTokenRequest, AuthResponse
from ...modules import auth_service

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("/register", response_model=AuthResponse)
def register(user: UserCreate, db: DB):
    return auth_service.register(user, db)

@auth_router.post("/login", response_model=AuthResponse)
def login(user: UserLogin, db: DB):
    return auth_service.login(user.email, user.password, db)

@auth_router.post("/refresh")
def refresh_access_token(token: RefreshTokenRequest,  db: DB):
    return auth_service.refresh_access_token(token.refresh_token, db)

@auth_router.post("/revoke")
def revoke_refresh_token(token: RefreshTokenRequest, db: DB):
    return auth_service.revoke_refresh_token(token.refresh_token, db)
@auth_router.post("/logout")
def logout(current_user: CurrentUser, db: DB):
    return auth_service.logout(current_user.id, db)