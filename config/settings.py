from dotenv import load_dotenv
import os
load_dotenv()
class Settings:
    MONGO_CONFIG_URI: str = os.getenv(
        "MONGO_CONFIG_URI",
        "mongodb://localhost:27017"
    )
    MONGO_CONFIG_DB: str = os.getenv(
        "MONGO_CONFIG_DB",
        "crawler_config"
    )
    MONGO_RAW_URI: str = os.getenv(
        "MONGO_RAW_URI",
        "mongodb://localhost:27017"
    )
    MONGO_RAW_DB: str = os.getenv(
        "MONGO_RAW_DB",
        "crawler_raw"
    )
    MONGO_PROCESSED_URI: str = os.getenv(
        "MONGO_PROCESSED_URI",
        "mongodb://localhost:27017"
    )
    MONGO_PROCESSED_DB: str = os.getenv(
        "MONGO_PROCESSED_DB",
        "crawler_processed"
    )
settings = Settings()
