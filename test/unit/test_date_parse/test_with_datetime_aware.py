from src.domain.services.date_parse import normalize_published_at
from datetime import datetime, timezone, timedelta
def test_parse_date_with_aware_datetime_non_utc():

    time = datetime(
        2026, 10, 7, 10, 0, 0,
        tzinfo=timezone(timedelta(hours=7))
    )

    expected = datetime(
        2026, 10, 7, 3, 0, 0,
        tzinfo=timezone.utc
    )

    assert normalize_published_at(time) == expected