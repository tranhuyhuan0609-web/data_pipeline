from pydantic import ValidationError
import pytest

from src.config.settings import load_settings
def test_settings_with_not_env(monkeypatch):
    monkeypatch.setenv("ENV", "not_env")
    with pytest.raises(ValidationError):
        load_settings()