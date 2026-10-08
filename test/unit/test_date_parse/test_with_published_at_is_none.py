from src.domain.services.date_parse import normalize_published_at 
import pytest
def test_parse_date_with_none():
    assert normalize_published_at(None) is None