from pathlib import Path

import pytest

from src.config import settings as settings_module


def test_load_settings_env_file_not_found(monkeypatch):
    monkeypatch.setenv("ENV", "test")

    fake_config_dir = Path("/path/that/does/not/exist")
    monkeypatch.setattr(
        settings_module,
        "CONFIG_DIR",
        fake_config_dir,
    )

    with pytest.raises(FileNotFoundError):
        settings_module.load_settings()