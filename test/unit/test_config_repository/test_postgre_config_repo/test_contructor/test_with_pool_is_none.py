import pytest
from src.infrastructure.repositories.postgresql_config_repository import  PostgresConfigRepository
def test_pool_is_none():
    with pytest.raises(ValueError, match="Pool cannot be None."):
        PostgresConfigRepository(pool=None,
            table_name="test_table",
            query_timeout=5.0
        )