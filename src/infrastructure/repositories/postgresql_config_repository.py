from contextlib import asynccontextmanager

from psycopg import sql
from psycopg.errors import UniqueViolation
from psycopg.types.json import Jsonb

from src.application.exceptions.config_exception import (
    ConfigAlreadyExistsError,
    ConfigNotFoundError,
)
from src.application.interfaces.config_repository import ConfigRepository
from src.domain.entities.crawler_config import CrawlerConfig


class PostgresConfigRepository(ConfigRepository):
    def __init__(
        self,
        pool,
        table_name: str,
        query_timeout: float = 5.0,
    ):
        if pool is None:
            raise ValueError("Pool cannot be None.")

        if not isinstance(table_name, str) or not table_name.strip():
            raise ValueError("Table name must be a non-empty string.")

        if (
            isinstance(query_timeout, bool)
            or not isinstance(query_timeout, (int, float))
            or query_timeout <= 0
        ):
            raise ValueError("Query timeout must be a positive number.")

        self.pool = pool
        self.table_name = table_name.strip()
        self.query_timeout = float(query_timeout)

    def _table(self) -> sql.Identifier:
        return sql.Identifier(self.table_name)

    async def _set_statement_timeout(self, conn) -> None:
        timeout_ms = int(self.query_timeout * 1000)

        await conn.execute(
            "SELECT set_config('statement_timeout', %s, true)",
            [str(timeout_ms)],
        )

    @asynccontextmanager
    async def _read_cursor(self):
        async with self.pool.connection() as conn:
            async with conn.transaction():
                await self._set_statement_timeout(conn)

                async with conn.cursor() as cur:
                    yield cur

    @asynccontextmanager
    async def _write_cursor(self):
        async with self.pool.connection() as conn:
            async with conn.transaction():
                await self._set_statement_timeout(conn)

                async with conn.cursor() as cur:
                    yield cur

    @staticmethod
    def _row_to_config(row) -> CrawlerConfig:
        return CrawlerConfig.model_validate(row)

    @staticmethod
    def _config_values(config: CrawlerConfig) -> tuple:
        return (
            config.site_id,
            config.name,
            config.enabled,
            str(config.base_url),
            [str(url) for url in config.start_urls],
            config.allowed_domains,
            Jsonb(config.selectors.model_dump(mode="json")),
            Jsonb(config.pagination.model_dump(mode="json")),
            Jsonb(config.crawler_settings.model_dump(mode="json")),
        )

    async def get_config(self, site_id: str) -> CrawlerConfig:
        query = sql.SQL(
            """
            SELECT
                site_id,
                name,
                enabled,
                base_url,
                start_urls,
                allowed_domains,
                selectors,
                pagination,
                crawler_settings
            FROM {}
            WHERE site_id = %s
            """
        ).format(self._table())

        async with self._read_cursor() as cur:
            await cur.execute(query, [site_id])
            row = await cur.fetchone()

        if row is None:
            raise ConfigNotFoundError(
                f"Config with site_id '{site_id}' not found."
            )

        return self._row_to_config(row)

    async def get_enabled_configs(self) -> list[CrawlerConfig]:
        query = sql.SQL(
            """
            SELECT
                site_id,
                name,
                enabled,
                base_url,
                start_urls,
                allowed_domains,
                selectors,
                pagination,
                crawler_settings
            FROM {}
            WHERE enabled = TRUE
            """
        ).format(self._table())

        async with self._read_cursor() as cur:
            await cur.execute(query)
            rows = await cur.fetchall()

        return [self._row_to_config(row) for row in rows]

    async def create_config(self, config: CrawlerConfig) -> None:
        query = sql.SQL(
            """
            INSERT INTO {} (
                site_id,
                name,
                enabled,
                base_url,
                start_urls,
                allowed_domains,
                selectors,
                pagination,
                crawler_settings
            )
            VALUES (
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s
            )
            """
        ).format(self._table())

        try:
            async with self._write_cursor() as cur:
                await cur.execute(
                    query,
                    self._config_values(config),
                )

        except UniqueViolation as exc:
            raise ConfigAlreadyExistsError(
                f"Config with site_id '{config.site_id}' already exists."
            ) from exc

    async def update_config(
        self,
        site_id: str,
        config: CrawlerConfig,
    ) -> None:
        if config.site_id != site_id:
            raise ValueError(
                "Site ID in the config does not match "
                "the provided site_id."
            )

        query = sql.SQL(
            """
            UPDATE {}
            SET
                name = %s,
                enabled = %s,
                base_url = %s,
                start_urls = %s,
                allowed_domains = %s,
                selectors = %s,
                pagination = %s,
                crawler_settings = %s
            WHERE site_id = %s
            """
        ).format(self._table())

        values = (
            self._config_values(config)
            + (site_id,)
        )

        async with self._write_cursor() as cur:
            await cur.execute(query, values)

            if cur.rowcount == 0:
                raise ConfigNotFoundError(
                    f"Config with site_id '{site_id}' not found."
                )

    async def delete_config(self, site_id: str) -> None:
        query = sql.SQL(
            """
            DELETE FROM {}
            WHERE site_id = %s
            """
        ).format(self._table())

        async with self._write_cursor() as cur:
            await cur.execute(query, [site_id])

            if cur.rowcount == 0:
                raise ConfigNotFoundError(
                    f"Config with site_id '{site_id}' not found."
                )