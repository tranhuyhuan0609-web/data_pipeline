from datetime import datetime, timezone
from dateutil import parser


def normalize_published_at(
    value: str | datetime | None,
    source_timezone=timezone.utc,
    dayfirst=True,
) -> datetime | None:

    if value is None:
        return None

    try:
        # Trường hợp đầu vào đã là datetime
        if isinstance(value, datetime):
            parsed_date = value

        # Trường hợp đầu vào là chuỗi
        elif isinstance(value, str):
            value = value.strip()

            if not value:
                return None

            parsed_date = parser.parse(
                value,
                dayfirst=dayfirst,
                fuzzy=False,
            )

        else:
            return None

        # Nếu ngày không có timezone,
        # gán timezone nguồn đã quy định.
        if parsed_date.tzinfo is None:
            parsed_date = parsed_date.replace(
                tzinfo=source_timezone
            )

        # Chuyển về UTC
        parsed_date = parsed_date.astimezone(timezone.utc)

        return parsed_date

    except (ValueError, OverflowError, TypeError):
        return None