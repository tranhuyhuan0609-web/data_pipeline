from contextlib import nullcontext

from src.domain.entities.crawler_config import CrawlerSettings, Pagination
from pydantic import ValidationError
import pytest
def test_crawler_setting():
    valid_settings = CrawlerSettings(
        retry_enabled=True,
        max_retries=3,)
    assert valid_settings.retry_enabled is True
    assert valid_settings.max_retries == 3
def test_crawler_setting_invalid_retry():
    with pytest.raises(ValidationError):
        CrawlerSettings(
            retry_enabled=False,
            max_retries=3,)
def test_crawler_setting_invalid_max_retries():
    with pytest.raises(ValidationError):
        CrawlerSettings(
            retry_enabled=True,
            max_retries=3,
            delay=-1.0)
def test_max_pages_validation():
        paginations = Pagination(
            enabled=True,
            next_page="a.next",
            max_pages=5
        )
        assert paginations.max_pages == 5   

