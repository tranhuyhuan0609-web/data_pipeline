from unittest.mock import MagicMock, AsyncMock, patch

import pytest

from src.application.application import Application


@pytest.mark.asyncio
async def test_shutdown_with_error():
    pool = MagicMock()
    pool.close = AsyncMock(
        side_effect=RuntimeError("close failed")
    )

    orchestrator = MagicMock()
    reactor = MagicMock()

    app = Application(
        orchestrator=orchestrator,
        reactor=reactor,
        pool=pool,
    )

    with patch("src.application.application.logger") as mock_logger:
        await app._shutdown()

    pool.close.assert_awaited_once_with()

    mock_logger.exception.assert_called_once_with(
        "Error closing PostgreSQL pool."
    )

    reactor.stop.assert_called_once_with()