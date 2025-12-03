import logging
from typing import List, Union
from pydantic import Field, validator
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    google_api_key: str = Field(..., env="GOOGLE_API_KEY")
    google_genai_use_vertexai: int = Field(0, env="GOOGLE_GENAI_USE_VERTEXAI")

    app_name: str = Field("complianceAssist", env="APP_NAME")
    user_id: str = Field("demo_user", env="USER_ID")
    session_id: str = Field("default_session", env="SESSION_ID")

    memory_backend: str = Field("sqlite", env="MEMORY_BACKEND")
    memory_file: str = Field("memory_store.json", env="MEMORY_FILE")
    sqlite_path: str = Field("memory.db", env="SQLITE_PATH")

    retry_attempts: int = Field(5, env="RETRY_ATTEMPTS")
    retry_exp_base: int = Field(7, env="RETRY_EXP_BASE")
    retry_initial_delay: int = Field(1, env="RETRY_INITIAL_DELAY")
    retry_status_codes: Union[List[int], str] = Field("429,500,503,504", env="RETRY_STATUS_CODES")

    @validator("google_api_key")
    def api_key_required(cls, v):
        if not v:
            raise ValueError("Please set GOOGLE_API_KEY")
        return v

    @validator("retry_status_codes", pre=True)
    def parse_codes(cls, v):
        if isinstance(v, str):
            return [int(code.strip()) for code in v.split(",")]
        return v

settings = Settings()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s :: %(message)s"
)
log = logging.getLogger("config")
log.info("Configuration loaded.")