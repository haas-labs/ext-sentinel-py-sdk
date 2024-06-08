import json

import pytest
from sentinel.core.v2.sentry import Sentry
from sentinel.metrics.enum import Enum
from sentinel.sentry.v2.metric import MetricServer


def test_metric_server_init():
    server = MetricServer()
    assert isinstance(server, MetricServer), "Incorrect metric server type"

    server = MetricServer().from_settings(
        Sentry(
            id="metrics/server",
            name="MetricServer",
            type="sentinel.sentry.v2.metric.MetricServer",
            parameters={"port": 9090},
        )
    )
    assert isinstance(server, MetricServer), "Incorrect metric server type"


@pytest.mark.asyncio
async def test_metric_server_health_check(aiohttp_client):
    server = MetricServer()
    server.init()
    client = await aiohttp_client(server.create_web_app())
    resp = await client.get("/health")
    assert resp.status == 200, "Incorrect health check reponse status code"
    response = json.loads(await resp.text())
    assert response["status"] == "healthy", "Incorrect health status"
    assert response["host"].startswith("127.0.0.1:"), "Incorrect host"


@pytest.mark.asyncio
async def test_metric_server_health_put_and_get_metrics(aiohttp_client):
    enum_metric = Enum(
        name="component_state",
        doc="Current component state",
        labels={"component": "comp_a"},
        states=["not_started", "running", "finished"],
    )
    enum_metric.set(labels={"component": "#A"}, value="running")
    enum_metric.set(labels={"component": "#B"}, value="running")
    enum_metric_data = enum_metric.dump().model_dump()

    server = MetricServer()
    server.init()

    client = await aiohttp_client(server.create_web_app())
    resp = await client.put("/metrics", json=[enum_metric_data])
    assert resp.status == 200, "Incorrect status code"
    response = json.loads(await resp.text())
    assert response["status"] == "accepted", "Incorrect response status"

    enum_metric.set(labels={"component": "#A"}, value="finished")
    enum_metric.set(labels={"component": "#B"}, value="finished")
    enum_metric_data = enum_metric.dump().model_dump()

    resp = await client.put("/metrics", json=[enum_metric_data])
    assert resp.status == 200, "Incorrect status code"
    response = json.loads(await resp.text())
    assert response["status"] == "accepted", "Incorrect response status"

    resp = await client.get("/metrics")
    assert resp.status == 200, "Incorrect status code"
    response: str = await resp.text()
    assert len(response.split("\n")) == 8, "Incorrect number of lines in the response"
