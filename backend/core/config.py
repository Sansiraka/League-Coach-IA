from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "League Coach IA"
    DATABASE_URL: str
    RIOT_API_KEY: str = ""
    GROQ_API_KEY: str = ""

    class Config:
        env_file = ".env"

settings = Settings()
