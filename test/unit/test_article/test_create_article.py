import pytest
from pydantic import HttpUrl, ValidationError
def test_create_article(article):
    assert article.url == HttpUrl('https://example.com/article1')
    assert article.url_hash == 'hash1'
    assert article.title == 'Test Article'
    assert article.source == 'test_site'
    assert article.author == 'John Doe'
    assert article.content == 'This is test content.'
    assert article.category == 'Test Category'
    assert article.published_at is None
    assert article.crawled_at.isoformat() == '2026-10-01T09:15:30.123456+00:00'
    