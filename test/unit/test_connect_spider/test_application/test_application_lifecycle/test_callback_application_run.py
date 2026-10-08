from unittest.mock import MagicMock, patch

from src.application.application import Application


def test_run_callback_starts_application():
    orchestrator = MagicMock()
    reactor = MagicMock()
    pool = MagicMock()

    application = Application(
        orchestrator=orchestrator,
        reactor=reactor,
        pool=pool,
    )

    with patch(
        "src.application.application.defer.ensureDeferred"
    ) as mock_ensure_deferred:

        application.run()

        callback = reactor.callWhenRunning.call_args.args[0]
        callback()
        coroutine = mock_ensure_deferred.call_args.args[0]
        coroutine.close()

    reactor.callWhenRunning.assert_called_once()
    mock_ensure_deferred.assert_called_once()
    reactor.run.assert_called_once_with()