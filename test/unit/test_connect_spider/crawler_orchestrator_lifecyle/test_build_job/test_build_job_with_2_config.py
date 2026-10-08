from src.infrastructure.crawler.scrapy.crawler_orchestrator import CrawlerOrchestrator
from src.infrastructure.crawler.scrapy.crawler_job import CrawlerJob
from unittest.mock import AsyncMock, Mock
async def test_build_jobs_with_2_enabled_configs():
    repository = Mock()
    crawler_factory = Mock()
    crawler_runner = Mock()
    config_A = Mock()
    config_B = Mock()
    repository.get_enabled_configs = AsyncMock(return_value=[
        config_A,
        config_B,
    ])
    crawler_A = Mock()
    crawler_B = Mock()
    crawler_factory.create_crawler.side_effect = [
        crawler_A,
        crawler_B,
    ]
    orchestrator = CrawlerOrchestrator(repository, crawler_factory, crawler_runner)
    jobs = await orchestrator.build_jobs()
   
    assert len(jobs) == 2
    assert jobs[0].crawler == crawler_A
    assert jobs[0].config == config_A
    assert jobs[1].crawler == crawler_B
    assert jobs[1].config == config_B
    crawler_factory.create_crawler.assert_any_call(config_A)
    crawler_factory.create_crawler.assert_any_call(config_B)