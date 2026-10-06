from src.domain.entities.crawler_config import CrawlerSettings
import pytest
def test_randomize_delay_enabled():
    valid_settings = CrawlerSettings(
        randomize_delay=True,
    )
    assert valid_settings.randomize_delay is True
def test_randomize_delay_disabled():
    valid_settings = CrawlerSettings(
        randomize_delay = False
    )
    assert valid_settings.randomize_delay is False