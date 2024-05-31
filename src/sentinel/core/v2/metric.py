import asyncio
import time
from typing import Dict, List

from aiohttp import web
from sentinel.core.v2.handler import Handler
from sentinel.core.v2.sentry import AsyncCoreSentry
from sentinel.metrics.core import MetricDatabase, MetricQueue
from sentinel.metrics.formatter import PrometheusFormattter
from sentinel.models.project import ProjectSettings


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
        parameters: Dict = dict(),
        handlers: List[Handler] = list(),
        metrics: MetricQueue = None,
        schedule: str = None,
        settings: ProjectSettings = None,
    ) -> None:
        super().__init__(
            name=name,
            description=description,
            restart=restart,
            parameters=parameters,
            handlers=handlers,
            metrics=metrics,
            schedule=schedule,
            settings=settings,
        )
        self._db = MetricDatabase(retention_period=self.parameters.get("retention_period", 30))
        self._retention_period = self.parameters.get("retention_period", 30) * 1000  # convert to milliseconds

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
        # TODO add option to manage host and port via sentry parameters
        return web.TCPSite(runner=app_runner, host="0.0.0.0", port=self.parameters.get("port", 9090))

    async def _run(self) -> None:
        try:
            srv = await self.create_web_server()
            await srv.start()
            metric_processor = asyncio.create_task(self.process(), name="MetricsProcessor")
            await asyncio.gather(metric_processor)
        finally:
            self.logger.info("Metric Server completed")

    async def process(self):
        last_cleanup_time = self.current_time()
        while True:
            metrics = await self.metrics_queue.receive()
            self.logger.info(f"Processing metrics: {metrics}")
            self._db.update(metrics)

            # cleanup outdated metrics in database by retention period
            current_time = self.current_time()
            if (current_time - last_cleanup_time) > self._retention_period:
                self._db.clean()

    async def handle_health(self, request: web.Request) -> web.Response:
        """
        Healthcheck
        ===========

        A web service should respond to a health check with a clear indication of its operational status. Here's a breakdown of key aspects:

        HTTP Status Code
        ----------------

        - 200 OK: This is the ideal response for a healthy service. It indicates the service is up and running normally.
        - Non-200 Status Code: Any other status code signifies an issue. Common examples include:
        - 500 Internal Server Error: The service encountered an internal problem and can't function properly.
        - 503 Service Unavailable: The service is temporarily unavailable due to maintenance or overload.

        Response Body (Optional)
        ------------------------

        While not always mandatory, including a response body can provide additional details about the service's health. This information can be in various formats like JSON or plain text, depending on the implementation. Here are some possible inclusions:

        Simple message: "OK" or "Healthy" for a successful check.
        Detailed status: Information on specific components or dependencies within the service (database connection, external API health).

        Liveness vs. Readiness Checks
        -----------------------------

        Some services differentiate between liveness and readiness checks using separate endpoints:

        - /health/live: Responds with a 200 OK if the service process is running, even if not fully functional.
        - /health/ready: Indicates if the service is ready to handle incoming traffic (all dependencies healthy).

        Choosing the Right Response
        ---------------------------

        The specific response format and details depend on the monitoring system and the desired level of information.
        """
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
