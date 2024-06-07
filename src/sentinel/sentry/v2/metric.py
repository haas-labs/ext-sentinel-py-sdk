import time
from typing import Dict

from aiohttp import web
from sentinel.core.v2.sentry import AsyncCoreSentry
from sentinel.metrics.core import MetricDatabase, MetricModel
from sentinel.metrics.formatter import PrometheusFormattter
from sentinel.models.sentry import Sentry


class MetricServer(AsyncCoreSentry):
    name = "MetricServer"
    description = """The server for collecting metrics from sentries 
                     via metrics queue and provide HTTP endpoint for 
                     integration with Prometeus"""

    def __init__(
        self,
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
            **kwargs,
        )
        self._retention_period_secs = self.parameters.get("retention_period", 30)
        self._retention_period_msecs = self._retention_period_secs * 1000
        self._host = self.parameters.get("host", "0.0.0.0")
        self._port = self.parameters.get("port", 9090)
        self._db = MetricDatabase(retention_period=self._retention_period_secs)
        self.last_cleanup_time = self.current_time()

    @classmethod
    def from_settings(cls, settings: Sentry, **kwargs):
        return cls(
            name=settings.name,
            description=settings.description,
            restart=settings.restart,
            schedule=settings.schedule,
            parameters=settings.parameters,
            **kwargs,
        )

    def current_time(self) -> int:
        """
        return current time in milliseconds
        """
        return int(time.time())

    def create_web_app(self) -> web.Application:
        app = web.Application(logger=self.logger)
        app.router.add_put("/metrics", self.update_metrics)
        app.router.add_get("/metrics", self.get_metrics)
        app.router.add_get("/health", self.handle_health)
        return app

    async def handle_health(self, request: web.Request) -> web.Response:
        health_status = {
            "status": "healthy",
            "host": request.host,
        }
        self.logger.info(health_status)
        return web.json_response(data=health_status)

    async def get_metrics(self, request: web.Request) -> web.Response:
        # cleanup outdated metrics in database by retention period
        current_time = self.current_time()
        if (current_time - self.last_cleanup_time) > self._retention_period_secs:
            self._db.clean()
            self.last_cleanup_time = self.current_time()

        metrics = PrometheusFormattter().format(self._db)
        return web.Response(text=metrics)

    async def update_metrics(self, request: web.Request) -> web.Resource:
        metrics_data = await request.json()
        for metric in metrics_data:
            self._db.update(metric=MetricModel(**metric))
        return web.json_response({"status": "accepted"})

    def run(self) -> None:
        self.init()

        app = self.create_web_app()
        web.run_app(app=app, host=self._host, port=self._port, ssl_context=None)
