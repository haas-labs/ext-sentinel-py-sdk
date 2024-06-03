from sentinel.metrics.core import MetricQueue
from sentinel.sentry.v2.metric import MetricServer


def test_sentry_metrics_server():
    queue = MetricQueue()
    server = MetricServer(metrics=queue)
    assert isinstance(server, MetricServer), "Incorrect metric server type"


# @pytest.mark.asyncio
# async def test_sentry_metrics_server_run():
#     queue = MetricQueue()
#     server = MetricServer(metrics=queue)
#     await server._run()
