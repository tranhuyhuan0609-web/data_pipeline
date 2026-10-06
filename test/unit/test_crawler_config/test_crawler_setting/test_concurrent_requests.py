from src.domain.entities.crawler_config import CrawlerSettings
import pytest
from pydantic import ValidationError
def test_concurrent_requests_success_one():
    valid_settings = CrawlerSettings(
        concurrent_requests = 1,
    )
    assert valid_settings.concurrent_requests == 1
def test_concurrent_requests_success_ten():
    valid_settings = CrawlerSettings(
        concurrent_requests = 10,
    )
    assert valid_settings.concurrent_requests == 10
def test_concurrent_requests_invalid_zero():
    with pytest.raises(ValidationError):
        CrawlerSettings(
            concurrent_requests = 0,
        )
def test_concurrent_requests_invalid_elevated():
    with pytest.raises(ValidationError):
        CrawlerSettings(
            concurrent_requests = 11,
        )