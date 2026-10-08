
import pytest
from scrapy.crawler import CrawlerRunner

from src.infrastructure.crawler.scrapy.crawler_factory import CrawlerFactory
from src.infrastructure.crawler.scrapy.generic_spider import GenericSpider
from src.domain.entities.crawler_config import CrawlerConfig


@pytest.fixture
def crawler_config():
    return CrawlerConfig(
        site_id="site_1",
        name="Test Crawler",
        enabled=True,
        base_url="https://example.com",
        start_urls=["https://example.com/start"],
        allowed_domains=["example.com"],
        selectors={
            "title": "h1.title",
            "content": "div.content",
        },
        pagination={
            "enabled": False,
            "max_pages": 5,
        },
        crawler_settings={
            "randomize_delay": True,
        },
        source_timezone="Asia/Ho_Chi_Minh",
    )


def test_crawler_factory_creates_crawler(crawler_config):
    factory = CrawlerFactory(
        spider_class=GenericSpider
    )

    crawler = factory.create_crawler(crawler_config)

    assert crawler.spidercls is GenericSpider
    assert crawler.settings.get("DOWNLOAD_DELAY") == 1.0
    assert crawler.settings.get("CONCURRENT_REQUESTS") == 1
    assert crawler.settings.get("DOWNLOAD_TIMEOUT") == 30