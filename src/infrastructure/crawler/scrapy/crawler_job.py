from dataclasses import dataclass
from scrapy.crawler import Crawler
from src.domain.entities.crawler_config import CrawlerConfig
@dataclass
class CrawlerJob:
    crawler: Crawler
    config: CrawlerConfig