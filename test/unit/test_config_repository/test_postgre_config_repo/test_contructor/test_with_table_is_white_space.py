from src.infrastructure.repositories.postgresql_config_repository import  PostgresConfigRepository
import pytest
def test_table_name_is_white_space():
    with pytest.raises(ValueError, match="Table name must be a non-empty string."):
        PostgresConfigRepository(pool="dummy_pool",
            table_name="   ",
            query_timeout=5.0
        )