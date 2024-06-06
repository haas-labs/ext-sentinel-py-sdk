import asyncio
import time
from typing import Dict

from aiohttp import web
from sentinel.core.v2.sentry import AsyncCoreSentry
from sentinel.metrics.core import MetricDatabase, MetricQueue
from sentinel.metrics.formatter import PrometheusFormattter
from sentinel.models.sentry import Sentry


class MetricServer(AsyncCoreSentry):
    name = "MetricServer"
    description = """The server for collecting metrics from sentries 
                     via metrics queue and provide HTTP endpoint for 
                     integration with Prometeus"""

    def __init__(
        self,
        metrics: MetricQueue,
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
            metrics=metrics,
            **kwargs,
        )
        self._metrics_queue = metrics
        self._retention_period_secs = self.parameters.get("retention_period", 30)
        self._retention_period_msecs = self._retention_period_secs * 1000
        self._host = self.parameters.get("host", "0.0.0.0")
        self._port = self.parameters.get("port", 9090)
        self._db = MetricDatabase(retention_period=self._retention_period_secs)

    @classmethod
    def from_settings(cls, settings: Sentry, **kwargs):
        queue = kwargs.pop("metrics_queue", None)
        return cls(
            name=settings.name,
            description=settings.description,
            restart=settings.restart,
            schedule=settings.schedule,
            parameters=settings.parameters,
            metrics=queue,
            **kwargs,
        )

    def current_time(self) -> int:
        """
        return current time in milliseconds
        """
        return int(time.time())

    async def create_web_server(self) -> web.TCPSite:
        srv = web.Application(logger=self.logger)
        srv.add_routes(
            [
                web.get("/metrics", self.handle_metrics),
                web.get("/health", self.handle_health),
            ]
        )
        app_runner = web.AppRunner(srv)
        await app_runner.setup()
        return web.TCPSite(runner=app_runner, host=self._host, port=self._port)

    async def handle_web_requests(self):
        srv = web.Application(logger=self.logger)
        srv.add_routes(
            [
                web.get("/metrics", self.handle_metrics),
                web.get("/health", self.handle_health),
            ]
        )
        app_runner = web.AppRunner(srv)
        await app_runner.setup()
        site = web.TCPSite(runner=app_runner, host=self._host, port=self._port)
        await site.start()

    async def processing(self) -> None:
        self.init()
        handlers = []
        try:
            # srv = await self.create_web_server()
            # await srv.start()
            web_requests_handler = asyncio.create_task(self.handle_web_requests(), name="WebRequestsHandler")
            handlers.append(web_requests_handler)

            metric_processor = asyncio.create_task(self.handle_incoming_metrics(), name="MetricsHandler")
            handlers.append(metric_processor)

            await asyncio.gather(*handlers)
        finally:
            self.logger.info("Metric Server completed")

    async def handle_incoming_metrics(self):
        last_cleanup_time = self.current_time()
        while True:
            metrics = await self._metrics_queue.receive()
            self.logger.info(metrics)
            self._db.update(metrics)

            # cleanup outdated metrics in database by retention period
            current_time = self.current_time()
            if (current_time - last_cleanup_time) > self._retention_period:
                self._db.clean()

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
