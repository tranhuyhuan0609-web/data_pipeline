
import pytest
from src.domain.entities.crawler_config import CrawlerConfig
def test_crawler_config_with_no_source_timezone():
    config = CrawlerConfig(
        site_id="site_1",
        name="Test Crawler",
        enabled=True,
        base_url="https://example.com",
        start_urls=["https://example.com/start"],
        allowed_domains=["example.com"],
        selectors={"title": "h1.title",
                   "content": "div.content"},
        pagination={"max_pages": 5},
        crawler_settings={"randomize_delay": True},
    )
    assert config.source_timezone == "UTC"
def test_crawler_config_with_source_timezone():
    config = CrawlerConfig(
        site_id="site_1",
        name="Test Crawler",
        enabled=True,
        base_url="https://example.com",
        start_urls=["https://example.com/start"],
        allowed_domains=["example.com"],
        selectors={"title": "h1.title",
                   "content": "div.content"},
        pagination={"max_pages": 5},
        crawler_settings={"randomize_delay": True},
        source_timezone="Asia/Tokyo"
    )
    assert config.source_timezone == "Asia/Tokyo"
def test_crawler_config_with_invalid_source_timezone():
    with pytest.raises(ValueError):
        config = CrawlerConfig(
        site_id="site_1",
        name="Test Crawler",
        enabled=True,
        base_url="https://example.com",
        start_urls=["https://example.com/start"],
        allowed_domains=["example.com"],
        selectors={"title": "h1.title",
                   "content": "div.content"},
        pagination={"max_pages": 5},
        crawler_settings={"randomize_delay": True},
        source_timezone="Invalid/Timezone"
    )
