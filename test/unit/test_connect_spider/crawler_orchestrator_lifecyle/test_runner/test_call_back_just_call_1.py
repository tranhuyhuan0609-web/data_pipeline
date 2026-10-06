from src.infrastructure.crawler.scrapy.crawler_orchestrator import CrawlerOrchestrator
from unittest.mock import Mock
def test_caller_callback_just_call_one():
    repository = Mock()
    crawler_factory = Mock()
    crawler_runner = Mock()
    on_all_jobs_finished = Mock()
    repository.get_enabled_configs.return_value = [
        config_A := Mock()
    ]
    crawler_factory.create_crawler.side_effect = [
        crawler_A := Mock(),
    ]
    crawler_runner.crawl.side_effect = [
        None,
    ]
    orchestrator = CrawlerOrchestrator(repository, crawler_factory, crawler_runner, on_all_jobs_finished)
    orchestrator.schedule()
    orchestrator.handle_spider_closed(spider = crawler_A, reason = "finished")
    assert orchestrator.terminal_jobs == 1
    on_all_jobs_finished.assert_called_once()
    assert orchestrator.list_of_spiders == set()
    orchestrator.handle_spider_closed(spider = crawler_A, reason = "finished")
    assert orchestrator.terminal_jobs == 1
    on_all_jobs_finished.assert_called_once()
    orchestrator.handle_spider_closed(spider = crawler_A, reason = "failed")
    assert orchestrator.terminal_jobs == 1
    assert orchestrator.failed_jobs == 0