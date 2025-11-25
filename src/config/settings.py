"""Configuration settings for agent applications."""
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from workspace root
workspace_root = Path(__file__).parent.parent.parent
env_path = workspace_root / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    """Application settings loaded from environment variables."""

    # Azure AI Agent Service
    PROJECT_ENDPOINT: str = os.getenv("PROJECT_ENDPOINT", "")
    PROJECT_API_KEY: str = os.getenv("PROJECT_API_KEY", "")

    # Application Insights
    APPLICATIONINSIGHTS_CONNECTION_STRING: Optional[str] = os.getenv(
        "APPLICATIONINSIGHTS_CONNECTION_STRING"
    )

    @classmethod
    def validate(cls) -> None:
        """Validate required settings are present."""
        missing = []
        if not cls.PROJECT_ENDPOINT:
            missing.append("PROJECT_ENDPOINT")
        if not cls.PROJECT_API_KEY:
            missing.append("PROJECT_API_KEY")

        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")


# Create global settings instance
settings = Settings()
