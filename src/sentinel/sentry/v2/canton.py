import hashlib
import time
from typing import Any, Dict, Optional

from sentinel.core.v2.sentry import AsyncCoreSentry
from sentinel.core.v2.settings import Settings
from sentinel.models.chains.canton.update import CantonUpdate
from sentinel.models.config import Configuration, Status
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
        # Optional: the Extractor's monitoring conditions, one configuration per tenant. Its
        # fields are the detector's manifest Schema and land on top of the profile parameters.
        if getattr(self.inputs, "config", None):
            self.inputs.config.on_config_change = self.on_config_change

    # handle incoming Canton update
    async def on_update(self, update: CantonUpdate) -> None: ...

    # ------------------------------------------------------------- configuration

    def configure(self, parameters: Dict) -> None:
        """Detectors override this to read their parameters; called again on every config change."""

    async def on_config_change(self, config: Configuration) -> None:
        """
        A monitoring condition for this detector arrived or changed. Its `config` carries the
        fields of the detector's manifest Schema; an ACTIVE one replaces the parameters of the
        same name, a DISABLED or DELETED one restores the profile defaults.
        """
        if config.config_schema.name != getattr(self, "schema_name", config.config_schema.name):
            return
        base = dict(getattr(self, "profile_parameters", None) or self.parameters or {})
        if config.status == Status.ACTIVE:
            base.update(config.config or {})
            self.logger.info(f"configuration {config.id} applied: {sorted((config.config or {}).keys())}")
        else:
            self.logger.info(f"configuration {config.id} {config.status.value}: back to profile parameters")
        self.profile_parameters = dict(self.parameters or {})
        self.configure(base)

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
        webhook = getattr(self.outputs, "webhook", None)
        if webhook is not None:  # the client's own receiver, when the profile declares one
            await webhook.send(event)
        return event
