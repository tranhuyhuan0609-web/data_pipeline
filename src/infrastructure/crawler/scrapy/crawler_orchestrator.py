import logging

from scrapy import signals
from scrapy.signalmanager import dispatcher

from src.infrastructure.crawler.scrapy.crawler_job import CrawlerJob


log = logging.getLogger(__name__)


class CrawlerOrchestrator:
    def __init__(
        self,
        repository,
        crawler_factory,
        crawler_runner,
        on_all_jobs_finished=None,
    ):
        self.repository = repository
        self.crawler_factory = crawler_factory
        self.crawler_runner = crawler_runner

        self.terminal_jobs = 0
        self.total_jobs = 0
        self.failed_jobs = 0
        self.on_all_jobs_finished = on_all_jobs_finished

        self.list_of_spiders = set()
        self.build_failed = 0

        dispatcher.connect(
            self.handle_spider_closed,
            signal=signals.spider_closed,
        )

    async def build_jobs(self) -> list[CrawlerJob]:
        crawler_jobs = []

        crawler_configs = await self.repository.get_enabled_configs()

        for config in crawler_configs:
            try:
                crawler = self.crawler_factory.create_crawler(config)

                crawler_jobs.append(
                    CrawlerJob(
                        crawler=crawler,
                        config=config,
                    )
                )

            except Exception as e:
                log.error(
                    f"Error creating crawler for config {config}: {e}"
                )
                self.build_failed += 1
                continue

        self.total_jobs = len(crawler_jobs)

        return crawler_jobs

    async def schedule(self):
        jobs = await self.build_jobs()

        if not jobs:
            if self.build_failed == 0:
                log.error(
                    "No enabled crawler configurations found. Exiting."
                )

                if self.on_all_jobs_finished:
                    self.on_all_jobs_finished()

                return

            elif self.build_failed > 0:
                log.error(
                    f"All crawler configurations failed to build. "
                    f"Exiting. Build failed count: {self.build_failed}"
                )
                if self.on_all_jobs_finished:
                    self.on_all_jobs_finished()
                return

        for job in jobs:
            try:
                self.crawler_runner.crawl(
                    job.crawler,
                    crawler_config=job.config,
                )

                self.list_of_spiders.add(job.crawler)

            except Exception as e:
                log.exception(
                    f"Error scheduling crawler for config "
                    f"{job.config}: {e}"
                )

                self.failed_jobs += 1
                self.terminal_jobs += 1

        self._check_all_jobs_finished()

    def handle_spider_closed(self, spider, reason: str):
        if spider not in self.list_of_spiders:
            log.error(
                f"Received spider_closed signal for unknown spider: "
                f"{spider}. Ignoring."
            )
            return

        self.list_of_spiders.remove(spider)

        self.terminal_jobs += 1

        if reason != "finished":
            self.failed_jobs += 1

        self._check_all_jobs_finished()

    def _check_all_jobs_finished(self):
        if self.total_jobs > 0:
            if self.terminal_jobs == self.total_jobs:
                dispatcher.disconnect(
                    self.handle_spider_closed,
                    signal=signals.spider_closed,
                )

                if self.on_all_jobs_finished:
                    self.on_all_jobs_finished()