"""
Samples captured on 2026-09-08 from a local Canton 3.5.16 (two participants, two synchronizers)
through the JSON Ledger API v2 of the client's participant, one per update kind.
"""

import json
import pathlib

from sentinel.models.chains.canton.update import (
    CantonEventType,
    CantonUpdate,
    CantonUpdateKind,
    ParticipantPermission,
)

RES = pathlib.Path("tests/models/chains/canton/resources")


def load(name: str):
    return json.load((RES / name).open("r"))


def test_transaction_created():
    u = CantonUpdate.from_json_api(load("update-transaction-created.json"))
    assert u.kind == CantonUpdateKind.TRANSACTION
    assert u.offset == 47 and u.update_id and u.synchronizer_id.startswith("sync1::")
    assert u.record_time and u.record_time > 1_700_000_000_000, "record_time is epoch ms"
    (ev,) = u.events
    assert ev.type == CantonEventType.CREATED
    assert ev.template_id.endswith(":Iou:Iou") and ev.package_name == "CantonExamples"
    assert [p.split("::")[0] for p in ev.signatories] == ["counterparty"]
    assert [p.split("::")[0] for p in ev.observers] == ["client"]
    assert [p.split("::")[0] for p in ev.witness_parties] == ["client"]
    assert ev.payload_hash and len(ev.payload_hash) == 64, "sha256 of create arguments"
    assert ev.payload is None, "raw payload is not kept by default"


def test_transaction_created_keeps_payload_on_request():
    u = CantonUpdate.from_json_api(load("update-transaction-created.json"), keep_payload=True)
    assert u.events[0].payload["amount"]["currency"] == "USD"


def test_transaction_exercised_carries_the_subtree():
    u = CantonUpdate.from_json_api(load("update-transaction-exercised.json"))
    exercised, created = u.events
    assert exercised.type == CantonEventType.EXERCISED and exercised.choice == "Share"
    assert exercised.consuming is True
    assert [p.split("::")[0] for p in exercised.acting_parties] == ["client"]
    assert exercised.node_id == 0 and exercised.last_descendant_node_id == 1
    assert created.type == CantonEventType.CREATED and created.node_id == 1
    assert sorted(p.split("::")[0] for p in created.observers) == ["client", "stranger"]
    assert exercised.payload_hash and created.payload_hash


def test_topology_added_and_revoked():
    added = CantonUpdate.from_json_api(load("update-topology-added.json"))
    revoked = CantonUpdate.from_json_api(load("update-topology-revoked.json"))
    assert added.kind == revoked.kind == CantonUpdateKind.TOPOLOGY
    (a,) = added.events
    assert a.type == CantonEventType.AUTHORIZATION_ADDED
    assert a.party.startswith("counterparty::") and a.participant.startswith("p1::")
    assert a.permission == ParticipantPermission.CONFIRMATION
    (r,) = revoked.events
    assert r.type == CantonEventType.AUTHORIZATION_REVOKED and r.permission is None
    assert r.party == a.party and r.participant == a.participant
    assert revoked.offset > added.offset


def test_reassignment_unassigned():
    u = CantonUpdate.from_json_api(load("update-reassignment-unassigned.json"))
    assert u.kind == CantonUpdateKind.REASSIGNMENT
    (ev,) = u.events
    assert ev.type == CantonEventType.UNASSIGNED
    assert ev.reassignment_id and ev.contract_id and ev.template_id.endswith(":Iou:Iou")
    assert ev.source.startswith("sync1::") and ev.target.startswith("sync2::")
    assert ev.submitter.startswith("client::") and ev.reassignment_counter == 1
    assert ev.assignment_exclusivity and ev.assignment_exclusivity > 1_700_000_000_000


def test_reassignment_assigned_matches_the_unassign():
    un = CantonUpdate.from_json_api(load("update-reassignment-unassigned.json")).events[0]
    u = CantonUpdate.from_json_api(load("update-reassignment-assigned.json"))
    (ev,) = u.events
    assert ev.type == CantonEventType.ASSIGNED
    assert ev.reassignment_id == un.reassignment_id and ev.contract_id == un.contract_id
    assert ev.source == un.source and ev.target == un.target and ev.reassignment_counter == 1
    assert u.synchronizer_id == un.target, "the assign is reported on the target synchronizer"
    assert ev.signatories and ev.payload_hash, "assigned carries the contract as created on the target"


def test_snapshot_inherits_pending_reassignments():
    snap = load("snapshot-pending-reassignment.json")
    u = CantonUpdate.snapshot_from_json_api(snap["entries"], snap["offset"])
    assert u.kind == CantonUpdateKind.SNAPSHOT and u.offset == snap["offset"]
    types = [e.type for e in u.events]
    assert types.count(CantonEventType.CREATED) == 2 and types.count(CantonEventType.UNASSIGNED) == 1
    pending = [e for e in u.events if e.type == CantonEventType.UNASSIGNED][0]
    assert pending.reassignment_id and pending.reassignment_counter == 1
    active = [e for e in u.events if e.type == CantonEventType.CREATED][0]
    assert active.source.startswith("sync1::") and active.reassignment_counter == 0


def test_round_trip_through_json_lines():
    u = CantonUpdate.from_json_api(load("update-transaction-exercised.json"))
    line = u.model_dump_json(exclude_none=True)
    back = CantonUpdate.model_validate_json(line)
    assert back == u
    assert back.events[0].stakeholders == list(dict.fromkeys(back.events[0].signatories + back.events[0].observers))
