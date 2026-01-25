from fastapi import APIRouter, HTTPException, status
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from auth import (
    get_github_authorize_url,
    exchange_code_for_token,
    get_github_user,
    is_user_allowed,
    create_jwt_token,
)
from config import get_settings

router = APIRouter(prefix="/auth", tags=["auth"])


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str


@router.get("/login")
async def login():
    """Redirect user to GitHub OAuth authorization page."""
    settings = get_settings()
    redirect_uri = f"{settings.frontend_url}/auth/callback"
    authorize_url = get_github_authorize_url(redirect_uri)
    return RedirectResponse(url=authorize_url)


@router.get("/callback", response_model=TokenResponse)
async def callback(code: str):
    """Handle GitHub OAuth callback, validate user, and return JWT."""
    try:
        # Exchange code for GitHub access token
        github_token = await exchange_code_for_token(code)

        # Get user info from GitHub
        user_info = await get_github_user(github_token)
        username = user_info.get("login")

        if not username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not get username from GitHub",
            )

        # Check if user is in allowlist
        if not is_user_allowed(username):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User not authorized to access this application",
            )

        # Create JWT token
        jwt_token = create_jwt_token(username)

        return TokenResponse(access_token=jwt_token, username=username)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Authentication failed: {str(e)}",
        )
