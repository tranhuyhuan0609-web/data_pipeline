from src.infrastructure.crawler.scrapy.crawler_orchestrator import CrawlerOrchestrator
from unittest.mock import Mock
def test_schedule_with_2_enabled_configs():
    repository = Mock()
    crawler_factory = Mock()
    crawler_runner = Mock()
    on_all_jobs_finished = Mock()
    config_A = Mock()
    config_B = Mock()
    repository.get_enabled_configs.return_value = [
        config_A,
        config_B,
    ]
    crawler_A = Mock()
    crawler_B = Mock()
    crawler_factory.create_crawler.side_effect = [
        crawler_A,
        crawler_B,
    ]
    orchestrator = CrawlerOrchestrator(repository, 
                                       crawler_factory, 
                                       crawler_runner, 
                                       on_all_jobs_finished
                                       )
    orchestrator.schedule()
    assert crawler_runner.crawl.call_count == 2
    crawler_runner.crawl.assert_any_call(crawler_A, crawler_config=config_A)
    crawler_runner.crawl.assert_any_call(crawler_B, crawler_config=config_B)