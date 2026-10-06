from src.infrastructure.repositories.postgresql_config_repository import PostgresConfigRepository
import pytest
from unittest.mock import AsyncMock, MagicMock
@pytest.mark.parametrize("config", [
    {"site_id":"site_A"}
],indirect=True)
@pytest.mark.asyncio
async def test_get_enabled_config_success(config):
    pool = MagicMock()
    repo = PostgresConfigRepository(
        pool=pool,
        table_name="crawler_config",
    )

    cursor = AsyncMock()
    cursor.fetchall.return_value = [config.model_dump()]

    read_cursor = MagicMock()
    read_cursor.__aenter__ = AsyncMock(return_value=cursor)
    read_cursor.__aexit__ = AsyncMock(return_value=None)

    repo._read_cursor = MagicMock(return_value=read_cursor)

    result = await repo.get_enabled_configs()

    assert result == [config]
    repo._read_cursor.assert_called_once()
    cursor.execute.assert_awaited_once()
    cursor.fetchall.assert_awaited_once()