from src.domain.entities.crawler_config import CrawlerConfig
from pydantic import ValidationError
import pytest
def test_crawler_config_validation():
    with pytest.raises(ValidationError):
        CrawlerConfig(
            site_id="site_123",
            name="Test Site",
            enabled=True,
            base_url="https://example.com",
            start_urls=["ettps://newsexample.com/article"],  
            allowed_domains=["example.com"],
            selectors={
                "title": "h1.title",
                "author": "span.author",
                "content": "div.content",
                "category": "span.category",
                "published_at": "time.published"
            },
            pagination={
                "enabled": True,
                "next_page": "a.next"
            },
            crawler_settings={
                "delay": 1.0,
                "randomize_delay": True,
                "concurrent_requests": 2,
                "download_timeout": 30,
                "retry_enabled": True,
                "max_retries": 3
            }
        )