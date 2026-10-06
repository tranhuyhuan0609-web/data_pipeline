import pytest
from src.domain.entities.crawler_config import CrawlerConfig
@pytest.fixture(scope="function")
def config(request):
    override = getattr(request, 'param', None)
    site_id = override.get('site_id', 'test_site') if override else 'test_site'
    name = override.get('name', 'Test Site') if override else 'Test Site'
    return CrawlerConfig(
        site_id=site_id,
        name=name,
        enabled=True,
        base_url="https://example.com",
        start_urls=["https://example.com"],
        allowed_domains=["example.com"],
        selectors={
            "title": "h1.title::text",
            "content": "div.content::text"
        },
        pagination={
            "enabled": True,
            "next_page": "a.next::attr(href)",
            "max_pages": 10,

        },
        crawler_settings={
            "delay": 1.0,
            "randomize_delay": True,
            "concurrent_requests": 2,
            "download_timeout": 30,
            "retry_enabled": True,
            "max_retries": 3

        })