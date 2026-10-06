from src.domain.entities.crawler_config import CrawlerSettings
import pytest
from pydantic import ValidationError
def test_retry_enabled_false_max_retries_greater_than_zero():
    with pytest.raises(ValidationError):
        CrawlerSettings(
            retry_enabled = False,
            max_retries = 1
        )
def test_retry_enabled_true_max_retries_zero():
    with pytest.raises(ValidationError):
        CrawlerSettings(
            retry_enabled = True,
            max_retries = 0
        )
def test_retry_enabled_false_max_retries_zero():
    valid_settings = CrawlerSettings(
        retry_enabled = False,
        max_retries = 0
    )
    assert valid_settings.retry_enabled == False
    assert valid_settings.max_retries == 0
def test_retry_enabled_true_max_retries_greater_than_zero():
    valid_settings = CrawlerSettings(
        retry_enabled = True,
        max_retries = 3
    )
    assert valid_settings.retry_enabled == True
    assert valid_settings.max_retries == 3