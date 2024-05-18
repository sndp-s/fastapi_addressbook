"""
Configs/Settings for the application
"""
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Main Configs/Settings class
    """
    app_name: str
    author_name: str
    author_email: str

    # Read the values from '.env' file
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
