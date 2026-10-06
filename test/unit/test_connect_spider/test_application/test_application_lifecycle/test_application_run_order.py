from unittest.mock import AsyncMock, Mock

from src.application.application import Application
def test_application_run_order():
    order = []
    orchestrator = Mock()
    pool = Mock()
    reactor = Mock()
    orchestrator.schedule.side_effect = AsyncMock(side_effect=lambda: order.append("schedule"))
    reactor.run.side_effect = lambda: order.append("run")
    application = Application(
        orchestrator,
        reactor,
        pool
    )
    application.run()
    assert order == ["schedule", "run"]