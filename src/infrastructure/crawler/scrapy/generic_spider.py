import scrapy
from datetime import datetime, timezone
from src.domain.services.url_hash import create_url_hash
from src.domain.entities.article import Article
from src.domain.services.date_parse import normalize_published_at
pages_crawled = 0
class GenericSpider(scrapy.Spider):
    name = "generic_spider"
    allowed_domains = []
    start_urls = []
    def __init__(self, crawler_config, *args, **kwargs):
        super(GenericSpider, self).__init__(*args, **kwargs)
        self.crawler_config = crawler_config
        self.allowed_domains = crawler_config.allowed_domains
        self.start_urls = [str(url) for url in crawler_config.start_urls]
        self.pages_crawled = 0
        self.pages_scheduled = len(self.start_urls)
    def extract_content(self, response)-> str:
        content_list = response.css(self.crawler_config.selectors.content).getall()
        content = " ".join(content.strip() for content in content_list if content.strip())
        return content
    def extract_title(self, response) -> str:
        title = response.css(self.crawler_config.selectors.title).get()
        if title is None or title.strip() == "":
            return ""
        return title.strip()
    def extract_author(self, response) -> str | None:
        if self.crawler_config.selectors.author:
            author = response.css(self.crawler_config.selectors.author).get()
            if author is not None:
                author = author.strip()
                if author == "":
                    return None
                return author
            return None
        return None
    def extract_category(self, response) -> str | None:
        if self.crawler_config.selectors.category:
            category = response.css(self.crawler_config.selectors.category).get()
            if category is not None:
                category = category.strip()
                if category == "":
                    return None
                return category
        return None
    
    def extract_published_at(self, response) -> datetime | None:
        published_at_str = response.css(self.crawler_config.selectors.published_at).get() if self.crawler_config.selectors.published_at else None
        return normalize_published_at(published_at_str)
    def parse(self, response):
        self.pages_crawled += 1
        title = self.extract_title(response)
        content = self.extract_content(response)
        author = self.extract_author(response) 
        category = self.extract_category(response)
        published_at = self.extract_published_at(response)
        url = response.url
        crawled_at = datetime.now(timezone.utc)
        source = self.crawler_config.site_id
        url_hash = create_url_hash(url)
        article_data = {
            "url": url,
            "url_hash": url_hash,
            "title": title,
            "source": source,
            "author": author,
            "content": content,
            "category": category,
            "published_at": published_at,
            "crawled_at": crawled_at, }
        if not title or not content:
            self.logger.warning(f"Missing title or content for URL: {url}. Skipping article.")
        else: 
            article = Article(**article_data)
            yield article.model_dump(mode="json")
        max_pages = self.crawler_config.pagination.max_pages
        if (
            self.crawler_config.pagination.enabled
            and (
                max_pages is None or
                self.pages_scheduled < max_pages
            )
        ):
            next_page = response.css(self.crawler_config.pagination.next_page).get() if self.crawler_config.pagination.next_page else None
            if next_page:
                next_request = response.follow(
                    next_page,
                    callback=self.parse
                )
                self.pages_scheduled += 1
                yield next_request
