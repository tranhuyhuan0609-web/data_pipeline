from src.infrastructure.repositories.postgresql_config_repository import  PostgresConfigRepository
import pytest
def tes_table_name_is_not_str():
    with pytest.raises(ValueError, match="Table name must be a non-empty string."):
        PostgresConfigRepository(pool="dummy_pool",
            table_name=123,
            query_timeout=5.0
        )