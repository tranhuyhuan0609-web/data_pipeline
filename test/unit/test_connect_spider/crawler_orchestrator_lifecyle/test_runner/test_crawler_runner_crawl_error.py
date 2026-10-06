from src.infrastructure.crawler.scrapy.crawler_orchestrator import CrawlerOrchestrator
from unittest.mock import Mock
def test_crawler_runner_crawl_error():
    repository = Mock()
    crawler_factory = Mock()
    crawler_runner = Mock()
    crawler_runner.crawl.side_effect = [
        None,
        Exception("Crawl error"),
        None,
    ]
    on_all_jobs_finished = Mock()
    repository.get_enabled_configs.return_value = [
        config_A := Mock(),
        config_B := Mock(),
        config_C := Mock(),
    ]
    crawler_factory.create_crawler.side_effect = [
        crawler_A := Mock(),
        crawler_B := Mock(),
        crawler_C := Mock(),
    ]
    orchestrator = CrawlerOrchestrator(repository, crawler_factory, crawler_runner, on_all_jobs_finished)
    orchestrator.schedule()
    assert orchestrator.total_jobs == 3
    assert orchestrator.terminal_jobs == 1
    assert orchestrator.list_of_spiders == {crawler_A, crawler_C}
    assert orchestrator.failed_jobs == 1
    assert crawler_runner.crawl.call_count == 3
    orchestrator.handle_spider_closed(spider=crawler_A, reason="finished")
    assert orchestrator.terminal_jobs == 2
    on_all_jobs_finished.assert_not_called()
    orchestrator.handle_spider_closed(spider=crawler_C, reason="failed")
    assert orchestrator.terminal_jobs == 3
    on_all_jobs_finished.assert_called_once()
    orchestrator.handle_spider_closed(spider=crawler_B, reason="finished")
    assert orchestrator.terminal_jobs == 3
    on_all_jobs_finished.assert_called_once()
   