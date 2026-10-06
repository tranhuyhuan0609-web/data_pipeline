
from src.infrastructure.crawler.scrapy.generic_spider import GenericSpider
import pytest
from scrapy.http import HtmlResponse, Request
@pytest.mark.parametrize("config",[
    {
        "title": "h1.title::text",
        "content": "div.content::text",
        "max_pages": 1,
        "next_page": "a.next::attr(href)"

    }
], indirect=True)
def test_spider_max_page_limit(config):
    config = config.model_copy(deep=True)
    spider = GenericSpider(crawler_config = config)
    html_page = """
        <html>
            <body>
                <h1 class="title">Test Title</h1>
                <div class="content">This is test content.</div>
                <a class="next" href="/page2">Next</a>
            </body>
        </html>
    """
    response = HtmlResponse(
        url="https://example.com/page1",
        body=html_page,
        encoding="utf-8",
        request=Request(url="https://example.com/page1"),
    )
    results = list(spider.parse(response))
    result = [result for result in results if isinstance(result, Request)  ]
    assert len(results) == 1
    assert isinstance(results[0], dict)
    assert results[0]["title"] == "Test Title"
    assert len(result) == 0
    assert spider.pages_scheduled == 1