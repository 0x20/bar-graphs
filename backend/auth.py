from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
import httpx

from config import get_settings

ALGORITHM = "HS256"
TOKEN_EXPIRE_HOURS = 24

GITHUB_AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_USER_URL = "https://api.github.com/user"


def get_github_authorize_url(redirect_uri: str) -> str:
    """Generate GitHub OAuth authorization URL."""
    settings = get_settings()
    return (
        f"{GITHUB_AUTHORIZE_URL}"
        f"?client_id={settings.github_client_id}"
        f"&redirect_uri={redirect_uri}"
        f"&scope=read:user"
    )


async def exchange_code_for_token(code: str) -> str:
    """Exchange OAuth code for GitHub access token."""
    settings = get_settings()
    async with httpx.AsyncClient() as client:
        response = await client.post(
            GITHUB_TOKEN_URL,
            data={
                "client_id": settings.github_client_id,
                "client_secret": settings.github_client_secret,
                "code": code,
            },
            headers={"Accept": "application/json"},
        )
        response.raise_for_status()
        return response.json()["access_token"]


async def get_github_user(access_token: str) -> dict:
    """Get GitHub user info from access token."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            GITHUB_USER_URL,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Accept": "application/json",
            },
        )
        response.raise_for_status()
        return response.json()


def is_user_allowed(username: str) -> bool:
    """Check if GitHub username is in the allowlist."""
    settings = get_settings()
    return username in settings.allowed_users_list


def create_jwt_token(username: str) -> str:
    """Create a JWT token for an authenticated user."""
    settings = get_settings()
    expire = datetime.now(timezone.utc) + timedelta(hours=TOKEN_EXPIRE_HOURS)
    payload = {
        "sub": username,
        "exp": expire,
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=ALGORITHM)


def decode_jwt_token(token: str) -> str | None:
    """Decode and validate JWT token, return username or None if invalid."""
    settings = get_settings()
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None
