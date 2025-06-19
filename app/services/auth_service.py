from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.models.user import User
from app.config.env_settings import env

# --- Security Setup ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

# --- Password Utilities ---
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# --- Token Creation ---
def create_access_token(username: str, role: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=env.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": username, "role": role, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, env.SECRET_KEY, algorithm=env.ALGORITHM)
    return encoded_jwt

# --- User Authentication & Authorization Dependencies ---
def authenticate_user(username: str, password: str) -> User | None:
    """Authenticates a user, returning the User object if successful."""
    role = None
    if username == env.ADMIN_USERNAME and verify_password(password, env.ADMIN_PASSWORD_HASH):
        role = env.ADMIN_USERNAME
    elif username == env.USER_USERNAME and verify_password(password, env.USER_PASSWORD_HASH):
        role = env.USER_USERNAME
    if role:
        return User(username=username, role=role)
    return None

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """
    Decode JWT access token and return the current user.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, env.SECRET_KEY, algorithms=[env.ALGORITHM])
        username = payload.get("sub")
        role = payload.get("role")
        if not username or not role:
            raise credentials_exception
        return User(username=username, role=role)
    except JWTError:
        raise credentials_exception

# Dependency for admin-only endpoints
def admin_required(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != env.ADMIN_USERNAME:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user

# Dependency for user routers (both 'user' and 'admin' can access)
def user_required(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role not in (env.USER_USERNAME, env.ADMIN_USERNAME):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User access required",
        )
    return current_user