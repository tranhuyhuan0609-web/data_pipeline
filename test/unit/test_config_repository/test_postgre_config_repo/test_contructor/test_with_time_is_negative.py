from src.infrastructure.repositories.postgresql_config_repository import  PostgresConfigRepository
import pytest
def test_time_is_negative():
    with pytest.raises(ValueError, match="Query timeout must be a positive number."):
        PostgresConfigRepository(pool="dummy_pool",
            table_name="test_table",
            query_timeout=-5.0
        )