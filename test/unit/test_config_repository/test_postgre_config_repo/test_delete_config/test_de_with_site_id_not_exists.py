from src.infrastructure.repositories.postgresql_config_repository import PostgresConfigRepository
import pytest
from unittest.mock import AsyncMock, MagicMock
from src.application.exceptions.config_exception import ConfigNotFoundError
@pytest.mark.asyncio
async def test_delete_config_site_id_not_found():
    pool = MagicMock()
    repo = PostgresConfigRepository(
        pool=pool,
        table_name="crawler_config",
    )

    cursor = AsyncMock()
    cursor.rowcount = 0

    write_cursor = MagicMock()
    write_cursor.__aenter__ = AsyncMock(return_value=cursor)
    write_cursor.__aexit__ = AsyncMock(return_value=None)

    repo._write_cursor = MagicMock(return_value=write_cursor)

    with pytest.raises(ConfigNotFoundError):
        await repo.delete_config(site_id="site_A")

    repo._write_cursor.assert_called_once()
    cursor.execute.assert_awaited_once()