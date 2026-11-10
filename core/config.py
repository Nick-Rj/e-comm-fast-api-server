# Configuration Management: Centralize application settings and database credentials

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

# BaseSettings will fetch the data from configuration and env files.
class Settings(BaseSettings):
    
    # SecretStr prevents accidental exposure of all actual database URL when the settings object is printed or represented.
    # Database URL is required and must come from the environment or the configured .env file.
    DATABASE_URL: SecretStr

    # Configuration for loading environment variables.
    # Pydantic Settings v2 uses SettingsConfigDict to configure environment loading.
    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8",
        extra = "ignore"
    )

# ---------------------------------------
# Centralized Settings Instance
# ---------------------------------------

# Create a centralized settings instance for application-wide use.
settings = Settings()        