import pytest
from unittest.mock import MagicMock, AsyncMock

from src.application.application import Application


@pytest.mark.asyncio
async def test_startup_success():
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

    await app.startup()

    pool.open.assert_awaited_once_with()
    orchestrator.schedule.assert_awaited_once_with()

    pool.close.assert_not_awaited()
    reactor.stop.assert_not_called()