from unittest.mock import MagicMock, AsyncMock

import pytest

from src.application.application import Application


@pytest.mark.asyncio
async def test_shutdown_success():
    pool = MagicMock()
    pool.open = AsyncMock()
    pool.close = AsyncMock()

    orchestrator = MagicMock()
    orchestrator.schedule = AsyncMock()
    reactor = MagicMock()

    app = Application(
        orchestrator=orchestrator,
        reactor=reactor,
        pool=pool,
    )
    # await app.startup()
    await app._shutdown()
    pool.close.assert_awaited_once_with()
    reactor.stop.assert_called_once_with()