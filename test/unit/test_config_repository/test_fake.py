# from src.infrastructure.repositories.fake_config_repository import FakeConfigRepository
# from src.domain.entities.crawler_config import CrawlerConfig
# import pytest
# from src.domain.entities.crawler_config import Selectors, Pagination, CrawlerSettings
# @pytest.fixture
# def repo():
#     return FakeConfigRepository()
# @pytest.fixture
# def config():
#     return CrawlerConfig(
#         site_id="test_site",
#         name="Test Site",
#         enabled=True,
#         base_url="https://example.com",
#         start_urls=["https://example.com/start"],
#         allowed_domains=["example.com"],
#         selectors=Selectors(
#             title="h1.title",
#             content="div.content"
#         ),
#         pagination=Pagination(
#             enabled=True,
#             next_page="a.next",
#             max_pages=5
#         ),
#         crawler_settings=CrawlerSettings(
#             delay=1.0,
#             randomize_delay=True,
#             concurrent_requests=2,
#             download_timeout=30,
#             retry_enabled=True,
#             max_retries=3
#         )
#     )
# def test_create_and_get_config(repo, config):
#     repo.create_config(config)
#     retrieved_config = repo.get_config(config.site_id)
#     assert retrieved_config == config
# def test_get_enabled_configs(repo, config):
#     repo.create_config(config)
#     enabled_configs = repo.get_enabled_configs()
#     assert len(enabled_configs) == 1
#     assert enabled_configs[0] == config
# def test_update_config(repo, config):
#     repo.create_config(config)
#     updated_config = CrawlerConfig(
#         site_id="test_site_updated",
#         name="Updated Test Site",
#         enabled=False,
#         base_url="https://example.com",
#         start_urls=["https://example.com/start"],
#         allowed_domains=["example.com"],
#         selectors=Selectors(
#             title="h1.title",
#             content="div.content"
#         ),
#         pagination=Pagination(
#             enabled=True,
#             next_page="a.next",
#             max_pages=5
#         ),
#         crawler_settings=CrawlerSettings(
#             delay=1.0,
#             randomize_delay=True,
#             concurrent_requests=2,
#             download_timeout=30,
#             retry_enabled=True,
#             max_retries=3
#         )
#     )
#     with pytest.raises(ValueError):
#         repo.update_config(config.site_id, updated_config)