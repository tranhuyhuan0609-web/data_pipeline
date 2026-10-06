
from src.infrastructure.crawler.scrapy.generic_spider import GenericSpider
from src.infrastructure.crawler.scrapy.setting_adapter import to_scrapy_settings
from src.domain.entities.crawler_config import CrawlerConfig
from scrapy.settings import Settings
from scrapy.crawler import Crawler
def create_scrapy_settings(crawler_config: CrawlerConfig) -> Settings:
    scrapy_settings_dict = to_scrapy_settings(crawler_config.crawler_settings)
    scrapy_settings = Settings()
    for key, value in scrapy_settings_dict.items():
        scrapy_settings.set(key, value)
    return scrapy_settings
class CrawlerFactory:
    def __init__(self, spider_class=GenericSpider):
        self.spider_class = spider_class
    def create_crawler(self, crawler_config: CrawlerConfig) -> Crawler:
        scrapy_settings = create_scrapy_settings(crawler_config)
        crawler = Crawler(self.spider_class,
                          settings=scrapy_settings,
                          )
        return crawler
    