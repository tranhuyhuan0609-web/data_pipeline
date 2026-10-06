import logging

from twisted.internet import defer

logger = logging.getLogger(__name__)


class Application:
    def __init__(self, orchestrator, reactor, pool):
        self.orchestrator = orchestrator
        self.reactor = reactor
        self.pool = pool
        self.orchestrator.on_all_jobs_finished = self.shutdown

    async def startup(self):
        try:
            await self.pool.open()
            await self.orchestrator.schedule()

        except Exception:
            logger.exception("Error starting application.")
            await self._close_pool()
            self.reactor.stop()

    def shutdown(self):
       
        defer.ensureDeferred(self._shutdown())

    async def _shutdown(self):
        try:
            await self.pool.close()
        except Exception:
            logger.exception("Error closing PostgreSQL pool.")
        finally:
            self.reactor.stop()

    def run(self):
        self.reactor.callWhenRunning(
            lambda: defer.ensureDeferred(
                self.startup()
            )
        )

        self.reactor.run()

    async def _close_pool(self):
        try:
            await self.pool.close()
        except Exception:
            logger.exception("Error closing PostgreSQL pool.")