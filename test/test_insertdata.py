from config.mongo import config_db
config_collection = config_db["configs"]
document = {
    "name": "test_config",
    "value": "test_value"
}
config_collection.insert_one(document)