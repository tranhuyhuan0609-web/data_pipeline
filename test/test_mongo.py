import pytest
from config.mongo import (
    config_client,
    raw_client,
    processed_client
)
def test_config_clients():
    test_1 = config_client.admin.command('ping')
    assert test_1['ok'] == 1.0
def test_raw_clients():
    test_2 = raw_client.admin.command('ping')
    assert test_2['ok'] == 1.0
def test_processed_clients():
    test_3 = processed_client.admin.command('ping')
    assert test_3['ok'] == 1.0