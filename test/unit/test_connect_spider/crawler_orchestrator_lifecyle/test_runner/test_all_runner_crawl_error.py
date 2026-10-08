from src.infrastructure.crawler.scrapy.crawler_orchestrator import CrawlerOrchestrator
from unittest.mock import AsyncMock, Mock
async def test_all_runner_crawl_error():
    repository = Mock()
    crawler_factory = Mock()
    crawler_runner = Mock()
    on_all_jobs_finished = Mock()
    repository.get_enabled_configs = AsyncMock(return_value=[
        config_A := Mock(),
        config_B := Mock(),
        config_C := Mock(),
    ])
    crawler_factory.create_crawler.side_effect = [
        crawler_A := Mock(),
        crawler_B := Mock(),
        crawler_C := Mock(),
    ]
    crawler_runner.crawl = Mock(side_effect=[
        Exception("Crawl error"),
        Exception("Crawl error"),
        Exception("Crawl error"),
    ])
    orchestrator = CrawlerOrchestrator(repository, crawler_factory, crawler_runner, on_all_jobs_finished)
    await orchestrator.schedule()
    assert orchestrator.total_jobs == 3
    assert orchestrator.terminal_jobs == 3
    assert orchestrator.failed_jobs == 3
    assert crawler_runner.crawl.call_count == 3