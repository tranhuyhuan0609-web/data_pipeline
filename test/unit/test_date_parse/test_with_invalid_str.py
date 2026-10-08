from src.domain.services.date_parse import normalize_published_at
def test_parse_date_with_invalid_string():
    invalid_time = "invalid date string"
    assert normalize_published_at(invalid_time) is None