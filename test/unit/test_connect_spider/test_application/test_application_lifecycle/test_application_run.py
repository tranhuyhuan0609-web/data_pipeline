from unittest.mock import MagicMock

from src.application.application import Application


def test_run_registers_startup_and_runs_reactor():
    orchestrator = MagicMock()
    reactor = MagicMock()
    pool = MagicMock()

    application = Application(
        orchestrator=orchestrator,
        reactor=reactor,
        pool=pool,
    )

    application.run()

    reactor.callWhenRunning.assert_called_once()
    reactor.run.assert_called_once_with()