from src.infrastructure.crawler.scrapy.crawler_orchestrator import CrawlerOrchestrator
from unittest.mock import Mock
def test_create_factory_error():
    repository = Mock()
    crawler_factory = Mock()
    crawler_runner = Mock()
    on_all_jobs_finished = Mock()
    orchestrator = CrawlerOrchestrator(repository, crawler_factory, crawler_runner, on_all_jobs_finished)
    repository.get_enabled_configs.return_value = [
        config_A := Mock(),
        config_B := Mock(),
        config_C := Mock(),
    ]
    crawler_factory.create_crawler.side_effect = [
        crawler_A := Mock(),
        Exception("Factory error"),
        crawler_C := Mock(),
    ]
    orchestrator.schedule()
    assert orchestrator.total_jobs == 2
    assert orchestrator.terminal_jobs == 0
    assert orchestrator.list_of_spiders == {crawler_A, crawler_C}
    assert orchestrator.failed_jobs == 0
    assert crawler_runner.crawl.call_count == 2
    on_all_jobs_finished.assert_not_called()