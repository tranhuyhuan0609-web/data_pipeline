import pytest
from scrapy.http import HtmlResponse, Request
from src.infrastructure.crawler.scrapy.generic_spider import GenericSpider
@pytest.mark.parametrize("config", [{
    "start_urls": ["https://example.com/test-article"],
    "title": "h1.title::text",
    "content": "div.content::text",
    "next_page": "a.next::attr(href)",
    "max_pages": 3
}], indirect=True)
def test_spider_with_no_content(config,
                              caplog,
                              ):
    config = config.model_copy(deep=True)
    spider = GenericSpider(crawler_config=config)

    html_content = """
        <html>
            <body>
                <h1 class="title">Test Title</h1>
                <div class="contents">This is test content.</div>
                <a class="next" href="/page2">Next</a>
            </body>
        </html>
    """
    request = Request(url="https://example.com/test-article")
    response = HtmlResponse(
        url="https://example.com/test-article",
        body=html_content,
        encoding="utf-8",
        request=request,
    )

    results = list(spider.parse(response))
    assert len(results) == 1
    assert any(
    "Missing title or content" in record.message
    and "https://example.com/test-article" in record.message
    for record in caplog.records
)
    assert isinstance(results[0], Request)