from src.config.settings import load_settings


def test_load_settings_test_environment(monkeypatch):
    monkeypatch.setenv("ENV", "test")

    settings = load_settings()

    assert settings.POSTGRES_DB == "web_pipeline_test"