import unittest
from unittest.mock import Mock
from src.infrastructure.crawler.scrapy.crawler_orchestrator import CrawlerOrchestrator
def test_build_jobs_with_none_enabled_config():
    repository = Mock()
    crawler_factory = Mock()
    crawler_runner = Mock()
    repository.get_enabled_configs.return_value = []
    orchestrator = CrawlerOrchestrator(repository, crawler_factory, crawler_runner)
    jobs = orchestrator.build_jobs()    
    assert jobs == []
    crawler_factory.assert_not_called()