from unittest.mock import Mock, AsyncMock, patch

from src.application.application import Application


def test_shutdown_callback_starts_shutdown():
    pool = Mock()
    pool.close = AsyncMock()

    orchestrator = Mock()
    reactor = Mock()

    application = Application(
        orchestrator=orchestrator,
        reactor=reactor,
        pool=pool,
    )

    with patch(
        "src.application.application.defer.ensureDeferred"
    ) as mock_ensure_deferred:

        application.shutdown()
        coroutine = mock_ensure_deferred.call_args.args[0]
        coroutine.close()

    mock_ensure_deferred.assert_called_once()
    assert mock_ensure_deferred.call_args.args[0] is not None