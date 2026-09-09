"""
Canton ledger update, as published by the Canton ingestion adapter and consumed by Canton sentries.

Canton has no blocks and no global chain: a participant node only sees the transactions in which
one of its parties is a stakeholder or informee. The unit the Ledger API streams is the *update*
(UpdateService.GetUpdates), of four kinds: Transaction, Reassignment, TopologyTransaction and
OffsetCheckpoint. This model flattens every kind into one envelope plus a list of typed events, so
a sentry can pattern-match on `event.type` without caring which kind carried it.

Offsets are participant-local int64 and are not comparable across participants; `update_id` is
the cross-participant identity of an update and the deduplication key for consumers.

`from_json_api` and `snapshot_from_json_api` build the model from the JSON Ledger API v2 payloads
(the `value`-wrapped shapes served by the participant's http-ledger-api). The gRPC adapter maps the
same field names in snake_case.
"""

import hashlib
import json
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

from pydantic import BaseModel, Field


class CantonUpdateKind(str, Enum):
    TRANSACTION = "transaction"
    REASSIGNMENT = "reassignment"
    TOPOLOGY = "topology"
    CHECKPOINT = "checkpoint"
    # The bootstrap of the active contract set plus incomplete reassignments, published once when
    # the adapter starts, before it opens the stream at the same offset.
    SNAPSHOT = "snapshot"


class CantonEventType(str, Enum):
    CREATED = "created"
    EXERCISED = "exercised"
    ARCHIVED = "archived"
    UNASSIGNED = "unassigned"
    ASSIGNED = "assigned"
    AUTHORIZATION_ADDED = "authorization_added"
    AUTHORIZATION_CHANGED = "authorization_changed"
    AUTHORIZATION_REVOKED = "authorization_revoked"
    AUTHORIZATION_ONBOARDING = "authorization_onboarding"


class ParticipantPermission(str, Enum):
    SUBMISSION = "SUBMISSION"
    CONFIRMATION = "CONFIRMATION"
    OBSERVATION = "OBSERVATION"
    UNSPECIFIED = "UNSPECIFIED"


class CantonEvent(BaseModel):
    """
    One event inside an update. Which fields are set depends on `type`:

    - created / exercised / archived: contract_id, template_id, package_name, witness_parties,
      interface_ids, acs_delta; created adds signatories, observers, created_at, payload_hash;
      exercised adds choice, acting_parties, consuming, last_descendant_node_id, payload_hash (of
      the choice argument)
    - unassigned / assigned: contract_id, template_id, reassignment_id, source, target, submitter,
      reassignment_counter; unassigned adds assignment_exclusivity; assigned adds the created
      contract fields (signatories, observers) on the target synchronizer
    - authorization_*: party, participant, permission (revoked has no permission)
    """

    type: CantonEventType
    offset: Optional[int] = None
    node_id: Optional[int] = None

    # contract events
    contract_id: Optional[str] = None
    template_id: Optional[str] = None
    package_name: Optional[str] = None
    signatories: List[str] = Field(default_factory=list)
    observers: List[str] = Field(default_factory=list)
    witness_parties: List[str] = Field(default_factory=list)
    interface_ids: List[str] = Field(default_factory=list)  # interfaces the contract implements (views on created, interface_id / implemented on exercised)
    acs_delta: Optional[bool] = None  # whether the event changes the active-contracts set of the reading parties
    created_at: Optional[int] = None  # epoch ms, created events

    # exercised
    choice: Optional[str] = None
    acting_parties: List[str] = Field(default_factory=list)
    consuming: Optional[bool] = None
    last_descendant_node_id: Optional[int] = None

    # reassignment
    reassignment_id: Optional[str] = None
    source: Optional[str] = None
    target: Optional[str] = None
    submitter: Optional[str] = None
    reassignment_counter: Optional[int] = None
    assignment_exclusivity: Optional[int] = None  # epoch ms

    # topology
    party: Optional[str] = None
    participant: Optional[str] = None
    permission: Optional[ParticipantPermission] = None

    # Contract data never leaves the client's trust boundary in the clear. The hash is always
    # present for created/exercised; the raw payload, the contract key, the interface views and the
    # choice result are optional (keep_payload) and meant for the local pipeline only.
    payload_hash: Optional[str] = None
    payload: Optional[Dict[str, Any]] = None
    contract_key: Optional[Any] = None
    interface_views: Optional[List[Dict[str, Any]]] = None
    exercise_result: Optional[Any] = None

    @property
    def stakeholders(self) -> List[str]:
        return list(dict.fromkeys(self.signatories + self.observers))


class CantonUpdate(BaseModel):
    kind: CantonUpdateKind
    offset: int
    update_id: Optional[str] = None
    synchronizer_id: Optional[str] = None
    record_time: Optional[int] = None  # epoch ms
    workflow_id: Optional[str] = None
    command_id: Optional[str] = None
    events: List[CantonEvent] = Field(default_factory=list)
    # checkpoint only: record time per synchronizer (epoch ms), the lag metric of the adapter
    synchronizer_times: Dict[str, int] = Field(default_factory=dict)

    # ------------------------------------------------------------------ JSON Ledger API v2 mapping

    @classmethod
    def from_json_api(cls, update: Dict[str, Any], keep_payload: bool = False) -> "CantonUpdate":
        """
        Build from one element of a GetUpdates / get-updates-page response
        (`{"update": {"Transaction": {"value": {...}}}}` or the inner `{"Transaction": ...}`).
        """
        kind, body = _unwrap(update.get("update", update))
        if kind == "Transaction":
            events = [_contract_event(e, keep_payload) for e in body.get("events", [])]
            return cls(
                kind=CantonUpdateKind.TRANSACTION,
                offset=_offset(body, events),
                update_id=body.get("updateId"),
                synchronizer_id=body.get("synchronizerId"),
                record_time=_ts(body.get("recordTime")),
                workflow_id=body.get("workflowId") or None,
                command_id=body.get("commandId") or None,
                events=events,
            )
        if kind == "Reassignment":
            events = [_reassignment_event(e, keep_payload) for e in body.get("events", [])]
            return cls(
                kind=CantonUpdateKind.REASSIGNMENT,
                offset=_offset(body, events),
                update_id=body.get("updateId"),
                synchronizer_id=body.get("synchronizerId"),
                record_time=_ts(body.get("recordTime")),
                workflow_id=body.get("workflowId") or None,
                command_id=body.get("commandId") or None,
                events=events,
            )
        if kind == "TopologyTransaction":
            events = [_topology_event(e) for e in body.get("events", [])]
            return cls(
                kind=CantonUpdateKind.TOPOLOGY,
                offset=_offset(body, events),
                update_id=body.get("updateId"),
                synchronizer_id=body.get("synchronizerId"),
                record_time=_ts(body.get("recordTime")),
                events=events,
            )
        if kind == "OffsetCheckpoint":
            return cls(
                kind=CantonUpdateKind.CHECKPOINT,
                offset=int(body.get("offset") or 0),
                synchronizer_times={
                    s.get("synchronizerId"): _ts(s.get("recordTime")) for s in body.get("synchronizerTimes", [])
                },
            )
        raise ValueError(f"Unknown Canton update kind: {kind}")

    @classmethod
    def snapshot_from_json_api(
        cls, entries: List[Dict[str, Any]], offset: int, keep_payload: bool = False
    ) -> "CantonUpdate":
        """
        Build the bootstrap snapshot from a GetActiveContracts response taken at `offset`.
        Active contracts become `created` events; incomplete reassignments become `unassigned` /
        `assigned` events, so a sentry that tracks reassignments inherits the pending ones.
        """
        events: List[CantonEvent] = []
        for entry in entries:
            kind, body = _unwrap(entry.get("contractEntry", entry))
            if kind == "JsActiveContract":
                ev = _contract_event({"CreatedEvent": body["createdEvent"]}, keep_payload)
                ev.source = body.get("synchronizerId")
                ev.reassignment_counter = body.get("reassignmentCounter")
                events.append(ev)
            elif "Unassigned" in kind:
                events.append(_reassignment_event({"UnassignedEvent": body.get("unassignedEvent", body)}, keep_payload))
            elif "Assigned" in kind:
                events.append(_reassignment_event({"AssignedEvent": body.get("assignedEvent", body)}, keep_payload))
        return cls(kind=CantonUpdateKind.SNAPSHOT, offset=offset, events=events)


# ---------------------------------------------------------------------------------- helpers


def _unwrap(node: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
    """JSON API oneOf shapes: {"Kind": {"value": {...}}}, {"event": {"Kind": {...}}} or {"Kind": {...}}."""
    node = node.get("event", node)
    kind, body = next(iter(node.items()))
    if isinstance(body, dict) and set(body.keys()) == {"value"}:
        body = body["value"]
    return kind, body


def _ts(value: Optional[str]) -> Optional[int]:
    if not value:
        return None
    if isinstance(value, (int, float)):
        return int(value)
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return int(dt.timestamp() * 1000)


def _offset(body: Dict[str, Any], events: List[CantonEvent]) -> int:
    return max([int(body.get("offset") or 0)] + [e.offset or 0 for e in events])


def payload_hash(payload: Any) -> Optional[str]:
    if payload is None:
        return None
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _permission(value: Optional[str]) -> Optional[ParticipantPermission]:
    if not value:
        return None
    name = value.replace("PARTICIPANT_PERMISSION_", "")
    try:
        return ParticipantPermission(name)
    except ValueError:
        return ParticipantPermission.UNSPECIFIED


def _contract_event(raw: Dict[str, Any], keep_payload: bool) -> CantonEvent:
    kind, b = _unwrap(raw)
    common = dict(
        offset=b.get("offset"),
        node_id=b.get("nodeId"),
        contract_id=b.get("contractId"),
        template_id=b.get("templateId"),
        package_name=b.get("packageName"),
        witness_parties=list(b.get("witnessParties", [])),
        acs_delta=b.get("acsDelta"),
    )
    if kind == "CreatedEvent":
        arg = b.get("createArgument", b.get("createArguments"))
        views = b.get("interfaceViews") or []
        return CantonEvent(
            type=CantonEventType.CREATED,
            signatories=list(b.get("signatories", [])),
            observers=list(b.get("observers", [])),
            interface_ids=[v.get("interfaceId") for v in views if v.get("interfaceId")],
            created_at=_ts(b.get("createdAt")),
            payload_hash=payload_hash(arg),
            payload=arg if keep_payload else None,
            contract_key=b.get("contractKey") if keep_payload else None,
            interface_views=views if keep_payload and views else None,
            **common,
        )
    if kind == "ExercisedEvent":
        arg = b.get("choiceArgument")
        interfaces = ([b["interfaceId"]] if b.get("interfaceId") else []) + list(b.get("implementedInterfaces") or [])
        return CantonEvent(
            type=CantonEventType.EXERCISED,
            choice=b.get("choice"),
            acting_parties=list(b.get("actingParties", [])),
            consuming=b.get("consuming"),
            last_descendant_node_id=b.get("lastDescendantNodeId"),
            interface_ids=list(dict.fromkeys(interfaces)),
            payload_hash=payload_hash(arg),
            payload=arg if keep_payload else None,
            exercise_result=b.get("exerciseResult") if keep_payload else None,
            **common,
        )
    if kind == "ArchivedEvent":
        return CantonEvent(type=CantonEventType.ARCHIVED, **common)
    raise ValueError(f"Unknown Canton contract event: {kind}")


def _reassignment_event(raw: Dict[str, Any], keep_payload: bool) -> CantonEvent:
    kind, b = _unwrap(raw)
    common = dict(
        reassignment_id=b.get("reassignmentId") or b.get("unassignId"),
        source=b.get("source"),
        target=b.get("target"),
        submitter=b.get("submitter"),
        reassignment_counter=b.get("reassignmentCounter"),
    )
    if "unassign" in kind.lower():
        return CantonEvent(
            type=CantonEventType.UNASSIGNED,
            offset=b.get("offset"),
            node_id=b.get("nodeId"),
            contract_id=b.get("contractId"),
            template_id=b.get("templateId"),
            package_name=b.get("packageName"),
            witness_parties=list(b.get("witnessParties", [])),
            assignment_exclusivity=_ts(b.get("assignmentExclusivity")),
            **common,
        )
    if "assign" in kind.lower():
        created = _contract_event({"CreatedEvent": b["createdEvent"]}, keep_payload) if b.get("createdEvent") else CantonEvent(type=CantonEventType.CREATED)
        return CantonEvent(
            type=CantonEventType.ASSIGNED,
            offset=created.offset,
            node_id=created.node_id,
            contract_id=created.contract_id,
            template_id=created.template_id,
            package_name=created.package_name,
            signatories=created.signatories,
            observers=created.observers,
            witness_parties=created.witness_parties,
            payload_hash=created.payload_hash,
            payload=created.payload,
            **common,
        )
    raise ValueError(f"Unknown Canton reassignment event: {kind}")


_TOPOLOGY_TYPES = {
    "ParticipantAuthorizationAdded": CantonEventType.AUTHORIZATION_ADDED,
    "ParticipantAuthorizationChanged": CantonEventType.AUTHORIZATION_CHANGED,
    "ParticipantAuthorizationRevoked": CantonEventType.AUTHORIZATION_REVOKED,
    "ParticipantAuthorizationOnboarding": CantonEventType.AUTHORIZATION_ONBOARDING,
}


def _topology_event(raw: Dict[str, Any]) -> CantonEvent:
    kind, b = _unwrap(raw)
    if kind not in _TOPOLOGY_TYPES:
        raise ValueError(f"Unknown Canton topology event: {kind}")
    return CantonEvent(
        type=_TOPOLOGY_TYPES[kind],
        party=b.get("partyId"),
        participant=b.get("participantId"),
        permission=_permission(b.get("participantPermission")),
    )
