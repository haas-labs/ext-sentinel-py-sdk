from typing import List

import httpx
from sentinel.metrics.core import MetricModel
from sentinel.utils.logger import Logger, get_logger


async def async_publish_metrics(
    metric_server_url: str, metrics: List[MetricModel], logger: Logger = get_logger(__name__)
) -> None:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.put(url=metric_server_url, json=metrics)
            if response.status_code != 200:
                logger.warning(f"Metrics update issue, response: {response}")
    except httpx.ConnectError as err:
        logger.warning(f"No connection to Metrics Server, error: {err}")


def publish_metrics(metric_server_url: str, metrics: List[MetricModel], logger: Logger = get_logger(__name__)) -> None:
    try:
        with httpx.Client() as client:
            response = client.put(url=metric_server_url, json=metrics)
            if response.status_code != 200:
                logger.warning(f"Metrics update issue, response: {response}")
    except httpx.ConnectError as err:
        logger.warning(f"No connection to Metrics Server, error: {err}")
