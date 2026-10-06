
from src.infrastructure.crawler.scrapy.generic_spider import GenericSpider
import pytest
from scrapy.http import HtmlResponse, Request
@pytest.mark.parametrize("config",[{
    "title": "h1.title::text",
    "content": "div.content::text",
    "start_urls": ["https://example.com/page1", "https://example.com/page2"],
    "next_page": "a.next::attr(href)"
}], indirect=True)
def test_pages_scheduled_limit(config):
    config = config.model_copy(deep=True)
    spider = GenericSpider(crawler_config = config)
    assert spider.pages_scheduled == 2
    html_page_1 = """
        <html>
            <body>
                <h1 class="title">Test Title 1</h1>
                <div class="content">This is test content 1.</div>
                <a class="next" href="/page2">Next</a>
            </body>
        </html>
    """
    response_page_1 = HtmlResponse(
        url="https://example.com/page1",
        body=html_page_1,
        encoding="utf-8",
        request=Request(url="https://example.com/page1"),
    )
    results = list(spider.parse(response_page_1))
    requested = [result for result in results if isinstance(result, Request)]
    assert spider.pages_scheduled == 3
    assert len(requested) == 1
    assert requested[0].url == "https://example.com/page2"
    html_page_2 = """
        <html>
            <body>
                <h1 class="title">Test Title 2</h1>
                <div class="content">This is test content 2.</div>
                <a class="next" href="/page3">Next</a>
            </body>
        </html>
    """
    response_page_2 = HtmlResponse(
        url="https://example.com/page2",
        body=html_page_2,
        encoding="utf-8",
        request=Request(url="https://example.com/page2"),
    )
    results = list(spider.parse(response_page_2))
    assert spider.pages_scheduled == 3
    requested = [result for result in results if isinstance(result, Request)]
    assert len(requested) == 0
    assert len(results) == 1
    assert not any(isinstance(result, Request) for result in results)