from unittest.mock import MagicMock, patch

import src.main as main


def test_main_wires_dependencies_correctly():
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
        ),
        patch.object(
            main,
            "PostgresConfigRepository",
            return_value=repository,
        ) as mock_repository,
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
        ) as mock_orchestrator,
        patch.object(
            main,
            "Application",
            return_value=application,
        ) as mock_application,
    ):
        main.main()

    mock_repository.assert_called_once_with(
        pool=pool,
        table_name="crawler_config",
    )

    mock_orchestrator.assert_called_once_with(
        repository=repository,
        crawler_factory=crawler_factory,
        crawler_runner=crawler_runner,
    )

    mock_application.assert_called_once_with(
        orchestrator=orchestrator,
        reactor=main.reactor,
        pool=pool,
    )

    application.run.assert_called_once_with()