from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    github_client_id: str
    github_client_secret: str
    jwt_secret: str
    allowed_users: str  # comma-separated list of GitHub usernames
    frontend_url: str = "http://localhost:5173"
    tab_data_path: str = "./tab-data"

    @property
    def allowed_users_list(self) -> list[str]:
        return [u.strip() for u in self.allowed_users.split(",") if u.strip()]

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()
