from src.infrastructure.crawler.scrapy.crawler_orchestrator import CrawlerOrchestrator
from unittest.mock import Mock
def test_duplicate_but_exists_crawler():
    repository = Mock()
    crawler_factory = Mock()
    crawler_runner = Mock()
    on_all_jobs_finished = Mock()
    repository.get_enabled_configs.return_value = [
        config_A := Mock(),
        config_B := Mock(),
    ]
    crawler_factory.create_crawler.side_effect = [
        crawler_A := Mock(),
        crawler_B := Mock(),
    ]
    crawler_runner.crawl.side_effect = [
        None,
        None,
    ]
    orchestrator = CrawlerOrchestrator(repository, crawler_factory, crawler_runner, on_all_jobs_finished)
    orchestrator.schedule()
    orchestrator.handle_spider_closed(spider = crawler_A, reason = "finished")
    assert orchestrator.terminal_jobs == 1
    on_all_jobs_finished.assert_not_called()
    orchestrator.handle_spider_closed(spider = crawler_A, reason = "finished")
    assert orchestrator.terminal_jobs == 1
    on_all_jobs_finished.assert_not_called()
    orchestrator.handle_spider_closed(spider = crawler_B, reason = "finished")
    assert orchestrator.terminal_jobs == 2
    on_all_jobs_finished.assert_called_once()