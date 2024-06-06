import asyncio
import signal
import time
from typing import Dict

from aiohttp import web
from sentinel.core.v2.sentry import AsyncCoreSentry
from sentinel.metrics.core import MetricDatabase, MetricQueue
from sentinel.metrics.formatter import PrometheusFormattter
from sentinel.models.sentry import Sentry

routes = web.RouteTableDef()


class MetricServer(AsyncCoreSentry):
    name = "MetricServer"
    description = """The server for collecting metrics from sentries 
                     via metrics queue and provide HTTP endpoint for 
                     integration with Prometeus"""

    def __init__(
        self,
        metrics_queue: MetricQueue,
        name: str = None,
        description: str = None,
        restart: bool = True,
        schedule: str = None,
        parameters: Dict = dict(),
        **kwargs,
    ) -> None:
        super().__init__(
            name=name,
            description=description,
            restart=restart,
            schedule=schedule,
            parameters=parameters,
            metrics_queue=metrics_queue,
            **kwargs,
        )
        self._metrics_queue = metrics_queue
        self._retention_period_secs = self.parameters.get("retention_period", 30)
        self._retention_period_msecs = self._retention_period_secs * 1000
        self._host = self.parameters.get("host", "0.0.0.0")
        self._port = self.parameters.get("port", 9090)
        self._db = MetricDatabase(retention_period=self._retention_period_secs)

    @classmethod
    def from_settings(cls, settings: Sentry, metrics_queue: MetricQueue, **kwargs):
        return cls(
            name=settings.name,
            description=settings.description,
            restart=settings.restart,
            schedule=settings.schedule,
            parameters=settings.parameters,
            metrics_queue=metrics_queue,
            **kwargs,
        )

    def current_time(self) -> int:
        """
        return current time in milliseconds
        """
        return int(time.time())

    async def handle_incoming_metrics(self):
        loop = asyncio.get_running_loop()
        last_cleanup_time = self.current_time()
        while True:
            metrics = await loop.run_in_executor(None, self._metrics_queue.receive)
            self._db.update(metrics)

            # cleanup outdated metrics in database by retention period
            current_time = self.current_time()
            if (current_time - last_cleanup_time) > self._retention_period_secs:
                self._db.clean()
                last_cleanup_time = self.current_time()

    def create_web_app(self) -> web.Application:
        app = web.Application(logger=self.logger)
        app.router.add_get("/metrics", self.handle_metrics)
        app.router.add_get("/health", self.handle_health)
        return app

    async def handle_health(self, request: web.Request) -> web.Response:
        health_status = {
            "status": "healthy",
            "host": request.host,
        }
        self.logger.info(health_status)
        return web.json_response(data=health_status)

    async def handle_metrics(self, request: web.Request) -> web.Response:
        """
        Metrics Endpoint
        """
        metrics = PrometheusFormattter().format(self._db)
        return web.Response(text=metrics)

    async def background_tasks(self, app: web.Application):
        self.logger.info("Starting background tasks")
        app[self.metrics_handler] = asyncio.create_task(self.handle_incoming_metrics())
        yield
        self.logger.info("Stopping background tasks")
        # app[self.metrics_handler].cancel()
        # await app[self.metrics_handler]
        # self.logger.info("Background tasks termination completed")

    def signal_handler(self, app: web.Application) -> None:
        asyncio.ensure_future(app.shutdown())
        asyncio.ensure_future(app.cleanup())

    def run(self) -> None:
        """
        Method representing async sentry's activity
        """
        self.init()

        app = self.create_web_app()
        self.metrics_handler = web.AppKey("metrics_handler", asyncio.Task[None])
        app.cleanup_ctx.append(self.background_tasks)

        loop = asyncio.get_event_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, self.signal_handler, app)

        web.run_app(app=app, host=self._host, port=self._port, ssl_context=None)
