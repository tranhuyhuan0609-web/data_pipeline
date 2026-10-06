from src.domain.entities.crawler_config import CrawlerSettings
def to_scrapy_settings(crawler_settings: CrawlerSettings) -> dict:
    return {
        "DOWNLOAD_DELAY": crawler_settings.delay,
        "RANDOMIZE_DOWNLOAD_DELAY": crawler_settings.randomize_delay,
        "CONCURRENT_REQUESTS": crawler_settings.concurrent_requests,
        "DOWNLOAD_TIMEOUT": crawler_settings.download_timeout,
        "RETRY_ENABLED": crawler_settings.retry_enabled,
        "RETRY_TIMES": crawler_settings.max_retries,
    }
