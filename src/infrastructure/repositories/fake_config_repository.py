from typing import List

from src.application.interfaces.config_repository import ConfigRepository
from src.domain.entities.crawler_config import CrawlerConfig
from src.application.exceptions.config_exception import ConfigNotFoundError, ConfigAlreadyExistsError
class FakeConfigRepository(ConfigRepository):
    def __init__(self):
        self.config = {}
    async def get_config(self, site_id: str) -> CrawlerConfig:
        if site_id not in self.config:
            raise ConfigNotFoundError(f"Config with site_id '{site_id}' not found.")
        return self.config[site_id]
    async def get_enabled_configs(self) -> List[CrawlerConfig]:
        if not self.config:
            return []
        return [config for config in self.config.values() if config.enabled == True]
    async def create_config(self, config: CrawlerConfig) -> None:
        if config.site_id in self.config:
            raise ConfigAlreadyExistsError(f"Config with site_id '{config.site_id}' already exists.")
        self.config[config.site_id] = config
    async def update_config(self, site_id: str, config: CrawlerConfig) -> None:
        if config.site_id == site_id:
            if site_id not in self.config:
                raise ConfigNotFoundError(f"Config with site_id '{site_id}' not found.")
            self.config[site_id] = config
        else: 
            raise ValueError("Site ID in the config does not match the provided site_id.")
    async def delete_config(self, site_id: str) -> None:
        if site_id not in self.config:
            raise ConfigNotFoundError(f"Config with site_id '{site_id}' not found.")
        del self.config[site_id]

        