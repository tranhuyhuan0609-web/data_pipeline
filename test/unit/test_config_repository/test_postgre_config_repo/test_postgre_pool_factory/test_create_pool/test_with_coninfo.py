from unittest.mock import patch
from src.infrastructure.postgres_db.pool import PostgresPoolFactory



def test_create_postgres_pool_with_connection_info():
    factory = PostgresPoolFactory(
        host="localhost",
        port=5433,
        user="postgres",
        password="password",
        dbname="test_db",
        min_size=2,
        max_size=5,
    )

    with patch(
        "src.infrastructure.postgres_db.pool.AsyncConnectionPool"
    ) as mock_pool:
        pool = factory.create_pool()

        mock_pool.assert_called_once()

        _, kwargs = mock_pool.call_args
        assert kwargs["conninfo"] == (
            "host=localhost "
            "port=5433 "
            "user=postgres "
            "password=password "
            "dbname=test_db"
        )
