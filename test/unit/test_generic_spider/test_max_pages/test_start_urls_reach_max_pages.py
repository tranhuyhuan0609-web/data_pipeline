from src.infrastructure.crawler.scrapy.generic_spider import GenericSpider
import pytest
from scrapy.http import HtmlResponse, Request
@pytest.mark.parametrize("config",[{
    "title": "h1.title::text",
    "content": "div.content::text",
    "next_page": "a.next::attr(href)",
    "start_urls": ["https://example.com/page1",
                   "https://example.com/page2",
                   "https://example.com/page3"],
    
}] , indirect=True)
def test_spider_start_urls_reach_max_pages(config):
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
    response = HtmlResponse(
        url="https://example.com/page1",
        body=html_page_1,
        encoding="utf-8",
        request=Request(url="https://example.com/page1"),
    )
    results = list(spider.parse(response))
    result = [result for result in results if isinstance(result, Request)]
    assert len(result) == 0
    assert len(results) == 1
    assert spider.extract_title(response) == "Test Title 1"
    assert results[0]["title"] == "Test Title 1"