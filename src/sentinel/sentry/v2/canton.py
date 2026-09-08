from typing import Dict

from sentinel.core.v2.sentry import AsyncCoreSentry
from sentinel.core.v2.settings import Settings
from sentinel.models.chains.canton.update import CantonUpdate

"""
Canton Update Detector: the base for sentries that watch a participant's update stream.

Mandatory dependencies:
- an inbound `updates` channel (sentinel.channels.kafka.canton or sentinel.channels.fs.canton)
- an outbound event channel

Unlike TransactionDetector there is no `network` parameter bound to BLOCKCHAIN: the stream is
already scoped to one participant and one set of parties by the adapter that produced it.
"""


class CantonUpdateDetector(AsyncCoreSentry):
    name = "CantonUpdateDetector"
    description = "Base detector over a Canton participant's update stream"

    def __init__(
        self,
        name: str = None,
        description: str = None,
        restart: bool = True,
        schedule: str = None,
        parameters: Dict = dict(),
        monitoring_enabled: bool = False,
        monitoring_port: int = 9090,
        settings: Settings = Settings(),
        **kwargs,
    ) -> None:
        super().__init__(
            name=name,
            description=description,
            restart=restart,
            schedule=schedule,
            parameters=parameters,
            monitoring_enabled=monitoring_enabled,
            monitoring_port=monitoring_port,
            settings=settings,
            **kwargs,
        )
        self.logger_name = "canton://" + self.name

    def init(self) -> None:
        super().init()
        if getattr(self.inputs, "updates", None):
            self.inputs.updates.on_update = self.on_update
        else:
            raise AttributeError("Missed required updates input channel, please check configuration")

    # handle incoming Canton update
    async def on_update(self, update: CantonUpdate) -> None: ...
