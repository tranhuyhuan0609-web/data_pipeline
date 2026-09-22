

from urllib.parse import urlparse

from pydantic import BaseModel , Field, HttpUrl , model_validator
class Selectors(BaseModel):
    title: str = Field(...)
    author: str
    content: str = Field(...)
    category: str
    published_at: str
class Pagination(BaseModel):
    enabled: bool = False
    next_page: str | None = None
class CrawlerSettings(BaseModel):
    delay: float = Field(default=1.0, ge=0.0)
    randomize_delay: bool = True

    concurrent_requests: int = Field(default=1, ge=1)

    download_timeout: int = Field(default=30, ge=1)

    retry_enabled: bool = True
    max_retries: int = Field(default=3, ge=0)

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
    
    def is_allowes_domains_valid(self, domain: str) -> bool:
        for allowed_domain in self.allowed_domains:
            if domain == allowed_domain:
                return True
            if domain.endswith("." + allowed_domain):
                return True
        return False
    @model_validator(mode="after")
    def validate_domain(self):
        
        base_domain = self.base_url.host
        if not self.is_allowes_domains_valid(base_domain):
            raise ValueError(f"Base URL domain '{base_domain}' is not in allowed domains: {self.allowed_domains}")
        for start_url in self.start_urls:
            
            start_domain = start_url.host
            if self.is_allowes_domains_valid(start_domain) is True:
                if start_domain == base_domain or start_domain.endswith("." + base_domain):
                    continue
                raise ValueError(f"Start URL domain '{start_domain}' is not in allowed domains: {self.allowed_domains}")
            raise ValueError(f"Start URL domain '{start_domain}' is not in allowed domains: {self.allowed_domains}")
        return self