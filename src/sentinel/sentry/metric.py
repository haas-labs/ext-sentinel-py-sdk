import asyncio
from typing import Dict
from aiohttp import web

from sentinel.metrics.core import MetricQueue
from sentinel.models.project import ProjectSettings
from sentinel.sentry.core import AsyncCoreSentry


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
        inputs: web.List[str] = list(),
        outputs: web.List[str] = list(),
        databases: web.List[str] = list(),
        metrics: MetricQueue = None,
        schedule: str = None,
        settings: ProjectSettings = None,
    ) -> None:
        super().__init__(
            nama=name,
            description=description,
            restart=restart,
            parameters=parameters,
            inputs=inputs,
            outputs=outputs,
            databases=databases,
            metrics=metrics,
            schedule=schedule,
            settings=settings,
        )
        self._registry = None

    async def create_web_server(self) -> web.TCPSite:
        srv = web.Application(logger=self.logger)
        srv.add_routes(
            [
                web.get("/metrics", self.metrics),
                web.get("/health", self.health),
            ]
        )
        app_runner = web.AppRunner(srv)
        await app_runner.setup()
        # TODO add option to manage host and port via sentry parameters
        return web.TCPSite(runner=app_runner, host="0.0.0.0", port=9090)

    async def _run(self) -> None:
        try:
            srv = await self.create_web_server()
            await srv.start()
            metric_processor = asyncio.create_task(self.process(), name="MetricsProcessor")
            await asyncio.gather(metric_processor)
        finally:
            self.logger.info("Metric Server completed")

    async def process(self):
        while True:
            metrics = await self.metrics_queue.receive()
            self.logger.info(f"Processing metrics: {metrics}")

    async def health(self, request: web.Request) -> web.Response:
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

    async def metrics(self, request: web.Request) -> web.Response:
        """
        Metrics Endpoint
        """
        return web.Response(text="Metrics Server")
