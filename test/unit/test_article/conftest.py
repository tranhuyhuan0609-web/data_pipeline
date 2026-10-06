import pytest

from src.domain.entities.article import Article

@pytest.fixture
def article(request):
    override = getattr(request, 'param', {})
    url = override.get('url', 'https://example.com/article1')
    url_hash = override.get('url_hash', 'hash1')
    title = override.get('title', 'Test Article')
    source = override.get('source', 'test_site')
    author = override.get('author', 'John Doe')
    content = override.get('content', 'This is test content.')
    category = override.get('category', 'Test Category')
    published_at = override.get('published_at', None)
    crawled_at = override.get('crawled_at', '2026-10-01T09:15:30.123456+00:00')
    return Article(
        url = url,
        url_hash = url_hash,
        title = title,
        source = source,
        author = author,
        content = content,
        category = category,
        published_at = published_at,
        crawled_at = crawled_at
    )