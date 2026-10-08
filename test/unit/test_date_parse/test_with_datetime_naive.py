from src.domain.services.date_parse import normalize_published_at
from datetime import datetime, timezone
def test_parse_date_with_datetime_naive():
    naive_datetime = datetime(2023, 1, 1, 12, 0, 0)   
    expected_datetime = naive_datetime.replace(tzinfo=timezone.utc)  
    assert normalize_published_at(naive_datetime) == expected_datetime