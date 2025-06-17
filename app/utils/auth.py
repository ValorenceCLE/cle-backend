import os
from datetime import datetime, timedelta
from passlib.context import CryptContext
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from the app/app.env file
env_path = Path(__file__).parent.parent / 'app.env'
load_dotenv(dotenv_path=env_path)

# Load environment variables
USER_PASSWORD_HASH = os.getenv("USER_PASSWORD_HASH")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PASSWORD_HASH")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")  # Default to HS256 if not set
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

class User(BaseModel):
    username: str
    role: str
    

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def check_credentials(username: str, password: str) -> bool:
    if username == "user":
        return verify_password(password, USER_PASSWORD_HASH)
    elif username == "admin":
        return verify_password(password, ADMIN_PASSWORD_HASH)
    return False

def create_access_token(username: str) -> str:
    expire = datetime.now(datetime.UTC) + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    payload = {"sub": username, "role": username, "exp": expire}
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username not in ("user", "admin") or role != username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return User(username=username, role=role)

# Dependency for admin-only endpoints
def admin_required(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user

# Dependency for user routers (both 'user' and 'admin' can access)
def user_required(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role not in ("user", "admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User access required",
        )
    return current_user