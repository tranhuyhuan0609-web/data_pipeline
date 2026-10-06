from src.infrastructure.repositories.postgresql_config_repository import PostgresConfigRepository
import pytest
from unittest.mock import AsyncMock, MagicMock
@pytest.mark.parametrize("config", [
    {"site_id":"site_A"}
], indirect=True)
@pytest.mark.asyncio
async def test_update_config_site_id_not_equals(config):
    pool = MagicMock()
    repo = PostgresConfigRepository(
        pool=pool,
        table_name="crawler_config",
    )

   
    with pytest.raises(ValueError):
        await repo.update_config(
            site_id="site_B",
            config=config,
        )