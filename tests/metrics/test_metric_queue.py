import pytest

from sentinel.metrics.core import MetricQueue


def test_metric_queue_init():
    metrics = MetricQueue()
    assert isinstance(metrics, MetricQueue), "Incorrect metric queue type"


@pytest.mark.asyncio
async def test_metric_queue_send_receive():
    TEST_METRICS = {"total_requests": 10}
    metric_queue = MetricQueue()
    await metric_queue.send(metrics=TEST_METRICS)
    metrics = await metric_queue.receive()
    assert metrics == TEST_METRICS, "Unexpected metric value"
