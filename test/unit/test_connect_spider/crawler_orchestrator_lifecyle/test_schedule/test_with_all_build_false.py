
from unittest.mock import Mock, AsyncMock

from src.infrastructure.crawler.scrapy.crawler_orchestrator import CrawlerOrchestrator
async def test_schedule_all_build_failures_calls_completion_callback():
    repository = Mock()
    crawler_factory = Mock()
    crawler_runner = Mock()
    on_all_jobs_finished = Mock()
    config_A = Mock()
    config_B = Mock()
    repository.get_enabled_configs = AsyncMock(return_value=[
        config_A,
        config_B,
    ])
    crawler_factory.create_crawler.side_effect = Exception(
        "Failed to create crawler"
    )
    orchestrator = CrawlerOrchestrator(repository, 
                                       crawler_factory, 
                                       crawler_runner, 
                                       on_all_jobs_finished
                                       )
    await orchestrator.schedule()
    assert orchestrator.build_failed == 2
    on_all_jobs_finished.assert_called_once_with()
    assert orchestrator.total_jobs == 0
    repository.get_enabled_configs.assert_awaited_once_with()