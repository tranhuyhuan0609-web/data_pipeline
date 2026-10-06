from unittest.mock import Mock, patch

from scrapy import signals

from src.infrastructure.crawler.scrapy.crawler_orchestrator import CrawlerOrchestrator


def test_disconnect_before_callback():
    target = "src.infrastructure.crawler.scrapy.crawler_orchestrator.dispatcher"

    call_order = []

    with patch(f"{target}.connect") as mock_connect:
        with patch(f"{target}.disconnect") as mock_disconnect:

            mock_disconnect.side_effect = lambda *args, **kwargs: call_order.append(
                "disconnect"
            )

            on_all_jobs_finished = Mock(
                side_effect=lambda: call_order.append("callback")
            )

            repository = Mock()
            crawler_factory = Mock()
            crawler_runner = Mock()

            config_A = Mock()
            crawler_A = Mock()

            repository.get_enabled_configs.return_value = [config_A]
            crawler_factory.create_crawler.return_value = crawler_A

            orchestrator = CrawlerOrchestrator(
                repository,
                crawler_factory,
                crawler_runner,
                on_all_jobs_finished,
            )

            orchestrator.schedule()

            orchestrator.handle_spider_closed(
                crawler_A,
                reason="finished",
            )

            assert call_order == ["disconnect", "callback"]
            assert mock_disconnect.call_count == 1
            on_all_jobs_finished.assert_called_once