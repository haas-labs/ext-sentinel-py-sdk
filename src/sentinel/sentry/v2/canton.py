import hashlib
import time
from typing import Any, Dict, Optional

from sentinel.core.v2.sentry import AsyncCoreSentry
from sentinel.core.v2.settings import Settings
from sentinel.models.chains.canton.update import CantonUpdate
from sentinel.models.event import Blockchain, Event

CANTON = Blockchain(network="canton", chain_id="canton")


def hash_id(value: Optional[str]) -> Optional[str]:
    """
    Party, contract and participant ids never leave a Canton sentry in the clear: every alert
    carries their sha256 instead, under a key with a _hash suffix.
    """
    if value is None:
        return None
    return hashlib.sha256(value.encode("utf-8")).hexdigest()

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

    async def emit(
        self,
        type: str,
        severity: float,
        update: CantonUpdate,
        category: str = "ALERT",
        desc: Optional[str] = None,
        **metadata: Any,
    ) -> Event:
        """
        Build and send the Event every Canton detector emits alike: blockchain fixed to canton,
        ts = the update's record_time, and offset / update_id / synchronizer_id always in metadata
        so an alert is traceable to the ledger. Callers pass ids already hashed (see hash_id).
        """
        event = Event(
            did=self.name,
            sid="ext:sentinel",
            category=category,
            type=type,
            severity=severity,
            desc=desc,
            ts=update.record_time or int(time.time() * 1000),
            blockchain=CANTON,
            metadata={
                "offset": update.offset,
                "update_id": update.update_id,
                "synchronizer_id": update.synchronizer_id,
                **metadata,
            },
        )
        await self.outputs.events.send(event)
        return event
