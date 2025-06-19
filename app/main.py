from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse

from app.api.router import api_router
from app.models.user import User
from app.services.auth_service import get_current_user, admin_required

app = FastAPI(
    title="CLE Backend API",
    description="Backend for Covert Law Enforcement IoT devices.",
    version="1.0.0"
)

app.include_router(api_router, prefix="/api")

app.add_middleware(GZipMiddleware, minimum_size=1024)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )

# --- Example Protected Endpoints in main.py ---
@app.get("/users/me", response_model=User, tags=["Users"])
async def read_users_me(current_user: User = Depends(get_current_user)):
    """Fetches the profile for the currently authenticated user."""
    return current_user

@app.get("/admin/panel", tags=["Admin"])
async def read_admin_panel(admin: User = Depends(admin_required)):
    """An example endpoint only accessible to admin users."""
    return {"message": f"Welcome to the admin panel, {admin.username}!"}

@app.get("/", tags=["Root"], summary="Root endpoint", description="Returns a simple message")
async def root():
    return {"status": "ok", "message": "CLE Backend Operational"}
