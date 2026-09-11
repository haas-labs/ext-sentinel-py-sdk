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
    assert ev.metadata["offset"] == str(update.offset) and ev.metadata["update_id"] == update.update_id
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
    assert json.loads(ev.metadata["policy"]) == {"name": "Canton Test", "version": "0.1.0", "config_id": 42}


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


def _raw_condition(cid=7, updated=1, status="ACTIVE", schema="Canton Stakeholder Anomaly", config=None, address="client::1220aa"):
    return {"id": cid, "createdAt": 1, "updatedAt": updated, "status": status, "name": "c", "source": "ATTACK_DETECTOR",
            "contract": {"id": 1, "createdAt": 1, "updatedAt": 1, "projectId": 1, "tenantId": 1, "chainUid": "canton_devnet", "name": "client party", "address": address},
            "schema": {"id": 3, "createdAt": 1, "updatedAt": 1, "status": "ACTIVE", "name": schema, "version": "0.1.1"},
            "config": config if config is not None else {"max_stakeholders_default": 25}}


class _FakeConditionsDB:
    """Stands in for RemoteMonitoringConditionsDB: keeps ACTIVE configs of one schema, like the real one."""

    def __init__(self, schema="Canton Stakeholder Anomaly"):
        from sentinel.models.config import Configuration, Status
        self._config_db, self.schema, self.ingested = {}, schema, 0
        self._Configuration, self._Status = Configuration, Status

    def ingest(self):
        self.ingested += 1

    def update(self, record):
        c = self._Configuration(**record.value)
        if c.config_schema.name != self.schema:
            return
        if c.status == self._Status.ACTIVE:
            self._config_db[c.id] = c
        else:
            self._config_db.pop(c.id, None)


def _record(raw):
    r = MagicMock()
    r.value = raw
    return r


@pytest.mark.asyncio
async def test_a_condition_record_goes_through_the_database_and_sets_the_policy():
    d = _detector()
    d.parameters = {"max_stakeholders_default": 10}
    d.logger = MagicMock()
    d.policy_name = "Canton Stakeholder Anomaly"
    applied = []
    d.configure = lambda p: applied.append(dict(p))
    d.databases = MagicMock()
    d.databases.monitoring_conditions = _FakeConditionsDB()
    await d.on_config_change(record=_record(_raw_condition(cid=7)))
    assert d.policy_config_id == 7
    assert applied[-1] == {"max_stakeholders_default": 25, "monitored_parties": ["client::1220aa"]}, "the condition's entity is a monitored party"
    await d.on_config_change(record=_record(_raw_condition(cid=7, updated=2, config={"max_stakeholders_default": 30})))
    assert applied[-1]["max_stakeholders_default"] == 30, "an updated condition is re-applied"
    await d.on_config_change(record=_record(_raw_condition(cid=9, schema="Canton Topology Drift")))
    assert d.policy_config_id == 7, "another detector's condition is filtered out by the database"
    await d.on_config_change(record=_record(_raw_condition(cid=7, updated=3, status="DISABLED")))
    assert d.policy_config_id is None and applied[-1] == {"max_stakeholders_default": 10}, "no active condition: profile defaults"


@pytest.mark.asyncio
async def test_the_alert_carries_the_condition_id_as_cid():
    update = CantonUpdate.from_json_api(json.load((RES / "update-transaction-created.json").open()))
    d = _detector()
    d.policy_name, d.policy_version = "Canton Stakeholder Anomaly", "0.1.1"
    d.parameters, d.logger, d.configure = {}, MagicMock(), lambda p: None
    from sentinel.models.config import Configuration
    d.apply_configuration(Configuration(**_raw_condition(cid=42)))
    event = await d.emit("canton_stakeholder_anomaly", 0.5, update)
    assert event.cid == 42 and json.loads(event.metadata["policy"])["config_id"] == 42
    d.restore_profile("test")
    event = await d.emit("canton_stakeholder_anomaly", 0.5, update)
    assert event.cid is None, "profile parameters: no condition to link the alert to"


def test_init_ingests_the_conditions_database_before_the_loop():
    d = _detector()
    d.parameters, d.logger, d.configure, d.policy_name = {}, MagicMock(), lambda p: None, "Canton Stakeholder Anomaly"
    d.inputs = MagicMock()
    d.databases = MagicMock()
    db = _FakeConditionsDB()
    from sentinel.models.config import Configuration
    db._config_db[5] = Configuration(**_raw_condition(cid=5))
    d.databases.monitoring_conditions = db
    # only the part of init after the SDK's own setup is under test: ingest, then the policy
    d.conditions_db().ingest()
    d.sync_policy()
    assert db.ingested == 1 and d.policy_config_id == 5


def test_init_configures_from_the_profile_then_lets_the_condition_land_on_top(monkeypatch):
    """The bug this guards: a detector that configured itself again after super().init() undid the
    condition the database had just applied, so a condition's fields never reached the running rule."""
    import sentinel.sentry.v2.canton as canton_module

    seen = []

    class Rule(CantonUpdateDetector):
        def configure(self, parameters):
            seen.append(dict(parameters))
            self.threshold = parameters.get("max_stakeholders_default")

    d = Rule.__new__(Rule)
    d.parameters, d.logger, d.policy_name = {"max_stakeholders_default": 25}, MagicMock(), "Canton Stakeholder Anomaly"
    d.policy_config_id, d.name = None, "Rule"
    d.inputs = MagicMock()
    d.inputs.updates = MagicMock()
    d.inputs.config = MagicMock()
    db = _FakeConditionsDB()
    from sentinel.models.config import Configuration
    db._config_db[9] = Configuration(**_raw_condition(cid=9, config={"max_stakeholders_default": 3}))
    d.databases = MagicMock()
    d.databases.monitoring_conditions = db
    monkeypatch.setattr(canton_module.CantonUpdateDetector.__mro__[1], "init", lambda self: None)  # the SDK's own setup is not under test

    Rule.init(d)

    assert [p.get("max_stakeholders_default") for p in seen] == [25, 3], "profile first, then the condition"
    assert d.threshold == 3 and d.policy_config_id == 9
    assert d.profile_parameters == {"max_stakeholders_default": 25}, "the profile stays the baseline a DISABLED condition restores"


@pytest.mark.asyncio
async def test_emit_metadata_is_a_map_of_strings():
    """The platform's event service reads metadata as Map<String,String> and silently drops a record
    with a list, an object or a number in it; the first Canton alert in dev vanished that way."""
    d = _detector()
    update = CantonUpdate.from_json_api(json.load((RES / "update-transaction-created.json").open()))
    await d.emit("t", 0.5, update, hashes=["a", "b"], node_id=3, ratio=0.25, flag=True, nothing=None, nested={"k": [1]})
    event = d.outputs.events.send.call_args.args[0]
    assert all(isinstance(v, str) for v in event.metadata.values()), event.metadata
    assert event.metadata["hashes"] == '["a","b"]' and event.metadata["node_id"] == "3" and event.metadata["ratio"] == "0.25"
    assert event.metadata["flag"] == "true" and "nothing" not in event.metadata
    assert event.metadata["policy"].startswith("{") and event.metadata["offset"].isdigit()


@pytest.mark.asyncio
async def test_emit_puts_the_message_and_the_update_id_where_the_platform_reads_them():
    update = CantonUpdate.from_json_api(json.load((RES / "update-transaction-created.json").open()))
    d = _detector()
    ev = await d.emit("t", 0.5, update, desc="A party saw what it should not")
    assert ev.metadata["desc"] == "A party saw what it should not", "ext-event reads the alert message from metadata.desc"
    assert ev.metadata["tx_hash"] == update.update_id, "ext-event's explorer link comes from metadata.tx_hash" 
