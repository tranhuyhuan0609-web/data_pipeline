from src.infrastructure.crawler.scrapy.generic_spider import GenericSpider
import pytest
from scrapy.http import HtmlResponse, Request
from scrapy.dupefilters import RFPDupeFilter
@pytest.mark.parametrize("config",[{
    "title": "h1.title::text",
    "content": "div.content::text",
    "next_page": "a.next::attr(href)",
    "max_pages": None,
}], indirect=True)
def test_duplicate_without_max_pages(tmp_path,config):
    dupefilter = RFPDupeFilter(path=str(tmp_path))
    spider = GenericSpider(crawler_config=config, dupefilter=dupefilter)
    dupefilter.open()
    html_page_1 = """
        <html>
            <body>
                <h1 class="title">Test Article</h1>
                <div class="content">This is test content.</div>
                <a class="next" href="/page2">Next</a>
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
    assert spider.extract_title(response_page_1) == "Test Article"
    assert dupefilter.request_seen(request_page_1) is False
    results = list(spider.parse(response_page_1))
    request_to_2 = [result for result in results if isinstance(result, Request)][0]
    assert dupefilter.request_seen(request_to_2) is False
    html_page_2 = """
    <html>
        <body>
            <h1 class="title">Test Article</h1>
            <div class="content">This is test content.</div>
            <a class="next" href="/page1">Next</a>
        </body>
    </html>
    """
   
    response_page_2 = HtmlResponse(
        url="https://example.com/page2",
        body=html_page_2,
        encoding="utf-8",
        request=request_to_2,
    )
    results_page_2 = list(spider.parse(response_page_2))
    request_to_1 = [result for result in results_page_2 if isinstance(result, Request)][0]
    assert spider.extract_title(response_page_2) == "Test Article"
    assert dupefilter.request_seen(request_to_1) is True
    dupefilter.close("finished")