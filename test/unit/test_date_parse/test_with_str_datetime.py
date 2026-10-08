from src.domain.services.date_parse import normalize_published_at
from datetime import datetime, timezone
def test_parse_date_with_string_datetime():

    time = "2026-10-07 10:00:00+07:00"

    expected = datetime(
        2026, 10, 7, 3, 0, 0,
        tzinfo=timezone.utc
    )

    assert normalize_published_at(time) == expected