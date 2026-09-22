from datetime import datetime
from pydantic import BaseModel, HttpUrl, Field
class Article(BaseModel):
    url: HttpUrl
    url_hash: str
    title: str
    author: str | None = None
    content: str
    category: str | None = None
    source: str
    published_at: datetime | None = None
    crawled_at: datetime
class ArticleEnrichment(BaseModel):
    summary: str | None = None
    keywords : list[str] = Field(default_factory=list)
class ProcessingMetaData(BaseModel):
    version: str
    processed_at: datetime