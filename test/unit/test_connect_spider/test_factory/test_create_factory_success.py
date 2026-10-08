from unittest.mock import Mock, patch

from src.infrastructure.crawler.scrapy.crawler_factory import CrawlerFactory


def test_create_crawler_success():
    spider_class = Mock()
    crawler_config = Mock()
    crawler = Mock()
    scrapy_settings = Mock()

    factory = CrawlerFactory(
        spider_class=spider_class
    )

    with patch(
        "src.infrastructure.crawler.scrapy.crawler_factory.create_scrapy_settings",
        return_value=scrapy_settings,
    ) as mock_create_settings, patch(
        "src.infrastructure.crawler.scrapy.crawler_factory.Crawler",
        return_value=crawler,
    ) as mock_crawler:

        result = factory.create_crawler(crawler_config)

    mock_create_settings.assert_called_once_with(crawler_config)

    mock_crawler.assert_called_once_with(
        spider_class,
        settings=scrapy_settings,
    )

    assert result is crawler