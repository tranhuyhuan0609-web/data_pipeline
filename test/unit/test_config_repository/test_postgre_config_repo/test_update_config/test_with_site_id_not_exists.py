from unittest.mock import AsyncMock, MagicMock
from src.infrastructure.repositories.postgresql_config_repository import PostgresConfigRepository
import pytest
from src.application.exceptions.config_exception import ConfigNotFoundError
@pytest.mark.parametrize("config", [
    {"site_id":"site_A"}
],indirect=True)
@pytest.mark.asyncio
async def test_update_config_site_id_not_found(config):
  
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
        await repo.update_config(
            site_id="site_A",
            config=config,
        )