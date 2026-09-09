import json
import pathlib
from unittest.mock import AsyncMock, MagicMock

import pytest

from sentinel.models.chains.canton.update import CantonUpdate
from sentinel.sentry.v2.canton import CantonUpdateDetector, hash_id

RES = pathlib.Path("tests/models/chains/canton/resources")


def _detector():
    d = CantonUpdateDetector.__new__(CantonUpdateDetector)
    d.name = "TestDetector"
    d.outputs = MagicMock()
    d.outputs.events.send = AsyncMock()
    d.outputs.webhook = None  # a Channels object without a webhook output resolves to None
    return d


def test_hash_id_is_sha256_and_none_safe():
    assert hash_id(None) is None
    h = hash_id("client::1220abc")
    assert len(h) == 64 and h == hash_id("client::1220abc") and h != hash_id("client::1220abd")


@pytest.mark.asyncio
async def test_emit_carries_the_common_fields():
    update = CantonUpdate.from_json_api(json.load((RES / "update-transaction-created.json").open()))
    d = _detector()
    ev = await d.emit("canton_test", 0.6, update, party_hash=hash_id("x"))
    d.outputs.events.send.assert_awaited_once_with(ev)
    assert ev.did == "TestDetector" and ev.category == "ALERT" and ev.type == "canton_test"
    assert ev.blockchain.network == "canton" and ev.blockchain.chain_id == "canton"
    assert ev.ts == update.record_time
    assert ev.metadata["offset"] == update.offset and ev.metadata["update_id"] == update.update_id
    assert ev.metadata["synchronizer_id"] == update.synchronizer_id
    assert ev.metadata["party_hash"] == hash_id("x")


@pytest.mark.asyncio
async def test_emit_event_category_for_informational_output():
    update = CantonUpdate.from_json_api(json.load((RES / "update-topology-added.json").open()))
    ev = await _detector().emit("canton_first_seen", 0.3, update, category="EVENT")
    assert ev.category == "EVENT"


@pytest.mark.asyncio
async def test_emit_fans_out_to_a_webhook_when_declared():
    update = CantonUpdate.from_json_api(json.load((RES / "update-transaction-created.json").open()))
    d = _detector()
    d.outputs.webhook = MagicMock()
    d.outputs.webhook.send = AsyncMock()
    ev = await d.emit("canton_test", 0.6, update)
    d.outputs.webhook.send.assert_awaited_once_with(ev)


@pytest.mark.asyncio
async def test_config_change_applies_schema_fields_and_disable_restores():
    from sentinel.models.config import Configuration
    d = _detector()
    d.parameters = {"max_stakeholders_default": 10, "severity": 0.6}
    d.logger = MagicMock()
    applied = []
    d.configure = lambda p: applied.append(dict(p))
    raw = {"id": 7, "createdAt": 1, "updatedAt": 1, "status": "ACTIVE", "name": "c", "source": "ext",
           "contract": {"id": 1, "createdAt": 1, "updatedAt": 1, "projectId": 1, "tenantId": 1, "chainUid": "canton", "name": "client party"},
           "schema": {"id": 3, "createdAt": 1, "updatedAt": 1, "status": "ACTIVE", "name": "Canton Stakeholder Anomaly", "version": "0.1.0"},
           "config": {"max_stakeholders_default": 25}}
    await d.on_config_change(Configuration(**raw))
    assert applied[-1] == {"max_stakeholders_default": 25, "severity": 0.6}
    raw["status"] = "DISABLED"
    await d.on_config_change(Configuration(**raw))
    assert applied[-1] == {"max_stakeholders_default": 10, "severity": 0.6}


@pytest.mark.asyncio
async def test_emit_carries_the_policy():
    update = CantonUpdate.from_json_api(json.load((RES / "update-transaction-created.json").open()))
    d = _detector()
    d.policy_name, d.policy_version, d.policy_config_id = "Canton Test", "0.1.0", 42
    ev = await d.emit("canton_test", 0.6, update)
    assert ev.metadata["policy"] == {"name": "Canton Test", "version": "0.1.0", "config_id": 42}


@pytest.mark.asyncio
async def test_a_republished_update_is_handled_once():
    update = CantonUpdate.from_json_api(json.load((RES / "update-transaction-created.json").open()))
    d = _detector()
    d.logger = MagicMock()
    from collections import deque
    d._recent_ids, d._recent_set = deque(maxlen=10_000), set()
    seen = []
    async def on_update(u): seen.append(u.update_id)
    d.on_update = on_update
    await d.handle_update(update)
    await d.handle_update(update)  # the adapter republished the page after a crash
    assert seen == [update.update_id]
    snapshot = CantonUpdate(kind="snapshot", offset=1)
    await d.handle_update(snapshot); await d.handle_update(snapshot)
    assert len(seen) == 3, "snapshots have no update_id and are never deduplicated"


@pytest.mark.asyncio
async def test_config_change_ignores_another_detectors_condition():
    from sentinel.models.config import Configuration
    d = _detector()
    d.parameters = {"max_stakeholders_default": 10}
    d.policy_name, d.policy_version = "Canton Stakeholder Anomaly", "0.1.1"
    d.logger = MagicMock()
    applied = []
    d.configure = lambda p: applied.append(dict(p))
    other = {"id": 8, "createdAt": 1, "updatedAt": 1, "status": "ACTIVE", "name": "c", "source": "ext",
             "contract": {"id": 1, "createdAt": 1, "updatedAt": 1, "projectId": 1, "tenantId": 1, "chainUid": "canton", "name": "x"},
             "schema": {"id": 4, "createdAt": 1, "updatedAt": 1, "status": "ACTIVE", "name": "Canton Topology Drift", "version": "0.1.1"},
             "config": {"max_stakeholders_default": 99}}
    await d.on_config_change(Configuration(**other))
    assert applied == [], "another detector's condition never reaches configure"
    mine = dict(other, schema={**other["schema"], "name": "Canton Stakeholder Anomaly"})
    await d.on_config_change(Configuration(**mine))
    assert applied == [{"max_stakeholders_default": 99}] and d.policy_config_id == 8
