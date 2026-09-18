from database.config_reponsitory import config_collection
def test_config_collection():
    assert config_collection.name == "configs"