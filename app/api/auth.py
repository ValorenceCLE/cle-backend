from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.models.token import Token
from app.services import auth_service

router = APIRouter()

@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK, tags=["Authentication"], summary="Main login endpoint", description="Authenticates a user and returns a JWT token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth_service.create_access_token(username=user.username, role=user.role)
    return {"access_token": access_token, "token_type": "bearer"}
