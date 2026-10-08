from src.domain.services.date_parse import normalize_published_at   
from datetime import datetime, timezone
def test_parse_date_with_int_published_time():
    time = 1696742400  

    assert normalize_published_at(time) == None