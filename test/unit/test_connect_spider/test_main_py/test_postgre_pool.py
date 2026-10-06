from unittest.mock import MagicMock, patch
import src.main as main


def test_main_passes_postgres_settings_to_pool_factory():
    settings = MagicMock()
    settings.POSTGRES_HOST = "localhost"
    settings.POSTGRES_PORT = 5433
    settings.POSTGRES_USER = "postgres"
    settings.POSTGRES_PASSWORD = "password"
    settings.POSTGRES_DB = "web_pipeline_test"

    pool = MagicMock()
    pool_factory = MagicMock()
    pool_factory.create_pool.return_value = pool

    repository = MagicMock()
    crawler_factory = MagicMock()
    crawler_runner = MagicMock()
    orchestrator = MagicMock()
    application = MagicMock()

    with (
        patch.object(main, "load_settings", return_value=settings),
        patch.object(
            main,
            "PostgresPoolFactory",
            return_value=pool_factory,
        ) as mock_pool_factory,
        patch.object(
            main,
            "PostgresConfigRepository",
            return_value=repository,
        ),
        patch.object(
            main,
            "CrawlerFactory",
            return_value=crawler_factory,
        ),
        patch.object(
            main,
            "CrawlerRunner",
            return_value=crawler_runner,
        ),
        patch.object(
            main,
            "CrawlerOrchestrator",
            return_value=orchestrator,
        ),
        patch.object(
            main,
            "Application",
            return_value=application,
        ),
    ):
        main.main()

    mock_pool_factory.assert_called_once_with(
        host="localhost",
        port=5433,
        user="postgres",
        password="password",
        dbname="web_pipeline_test",
    )