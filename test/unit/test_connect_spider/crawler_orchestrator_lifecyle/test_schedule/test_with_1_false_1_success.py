from unittest.mock import Mock, AsyncMock

from src.infrastructure.crawler.scrapy.crawler_orchestrator import (
    CrawlerOrchestrator,
)


async def test_schedule_with_1_build_failure_and_1_success():
    repository = Mock()
    crawler_factory = Mock()
    crawler_runner = Mock()
    on_all_jobs_finished = Mock()

    config_A = Mock()
    config_B = Mock()
    crawler_B = Mock()

    repository.get_enabled_configs = AsyncMock(
        return_value=[
            config_A,
            config_B,
        ]
    )

    crawler_factory.create_crawler.side_effect = [
        Exception("Failed to create crawler"),
        crawler_B,
    ]

    orchestrator = CrawlerOrchestrator(
        repository,
        crawler_factory,
        crawler_runner,
        on_all_jobs_finished,
    )

    await orchestrator.schedule()

    assert orchestrator.build_failed == 1
    assert orchestrator.total_jobs == 1
    assert orchestrator.terminal_jobs == 0

    repository.get_enabled_configs.assert_awaited_once_with()

    crawler_runner.crawl.assert_called_once()

    assert crawler_B in orchestrator.list_of_spiders

    on_all_jobs_finished.assert_not_called()