from config.mongo import config_db
config_collection = config_db["configs"]
config_collection.create_index("" \
"site_id",
unique = True)
def create_config(document):
    result = config_collection.insert_one(document)
    return result.inserted_id