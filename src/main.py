from twisted.internet import asyncioreactor

import asyncio

if hasattr(asyncio, "WindowsSelectorEventLoopPolicy"):
    asyncio.set_event_loop_policy(
        asyncio.WindowsSelectorEventLoopPolicy()
    )

from twisted.internet import asyncioreactor

asyncioreactor.install()

from twisted.internet import reactor

from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner

from src.config.settings import load_settings

from src.application.application import Application
from src.infrastructure.crawler.scrapy.crawler_orchestrator import CrawlerOrchestrator

from src.infrastructure.crawler.scrapy.crawler_factory import CrawlerFactory
from src.infrastructure.crawler.scrapy.generic_spider import GenericSpider

from src.infrastructure.postgres_db.pool import PostgresPoolFactory
from src.infrastructure.repositories.postgresql_config_repository import (
    PostgresConfigRepository,
)


def main():

    settings = load_settings()

    
    pool_factory = PostgresPoolFactory(
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        dbname=settings.POSTGRES_DB,
    )

    pool = pool_factory.create_pool()

   
    repository = PostgresConfigRepository(
        pool=pool,
        table_name="crawler_config",
    )

   
    crawler_factory = CrawlerFactory(
        spider_class=GenericSpider,
    )

    crawler_runner = CrawlerRunner()

    
    orchestrator = CrawlerOrchestrator(
        repository=repository,
        crawler_factory=crawler_factory,
        crawler_runner=crawler_runner,
    )

    
    application = Application(
        orchestrator=orchestrator,
        reactor=reactor,
        pool=pool,
    )

   
    application.run()


if __name__ == "__main__":
    main()