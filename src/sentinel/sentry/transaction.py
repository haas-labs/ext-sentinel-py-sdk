import asyncio

from typing import Dict, List

from sentinel.sentry.core import AsyncCoreSentry

from sentinel.metrics.core import MetricQueue
from sentinel.metrics.collector import MetricModel
from sentinel.channels.metric.core import MetricChannel

from sentinel.definitions import BLOCKCHAIN

from sentinel.models.transaction import Transaction
from sentinel.models.project import ProjectSettings

"""
Transaction Detector uses for detection different cases in transaction stream.

The detector's dependencies (mandatory):
- inbound transaction channel
- outbound event channel

Optional dependencies:
- different databases

"""


class TransactionDetector(AsyncCoreSentry):
    name = "TransactionDetector"
    description = """
        The base detector which can be used for mointoring activities 
        in transactions stream and publishing results to events stream 
    """

    def __init__(
        self,
        name: str = None,
        description: str = None,
        restart: bool = True,
        parameters: Dict = dict(),
        inputs: List[str] = list(),
        outputs: List[str] = list(),
        databases: List[str] = list(),
        metrics: MetricQueue = None,
        schedule: str = None,
        settings: ProjectSettings = None,
    ) -> None:
        super().__init__(
            name=name,
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

        # remove empty spaces and new lines in description
        self.description = " ".join(self.description.split())

        network = parameters.get("network")
        assert network is not None, f"Unknown network, {network}"

        detector_prefix = BLOCKCHAIN.get(network).network
        self.logger_name = "://".join([detector_prefix, name]) if network != "" else name

    # handle incoming transaction
    async def on_transaction(self, transaction: Transaction) -> None: ...

    # handle incoming metrics
    async def on_metric(self, metric: MetricModel) -> None: ...

    async def _run(self) -> None:
        """
        Run Transaction Detector processing
        """
        await self.on_init()

        try:
            tasks = []

            # Inputs
            for name in self.inputs.channels:
                self.logger.info(f"Starting channel, name: {name}")
                channel_inst = getattr(self.inputs, name)
                if name == "transactions":
                    channel_inst.on_transaction = self.on_transaction
                channel_task = asyncio.create_task(channel_inst.run(), name=name)
                tasks.append(channel_task)

            # Outputs
            for name in self.outputs.channels:
                self.logger.info(f"Starting channel, name: {name}")
                channel_inst = getattr(self.outputs, name)
                channel_task = asyncio.create_task(channel_inst.run(), name=name)
                tasks.append(channel_task)

            # Metrics
            # if self.metrics_queue is not None:
            #     self.logger.info("Starting channel, name: metrics")
            #     metric_inst = MetricChannel(
            #         name="metrics",
            #         record_type="sentinel.metrics.collector.MetricModel",
            #         metric_queue=self.metrics_queue,
            #     )
            #     metric_task = asyncio.create_task(metric_inst.run(), name=name)
            #     tasks.append(metric_task)

            await asyncio.gather(*tasks)
        finally:
            self.logger.info("Transaction Detector Processing completed")
