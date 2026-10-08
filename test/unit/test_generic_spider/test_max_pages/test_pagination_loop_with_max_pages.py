
from src.infrastructure.crawler.scrapy.generic_spider import GenericSpider
import pytest
from scrapy.http import HtmlResponse, Request
@pytest.mark.parametrize("config",[{
    "title": "h1.title::text",
    "content": "div.content::text",
    "next_page": "a.next::attr(href)",
    "max_pages": 3
}], indirect=True)
def test_spider_pagination_loop_with_max_pages(config):
    config = config.model_copy(deep=True)
    spider = GenericSpider(crawler_config = config)
    html_page_1 = """
        <html>
            <body>
                <h1 class="title">Test Title 1</h1>
                <div class="content">This is test content 1.</div>
                <a class="next" href="/page2">Next</a>
            </body>
        </html>
    """
    html_page_2 = """
        <html>
            <body>
                <h1 class="title">Test Article 2</h1>
                <div class="content">This is content of page 2.</div>
                <a class="next" href="/page1">Next</a>
            </body>
        </html>
    """
    request_page_1 = Request(url="https://example.com/page1")
    response_page_1 = HtmlResponse(
        url="https://example.com/page1",
        body=html_page_1,
        encoding="utf-8",
        request=request_page_1,
    )
    results_page_1 = list(spider.parse(response_page_1))
    assert len(results_page_1) == 2
    assert isinstance(results_page_1[0], dict)
    assert isinstance(results_page_1[1], Request)

    request_page_2 = Request(url="https://example.com/page2")
    response_page_2 = HtmlResponse(
        url="https://example.com/page2",
        body=html_page_2,
        encoding="utf-8",
        request=request_page_2,
    )
    results_page_2 = list(spider.parse(response_page_2))
    assert len(results_page_2) == 1
    assert isinstance(results_page_2[0], dict)
   
      