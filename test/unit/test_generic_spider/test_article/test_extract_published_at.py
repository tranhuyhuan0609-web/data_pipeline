from src.domain.entities.crawler_config import CrawlerConfig
from scrapy.http import HtmlResponse, Request
from datetime import datetime, timezone
from src.infrastructure.crawler.scrapy.generic_spider import GenericSpider
def test_extract_published_at_with_source_timezone():
    crawler_config = CrawlerConfig(
        site_id="site_1",
        name="Test Crawler",
        enabled=True,
        base_url="https://example.com",
        start_urls=["https://example.com/start"],
        allowed_domains=["example.com"],
        selectors={"title": "h1.title",
                   "content": "div.content",
                   "published_at": "span.date::text"},
        pagination={"max_pages": 5},
        crawler_settings={"randomize_delay": True},
        source_timezone="Asia/Tokyo"
    )

    spider = GenericSpider(crawler_config=crawler_config)

    html_content = """
    <html>
        <body>
            <span class="date">2026-10-07 10:00:00</span>
        </body>
    </html>
    """

    response = HtmlResponse(
        url="https://example.com/article/1",
        body=html_content,
        encoding='utf-8',
        request=Request(url="https://example.com/article/1")
    )

    expected_datetime = datetime(2026, 10, 7, 1, 0, 0, tzinfo=timezone.utc)

    assert spider.extract_published_at(response) == expected_datetime