import pytest
from src.domain.entities.crawler_config import ( CrawlerConfig,
                                                Selectors,
                                                Pagination,
                                                CrawlerSettings)

@pytest.fixture(scope = "function")
def config(request):
    override = getattr(request, 'param', {})
    site_id = override.get('site_id', 'test_site')
    name = override.get('name', 'Test Site')
    enabled = override.get('enabled', True)
    base_url = override.get('base_url', 'https://example.com')
    start_urls = override.get('start_urls', ['https://example.com/page1'])
    allowed_domains = override.get('allowed_domains', ['example.com'])
    max_pages = override.get('max_pages', 3)
    pagination_enabled = override.get('pagination_enabled', True)
    delay = override.get('delay', 1.0)
    randomize_delay = override.get('randomize_delay', True)
    concurrent_requests = override.get('concurrent_requests', 2)
    download_timeout = override.get('download_timeout', 30)
    max_retries = override.get('max_retries', 3)
    retry_enabled = override.get('retry_enabled', True)
    title = override.get('title', 'h1.title')
    content = override.get('content', 'div.content')
    next_page = override.get('next_page', 'a.next')
    publish_at = override.get('publish_at', 'span.publish-date')
    return CrawlerConfig(
        site_id=site_id,
        name=name,
        enabled=enabled,
        base_url=base_url,
        start_urls=start_urls,
        allowed_domains=allowed_domains,
        selectors=Selectors(
            title=title,
            content=content,
            publish_at=publish_at,
        ),
        pagination=Pagination(
            enabled=pagination_enabled,
            next_page=next_page,
            max_pages=max_pages
        ),
        crawler_settings=CrawlerSettings(
            delay=delay,
            randomize_delay=randomize_delay,
            concurrent_requests=concurrent_requests,
            download_timeout=download_timeout,
            retry_enabled=retry_enabled,
            max_retries=max_retries,
         
        )
    )