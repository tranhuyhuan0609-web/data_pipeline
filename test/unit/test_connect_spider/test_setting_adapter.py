from src.domain.entities.crawler_config import CrawlerSettings
from src.infrastructure.crawler.scrapy.setting_adapter import to_scrapy_settings
def test_to_scrapy_settings_with_retry_enabled_true():
    crawler_settings = CrawlerSettings(
        delay=2.0,
        randomize_delay=False,
        concurrent_requests=5,
        download_timeout=60,
        retry_enabled=True,
        max_retries=4
    )
    scrapy_settings = to_scrapy_settings(crawler_settings)
    assert scrapy_settings["DOWNLOAD_DELAY"] == 2.0
    assert scrapy_settings["RANDOMIZE_DOWNLOAD_DELAY"] is False
    assert scrapy_settings["CONCURRENT_REQUESTS"] == 5
    assert scrapy_settings["DOWNLOAD_TIMEOUT"] == 60
    assert scrapy_settings["RETRY_ENABLED"] is True
    assert scrapy_settings["RETRY_TIMES"] == 4
def test_to_scrapy_settings_with_retry_enabled_false():
    crawler_settings = CrawlerSettings(
        delay=1.0,
        randomize_delay=True,
        concurrent_requests=3,
        download_timeout=30,
        retry_enabled=False,
        max_retries=0
    )
    scrapy_settings = to_scrapy_settings(crawler_settings)
    assert scrapy_settings["DOWNLOAD_DELAY"] == 1.0
    assert scrapy_settings["RANDOMIZE_DOWNLOAD_DELAY"] is True
    assert scrapy_settings["CONCURRENT_REQUESTS"] == 3
    assert scrapy_settings["DOWNLOAD_TIMEOUT"] == 30
    assert scrapy_settings["RETRY_ENABLED"] is False
    assert scrapy_settings["RETRY_TIMES"] == 0