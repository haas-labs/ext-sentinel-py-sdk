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
