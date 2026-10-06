
from pydantic import BaseModel , Field, HttpUrl , model_validator
class Selectors(BaseModel):
    title: str = Field(...)
    author: str | None = None
    content: str = Field(...)
    category: str | None = None
    published_at: str | None = None
class Pagination(BaseModel):
    enabled: bool = False
    next_page: str | None = None
    max_pages: int | None = Field(default=100, ge=1)
    @model_validator(mode="after")
    def validate_pagination(self):
        if self.enabled and not self.next_page:
            raise ValueError("Pagination is enabled, but next_page selector is not provided.")
        elif not self.enabled and self.next_page:
            raise ValueError("Pagination is disabled, but next_page selector is provided.")
        return self
class CrawlerSettings(BaseModel):
    delay: float = Field(default=1.0, gt=0.0)
    randomize_delay: bool = True

    concurrent_requests: int = Field(default=1, ge=1, le=10)

    download_timeout: int = Field(default=30, ge=1, le=300)

    retry_enabled: bool = True
    max_retries: int = Field(default=3, ge=0)
   
    @model_validator(mode="after")
    def validate_retry_settings(self):
            if not self.retry_enabled and self.max_retries > 0:
                raise ValueError("Retry is disabled, but max_retries is greater than 0.")
            if self.retry_enabled and self.max_retries == 0:
                raise ValueError("Retry is enabled, but max_retries is 0.")
            return self
    
    

class CrawlerConfig(BaseModel):
    site_id: str = Field(...)
    name: str = Field(...)
    enabled: bool
    base_url: HttpUrl = Field(...)
    start_urls: list[HttpUrl] = Field(min_length=1)
    allowed_domains: list[str] = Field(min_length=1)
    selectors: Selectors
    pagination: Pagination
    crawler_settings: CrawlerSettings
    @model_validator(mode="after")
    def validation_start_urls(self):
        if self.pagination.max_pages is not None:
            if len(self.start_urls) > self.pagination.max_pages:
                raise ValueError(f"Number of start_urls ({len(self.start_urls)}) exceeds max_pages ({self.pagination.max_pages}).")
            return self
        return self

    
    def is_allowed_domains_valid(self, domain: str) -> bool:
        for allowed_domain in self.allowed_domains:
            if domain == allowed_domain:
                return True
            if domain.endswith("." + allowed_domain):
                return True
        return False
    @model_validator(mode="after")
    def validate_domain(self):
        
        base_domain = self.base_url.host
        if not self.is_allowed_domains_valid(base_domain):
            raise ValueError(f"Base URL domain '{base_domain}' is not in allowed domains: {self.allowed_domains}")
        for start_url in self.start_urls:
            
            start_domain = start_url.host
            if not self.is_allowed_domains_valid(start_domain):
                raise ValueError(f"Start URL domain '{start_domain}' is not in allowed domains: {self.allowed_domains}")
            if start_domain != base_domain and not start_domain.endswith("." + base_domain):
                raise ValueError(f"Start URL domain '{start_domain}' does not match base URL domain '{base_domain}'")
        return self