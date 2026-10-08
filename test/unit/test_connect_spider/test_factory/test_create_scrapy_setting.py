from unittest.mock import Mock, patch

from scrapy.settings import Settings

from src.infrastructure.crawler.scrapy.crawler_factory import (
    create_scrapy_settings,
)


def test_create_scrapy_settings():
    crawler_config = Mock()

    scrapy_settings_dict = {
        "DOWNLOAD_DELAY": 2,
        "CONCURRENT_REQUESTS": 16,
    }

    with patch(
        "src.infrastructure.crawler.scrapy.crawler_factory.to_scrapy_settings",
        return_value=scrapy_settings_dict,
    ) as mock_to_scrapy_settings:

        result = create_scrapy_settings(crawler_config)

    mock_to_scrapy_settings.assert_called_once_with(
        crawler_config.crawler_settings
    )

    assert isinstance(result, Settings)
    assert result.get("DOWNLOAD_DELAY") == 2
    assert result.get("CONCURRENT_REQUESTS") == 16