from src.domain.entities.article import Article
from pydantic import HttpUrl, ValidationError
from datetime import datetime, timezone
import pytest
def test_miss_title():
    with pytest.raises(ValidationError):
        Article(
            url = HttpUrl('https://example.com/article1'),
            url_hash = 'hash1',
            title = None,  
            source = 'test_site',
            author = 'John Doe',
            content = 'This is test content.',
            category = 'Test Category',
            published_at = None,
            crawled_at = datetime.now(timezone.utc)
        )
