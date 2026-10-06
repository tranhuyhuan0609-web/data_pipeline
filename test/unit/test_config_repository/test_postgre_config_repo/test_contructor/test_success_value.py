from src.infrastructure.repositories.postgresql_config_repository import  PostgresConfigRepository
import pytest
def test_success_value():
    repo = PostgresConfigRepository(pool="dummy_pool",
        table_name="test_table",
        query_timeout=5.0
    )
    assert isinstance(repo, PostgresConfigRepository)