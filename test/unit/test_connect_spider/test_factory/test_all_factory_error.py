from src.infrastructure.crawler.scrapy.crawler_orchestrator import CrawlerOrchestrator
from unittest.mock import AsyncMock, Mock
async def test_create_factory_all_error():
    repository = Mock()
    crawler_factory = Mock()
    crawler_runner = Mock()
    on_all_jobs_finished = Mock()
    orchestrator = CrawlerOrchestrator(repository, crawler_factory, crawler_runner, on_all_jobs_finished)
    repository.get_enabled_configs = AsyncMock(return_value=[
        config_A := Mock(),
        config_B := Mock(),
        config_C := Mock(),
    ])
    crawler_factory.create_crawler = Mock(side_effect=[Exception("Factory error"),
                                          Exception("Factory error"),
                                          Exception("Factory error")]   )
    await orchestrator.schedule()
    assert orchestrator.total_jobs == 0
    assert orchestrator.terminal_jobs == 0
    assert orchestrator.list_of_spiders == set()
    assert orchestrator.failed_jobs == 0
    assert orchestrator.build_failed == 3
    assert crawler_runner.crawl.call_count == 0
    on_all_jobs_finished.assert_called_once()