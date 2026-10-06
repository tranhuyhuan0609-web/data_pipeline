from unittest.mock import MagicMock, AsyncMock, patch

import pytest

from src.application.application import Application


@pytest.mark.asyncio
async def test_startup_error_closes_pool_and_stops_reactor():
    pool = MagicMock()
    pool.open = AsyncMock()
    pool.close = AsyncMock()

    orchestrator = MagicMock()
    orchestrator.schedule = AsyncMock(
        side_effect=RuntimeError("schedule failed")
    )

    reactor = MagicMock()

    app = Application(
        orchestrator=orchestrator,
        reactor=reactor,
        pool=pool,
    )

    with patch("src.application.application.logger") as mock_logger:
        await app.startup()

    mock_logger.exception.assert_called_once_with(
        "Error starting application."
    )

    pool.open.assert_awaited_once_with()
    orchestrator.schedule.assert_awaited_once_with()
    pool.close.assert_awaited_once_with()
    reactor.stop.assert_called_once_with()