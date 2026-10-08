from datetime import datetime, timezone, tzinfo

from dateutil import parser


def normalize_published_at(
    value: str | datetime | None,
    source_timezone: tzinfo = timezone.utc,
) -> datetime | None:

    if value is None:
        return None

    try:
        if isinstance(value, str):
            value = value.strip()

            if not value:
                return None

            parsed_date = parser.parse(
                value,
                fuzzy=False,
            )

        elif isinstance(value, datetime):
            parsed_date = value

        else:
            return None

        if parsed_date.tzinfo is None:
            parsed_date = parsed_date.replace(
                tzinfo=source_timezone
            )

        return parsed_date.astimezone(timezone.utc)

    except (ValueError, OverflowError, TypeError):
        return None