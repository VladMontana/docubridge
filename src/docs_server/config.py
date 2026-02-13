from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    docs_dir: Path = Path(__file__).parent.parent.parent / "docs"

    model_config = {"env_file": ".env"}


settings = Settings()