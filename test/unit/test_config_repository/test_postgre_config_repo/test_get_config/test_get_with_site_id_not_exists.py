from src.infrastructure.repositories.postgresql_config_repository import PostgresConfigRepository
import pytest
from unittest.mock import AsyncMock, MagicMock
from src.application.exceptions.config_exception import ConfigNotFoundError
@pytest.mark.asyncio
async def test_get_config_site_id_not_exists():
    pool = MagicMock()
    repo = PostgresConfigRepository(
        pool=pool,
        table_name="crawler_config",
    )

    cursor = AsyncMock()
    cursor.fetchone.return_value = None

    read_cursor = MagicMock()
    read_cursor.__aenter__ = AsyncMock(return_value=cursor)
    read_cursor.__aexit__ = AsyncMock(return_value=None)

    repo._read_cursor = MagicMock(return_value=read_cursor)

    with pytest.raises(ConfigNotFoundError):
        await repo.get_config(
            site_id="site_A",
        )