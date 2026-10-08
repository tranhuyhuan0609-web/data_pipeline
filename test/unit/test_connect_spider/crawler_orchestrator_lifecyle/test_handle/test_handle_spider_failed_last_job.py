from src.infrastructure.crawler.scrapy.crawler_orchestrator import CrawlerOrchestrator
from unittest.mock import Mock
def test_handle_crawler_closed_failed_last_job():
    repository = Mock()
    crawler_factory = Mock()
    on_all_jobs_finished = Mock()
    crawler_runner = Mock()
    orchestrator = CrawlerOrchestrator(repository, crawler_factory, crawler_runner, on_all_jobs_finished)
    orchestrator.total_jobs = 1
    orchestrator.terminal_jobs = 0
    orchestrator.list_of_spiders = {crawler_A := Mock()}
    orchestrator.handle_spider_closed(spider=crawler_A, reason="failed")
    assert orchestrator.terminal_jobs == 1
    assert orchestrator.failed_jobs == 1
    on_all_jobs_finished.assert_called_once()
    assert crawler_A not in orchestrator.list_of_spiders
