from src.domain.entities.crawler_config import CrawlerSettings
import pytest 
from pydantic import ValidationError  
def test_delay_success():
    valid_settings = CrawlerSettings(
        delay = 0.001,
    )
    assert valid_settings.delay == 0.001
def test_delay_invalid():
    with pytest.raises(ValidationError):
        CrawlerSettings(
            delay = 0,
        )
def test_delay_invalid_negative():
    with pytest.raises(ValidationError):
        CrawlerSettings(
            delay = -1.0,
        )
        
