from src.infrastructure.crawler.scrapy.crawler_orchestrator import CrawlerOrchestrator
from unittest.mock import AsyncMock, Mock
async def test_crawler_runner_crawl_not_crash_on_error():
    repository = Mock()
    crawler_factory = Mock()
    crawler_runner = Mock()
    on_all_jobs_finished = Mock()
    repository.get_enabled_configs = AsyncMock(return_value=[
        config_A := Mock(),
        config_B := Mock(),
        config_C := Mock(),
    ])
    crawler_runner.crawl.side_effect = [
        None,
        Exception("Crawl error"),
        None,
    ]
    orchestrator = CrawlerOrchestrator(repository, crawler_factory, crawler_runner, on_all_jobs_finished)
    crawler_factory.create_crawler.side_effect = [
        crawler_A := Mock(),
        crawler_B := Mock(),
        crawler_C := Mock(),
    ]
    await orchestrator.schedule()
    assert orchestrator.terminal_jobs == 1
    assert orchestrator.failed_jobs == 1
    assert crawler_runner.crawl.call_count == 3
    crawler_runner.crawl.assert_any_call(crawler_A, crawler_config=config_A)
    crawler_runner.crawl.assert_any_call(crawler_B, crawler_config=config_B)
    crawler_runner.crawl.assert_any_call(crawler_C, crawler_config=config_C)