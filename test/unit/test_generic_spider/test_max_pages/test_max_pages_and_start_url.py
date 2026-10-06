from src.domain.entities.crawler_config import ( CrawlerConfig,
                                                Selectors,
                                                Pagination,
                                                CrawlerSettings)
import pytest
from pydantic import HttpUrl

def test_max_pages_is_none():
    config = CrawlerConfig(
        site_id="test_site",
        name="Test Site",
        enabled=True,
        base_url="https://example.com",
        start_urls=["https://example.com/page1", "https://example.com/page2"],
        allowed_domains=["example.com"],
        selectors=Selectors(
            title="h1.title",
            content="div.content"
        ),
        pagination=Pagination(
            enabled=True,
            next_page="a.next",
            max_pages=None
        ),
        crawler_settings=CrawlerSettings(
            delay=1.0,
            randomize_delay=True,
            concurrent_requests=2,
            download_timeout=30,
            retry_enabled=True,
            max_retries=3
        )
    )
    assert config.pagination.max_pages is None
    assert config.start_urls == [HttpUrl("https://example.com/page1"), HttpUrl("https://example.com/page2")]
def test_max_pages_is_set():
    with pytest.raises(ValueError):
        CrawlerConfig(
            site_id="test_site",
            name="Test Site",
            enabled=True,
            base_url="https://example.com",
            start_urls=["https://example.com/page1", "https://example.com/page2", "https://example.com/page3"],
            allowed_domains=["example.com"],
            selectors=Selectors(
                title="h1.title",
                content="div.content"
            ),
            pagination=Pagination(
                enabled=True,
                next_page="a.next",
                max_pages=2
            ),
            crawler_settings=CrawlerSettings(
                delay=1.0,
                randomize_delay=True,
                concurrent_requests=2,
                download_timeout=30,
                retry_enabled=True,
                max_retries=3
            )
        )