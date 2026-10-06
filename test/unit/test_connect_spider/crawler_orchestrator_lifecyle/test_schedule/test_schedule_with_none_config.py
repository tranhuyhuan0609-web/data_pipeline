from src.infrastructure.crawler.scrapy.crawler_orchestrator import CrawlerOrchestrator
from unittest.mock import Mock
def test_schedule_with_none_enabled_config():
    repository = Mock()
    repository.get_enabled_configs.return_value = []
    crawler_factory = Mock()
    crawler_runner = Mock()
    on_all_jobs_finished = Mock()
    orchestrator = CrawlerOrchestrator(repository, crawler_factory, crawler_runner, on_all_jobs_finished)
    orchestrator.schedule()
    crawler_runner.crawl.assert_not_called()
    assert crawler_factory.create_crawler.call_count == 0
    repository.get_enabled_configs.assert_called_once()
    on_all_jobs_finished.assert_called_once()
