from src.infrastructure.crawler.scrapy.crawler_orchestrator import CrawlerOrchestrator
from unittest.mock import Mock
async def test_handle_crawler_closed():
    repository = Mock()
    crawler_factory = Mock()
    on_all_jobs_finished = Mock()
    crawler_runner = Mock()
    orchestrator = CrawlerOrchestrator(repository, crawler_factory, crawler_runner, on_all_jobs_finished)
    orchestrator.total_jobs = 2
    orchestrator.terminal_jobs = 0
    orchestrator.list_of_spiders = {crawler_A := Mock()}
    orchestrator.handle_spider_closed(spider=crawler_A, reason="finished")
    assert orchestrator.terminal_jobs == 1
    assert orchestrator.failed_jobs == 0
    on_all_jobs_finished.assert_not_called()