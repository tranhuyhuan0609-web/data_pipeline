from src.infrastructure.repositories.postgresql_config_repository import PostgresConfigRepository
import pytest
from unittest.mock import AsyncMock, MagicMock
@pytest.mark.parametrize("config", [
    {"site_id":"site_A"}
], indirect=True)
@pytest.mark.asyncio
async def test_update_config_success(config):
    pool = MagicMock()
    repo = PostgresConfigRepository(
        pool=pool,
        table_name="crawler_config",
    )

    cursor = AsyncMock()
    cursor.rowcount = 1

    write_cursor_mock = MagicMock()
    write_cursor_mock.__aenter__ = AsyncMock(return_value=cursor)
    write_cursor_mock.__aexit__ = AsyncMock(return_value=None)

    repo._write_cursor = MagicMock(return_value=write_cursor_mock)
    await repo.update_config(
        site_id="site_A",
        config=config,
    )
    repo._write_cursor.assert_called_once()
    cursor.execute.assert_awaited_once()