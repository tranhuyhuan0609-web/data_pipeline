
# import os
# from dotenv import load_dotenv

# load_dotenv()


# def get_required(key: str) -> str:
#     value = os.getenv(key)
#     if value is None or value.strip() == "":
#         raise ValueError(f"Environment variable '{key}' is required but not set.")
#     return value

# def get_int(key: str, default: int | None = None) -> int:
#    value = os.getenv(key)
#    if value is None or value.strip() == "":
#         if default is not None:
#             return default
#         raise ValueError(f"Environment variable '{key}' is required but not set.")
#    try:
#         return int(value)
#    except ValueError:
#         raise ValueError(f"Environment variable '{key}' must be an integer, but got '{value}'.")
          
       



# POSTGRES_HOST = get_required("POSTGRES_HOST")
# POSTGRES_PORT = get_int("POSTGRES_PORT", 5432)
# POSTGRES_DB = get_required("POSTGRES_DB")
# POSTGRES_USER = get_required("POSTGRES_USER")
# POSTGRES_PASSWORD = get_required("POSTGRES_PASSWORD")




# MONGO_URI = get_required("MONGO_URI")
# MONGO_DB = get_required("MONGO_DB")



# KAFKA_BOOTSTRAP_SERVERS = get_required("KAFKA_BOOTSTRAP_SERVERS")
# KAFKA_RAW_TOPIC = get_required("KAFKA_RAW_TOPIC")
# KAFKA_DLQ_TOPIC = get_required("KAFKA_DLQ_TOPIC")
# KAFKA_CONSUMER_GROUP = get_required("KAFKA_CONSUMER_GROUP")




# CRAWLER_LOG_LEVEL = os.getenv("CRAWLER_LOG_LEVEL", "INFO")