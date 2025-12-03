# config.py
import logging
from typing import List
from pydantic import Field, validator
from pydantic_settings import BaseSettings
from dotenv import load_dotenv   # <-- add this
import os

# Load variables from .env into os.environ
load_dotenv()

class Settings(BaseSettings):
    google_api_key: str = Field(..., env="GOOGLE_API_KEY")
    app_name: str = Field("complianceAssist")
    user_id: str = Field("demo_user")
    session_id: str = Field("default_session")
    memory_backend: str = Field("sqlite")
    memory_file: str = Field("memory_store.json")
    sqlite_path: str = Field("memory.db")
    retry_attempts: int = 5
    retry_exp_base: int = 7
    retry_initial_delay: int = 1
    retry_status_codes: List[int] = Field(default_factory=lambda: [429, 500, 503, 504])

    @validator("google_api_key")
    def api_key_required(cls, v):
        if not v:
            raise ValueError("Please set GOOGLE_API_KEY")
        return v

settings = Settings()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s :: %(message)s"
)
log = logging.getLogger("config")
log.info("Configuration loaded.")
