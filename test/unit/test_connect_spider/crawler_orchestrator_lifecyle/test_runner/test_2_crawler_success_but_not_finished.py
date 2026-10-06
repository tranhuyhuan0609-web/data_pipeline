from src.infrastructure.crawler.scrapy.crawler_orchestrator import CrawlerOrchestrator
from unittest.mock import Mock
def test_crawler_runner_success_but_not_finished():
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
    assert orchestrator.terminal_jobs == 0
    assert orchestrator.failed_jobs == 0
    assert orchestrator.total_jobs == 2
    assert crawler_runner.crawl.call_count == 2
    on_all_jobs_finished.assert_not_called()