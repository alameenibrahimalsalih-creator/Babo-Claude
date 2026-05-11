try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Babo Claude"
    
    # Database and Memory Settings
    REDIS_URL: str = "redis://localhost:6379"
    POSTGRES_URL: str = "postgresql://postgres:postgres@localhost/babo"
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    
    # API Keys
    BINANCE_API_KEY: str = ""
    BINANCE_SECRET: str = ""
    TELEGRAM_BOT_TOKEN: str = "8541846195:AAFP4ygYvR1vySGoJM8bHIxnT8oJtYRG8jU"
    
    # Consensus Settings
    CONSENSUS_THRESHOLD: float = 0.85

settings = Settings()
