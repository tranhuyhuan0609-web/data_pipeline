from src.infrastructure.crawler.scrapy.crawler_orchestrator import CrawlerOrchestrator
from unittest.mock import AsyncMock, Mock,patch
from scrapy import signals
from scrapy.signalmanager import dispatcher
async def test_dispatcher_connect():
    target = 'src.infrastructure.crawler.scrapy.crawler_orchestrator.dispatcher'
    with patch(f'{target}.connect') as mock_connect:
        with patch(f'{target}.disconnect') as mock_disconnect:
            repository = Mock()
            crawler_factory = Mock()
            crawler_runner = Mock()
            on_all_jobs_finished = Mock()
            repository.get_enabled_configs = AsyncMock(return_value=[
                config_A := Mock(),
                config_B := Mock(),
            ])
            crawler_factory.create_crawler.side_effect = [
                crawler_A := Mock(),
                crawler_B := Mock(),
            ]
            orchestrator = CrawlerOrchestrator(repository, crawler_factory, crawler_runner, on_all_jobs_finished)
            mock_connect.assert_called_once_with(orchestrator.handle_spider_closed, signal=signals.spider_closed)
            await orchestrator.schedule()
            mock_disconnect.assert_not_called()
            orchestrator.handle_spider_closed(crawler_A, reason='finished')
            mock_disconnect.assert_not_called()
            orchestrator.handle_spider_closed(crawler_B, reason='finished')
            mock_disconnect.assert_called_once_with(orchestrator.handle_spider_closed, signal=signals.spider_closed)
            on_all_jobs_finished.assert_called_once()