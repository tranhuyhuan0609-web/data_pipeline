
import pytest
from unittest.mock import patch

from pydantic import ValidationError
from pydantic_core import InitErrorDetails, PydanticCustomError
from scrapy.http import HtmlResponse, Request

from src.infrastructure.crawler.scrapy.generic_spider import GenericSpider


def raise_article_validation_error(*args, **kwargs):
    errors = [
        InitErrorDetails(
            type=PydanticCustomError(
                "invalid_article",
                "Invalid article schema",
            ),
            loc=("title",),
            input="invalid",
        )
    ]

    raise ValidationError.from_exception_data(
        title="Article",
        line_errors=errors,
    )


@pytest.mark.parametrize(
    "config",
    [{
        "title": "h1.title::text",
        "content": "div.content::text",
        "next_page": "a.next::attr(href)",
        "max_pages": 3,
    }],
    indirect=True,
)
def test_invalid_article_schema_skip_log_and_continue_pagination(
    config,
    caplog,
):
    config = config.model_copy(deep=True)

    spider = GenericSpider(crawler_config=config)

    html_content = """
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
        body=html_content,
        encoding="utf-8",
        request=Request(url="https://example.com/page1"),
    )

    with patch(
        "src.infrastructure.crawler.scrapy.generic_spider.Article",
        side_effect=raise_article_validation_error,
    ):
        results = list(spider.parse(response))


    articles = [
        result
        for result in results
        if not isinstance(result, Request)
    ]

    assert articles == []


    requests = [
        result
        for result in results
        if isinstance(result, Request)
    ]

    assert len(requests) == 1
    assert requests[0].url == "https://example.com/page2"


    assert any(
        "page1" in record.message
        for record in caplog.records
    )
