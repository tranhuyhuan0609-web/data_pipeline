from pymongo import MongoClient
from config.settings import settings
config_client = MongoClient(settings.MONGO_CONFIG_URI)
config_db = config_client[settings.MONGO_CONFIG_DB]
raw_client = MongoClient(settings.MONGO_RAW_URI)
raw_db = raw_client[settings.MONGO_RAW_DB]
processed_client = MongoClient(settings.MONGO_PROCESSED_URI)
processed_db = processed_client[settings.MONGO_PROCESSED_DB]
