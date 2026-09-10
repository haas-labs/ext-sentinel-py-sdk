import hashlib
import time
from collections import deque
from typing import Any, Deque, Dict, Optional, Set

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


RECENT_UPDATES = 10_000  # update_ids remembered for deduplication


class CantonUpdateDetector(AsyncCoreSentry):
    name = "CantonUpdateDetector"
    description = "Base detector over a Canton participant's update stream"

    # The policy an alert was judged against: the detector's manifest (name, version) and, when
    # the parameters came from the Extractor, the monitoring condition id. Subclasses set the
    # first two in configure(); on_config_change sets the third.
    policy_name: Optional[str] = None
    policy_version: Optional[str] = None
    policy_config_id: Optional[int] = None

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
        self._recent_ids: Deque[str] = deque(maxlen=RECENT_UPDATES)
        self._recent_set: Set[str] = set()

    def init(self) -> None:
        super().init()
        if getattr(self.inputs, "updates", None):
            self.inputs.updates.on_update = self.handle_update
        else:
            raise AttributeError("Missed required updates input channel, please check configuration")
        # Optional: the Extractor's monitoring conditions, the platform's standard wiring. The
        # `config` input channel delivers every record of the conditions topic; the
        # `monitoring_conditions` database (RemoteMonitoringConditionsDB) keeps the ACTIVE ones of
        # this detector's schema on this chain uid; the newest of them is the policy in force, its
        # fields landing on top of the profile parameters. One tenant per sentry.
        if getattr(self.inputs, "config", None):
            self.inputs.config.on_config_change = self.on_config_change
        db = self.conditions_db()
        if db is not None:
            db.ingest()  # the full state of the topic, before the loop starts (as every detector does)
            self.sync_policy()

    async def handle_update(self, update: CantonUpdate) -> None:
        """
        Every update passes here before on_update. The adapter persists its offset only after
        the broker's ack, so a crash in between republishes a page; update_id is the
        cross-participant identity of an update and the key that makes that republish harmless.
        Snapshots carry no update_id and are never deduplicated.
        """
        if update.update_id:
            if update.update_id in self._recent_set:
                self.logger.info(f"update {update.update_id[:12]}… already seen at this offset range, skipped")
                return
            if len(self._recent_ids) == self._recent_ids.maxlen:
                self._recent_set.discard(self._recent_ids[0])
            self._recent_ids.append(update.update_id)
            self._recent_set.add(update.update_id)
        await self.on_update(update)

    # handle incoming Canton update
    async def on_update(self, update: CantonUpdate) -> None: ...

    @property
    def policy(self) -> Dict[str, Any]:
        return {"name": self.policy_name, "version": self.policy_version, "config_id": self.policy_config_id}

    # ------------------------------------------------------------- configuration

    def configure(self, parameters: Dict) -> None:
        """Detectors override this to read their parameters; called again on every config change."""

    def conditions_db(self):
        databases = getattr(self, "databases", None)
        return getattr(databases, "monitoring_conditions", None) if databases is not None else None

    async def on_config_change(self, record: Any = None, config: Optional[Configuration] = None) -> None:
        """
        Called by the `config` channel with a raw record of the conditions topic, or directly with
        a parsed Configuration (local profiles, tests). A record goes through the database, which
        filters by source, chain uid, schema name/version and status; then the policy in force is
        recomputed from what the database holds.
        """
        if config is None and isinstance(record, Configuration):
            config = record
        if config is not None:
            self.apply_configuration(config)
            return
        db = self.conditions_db()
        if db is None or record is None:
            return
        db.update(record)
        self.sync_policy()

    def sync_policy(self) -> None:
        """The newest ACTIVE condition of this detector is the policy; none means the profile defaults."""
        db = self.conditions_db()
        configs = dict(getattr(db, "_config_db", {}) or {}) if db is not None else {}
        if not configs:
            if self.policy_config_id is not None:
                self.restore_profile("no active condition left")
            return
        newest = max(configs.values(), key=lambda c: (c.updated_at or 0, c.id))
        if newest.id != self.policy_config_id or newest.updated_at != getattr(self, "_policy_updated_at", None):
            self.apply_configuration(newest)

    def apply_configuration(self, config: Configuration) -> None:
        """
        A monitoring condition for this detector arrived or changed. Its `config` carries the
        fields of the detector's manifest Schema; an ACTIVE one replaces the parameters of the
        same name, a DISABLED or DELETED one restores the profile defaults. The condition's
        entity (the client's party id in `contract.address`) becomes a monitored party unless
        the condition names them itself.
        """
        if self.policy_name and config.config_schema.name != self.policy_name:
            return  # a condition of another detector on the shared conditions topic
        if config.status != Status.ACTIVE:
            self.restore_profile(f"configuration {config.id} {config.status.value}")
            return
        base = dict(getattr(self, "profile_parameters", None) or self.parameters or {})
        fields = dict(config.config or {})
        party = getattr(config.contract, "address", None)
        if party and not fields.get("monitored_parties"):
            fields["monitored_parties"] = sorted(set(base.get("monitored_parties") or []) | {party})
        base.update(fields)
        self.policy_config_id = config.id
        self._policy_updated_at = config.updated_at
        self.logger.info(f"configuration {config.id} applied: {sorted(fields.keys())}")
        self.profile_parameters = dict(getattr(self, "profile_parameters", None) or self.parameters or {})
        self.configure(base)

    def restore_profile(self, why: str) -> None:
        self.policy_config_id = None
        self._policy_updated_at = None
        self.logger.info(f"{why}: back to profile parameters")
        self.profile_parameters = dict(getattr(self, "profile_parameters", None) or self.parameters or {})
        self.configure(dict(self.profile_parameters))

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
        cid = the monitoring condition in force (None when the parameters come from the profile),
        ts = the update's record_time, and offset / update_id / synchronizer_id always in metadata
        so an alert is traceable to the ledger. Callers pass ids already hashed (see hash_id).
        """
        event = Event(
            did=self.name,
            sid="ext:sentinel",
            cid=self.policy_config_id,  # the monitoring condition: what links the alert to the entity and project
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
                "policy": self.policy,
                **metadata,
            },
        )
        await self.outputs.events.send(event)
        webhook = getattr(self.outputs, "webhook", None)
        if webhook is not None:  # the client's own receiver, when the profile declares one
            await webhook.send(event)
        return event
