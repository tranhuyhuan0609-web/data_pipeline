from src.domain.services.date_parse import normalize_published_at
def test_parse_date_with_white_space():
    assert normalize_published_at("   ") is None