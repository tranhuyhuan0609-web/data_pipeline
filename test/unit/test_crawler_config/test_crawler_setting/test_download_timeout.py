from src.domain.entities.crawler_config import CrawlerSettings
import pytest
from pydantic import ValidationError
def test_download_timeout_success():
    valid_settings = CrawlerSettings(
        download_timeout = 1.0,
    )
    assert valid_settings.download_timeout == 1.0
def test_download_timeout_invalid_zero():
    with pytest.raises(ValidationError):
        CrawlerSettings(
            download_timeout = 0,
        )
def test_download_timeout_invalid_elevated():
    with pytest.raises(ValidationError):
        CrawlerSettings(
            download_timeout = 301.0,
        )
def test_download_timeout_success_elevated():
    valid_settings = CrawlerSettings(
        download_timeout = 300.0,
    )
    assert valid_settings.download_timeout == 300.0