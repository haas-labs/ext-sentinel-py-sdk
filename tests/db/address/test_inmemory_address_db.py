from typing import List
from pydantic import BaseModel

from sentinel.db.address.memory import to_bytes
from sentinel.db.address.memory import InMemoryAddressDB


class MonitoredContract(BaseModel):
    addr: bytes


def test_in_memory_address_db_init():
    db = InMemoryAddressDB(metadata_type=MonitoredContract)
    assert isinstance(db, InMemoryAddressDB), "Incorrect db type for in-memory address db"


def test_in_memory_kv_db_manage_direct_mapping():
    addr1 = "0x61d0c37f406d1b19fbf9b5267887d67400849a7f"
    addr2 = "0x61d0c37f406d1b19fbf9b5267887d67400849a7e"

    db = InMemoryAddressDB(metadata_type=MonitoredContract)
    db.put(addr1, MonitoredContract(addr=addr1))
    db.put(to_bytes(addr1), MonitoredContract(addr=addr1))
    assert db.size == 1, "Incorrect number of record in AddressDB"
    assert db.exists(addr1), f"Unknown address, {addr1}"

    db.put(addr2, None)
    assert db.size == 2, "Incorrect number of record in AddressDB"
    db.remove(addr2)
    assert db.size == 1, "Incorrect number of record in AddressDB"

    assert db.get(address=addr1) == MonitoredContract(addr=addr1)
    assert db.all() == {to_bytes(addr1): MonitoredContract(addr=addr1)}, "Incorrect records when getting all"


def test_in_memory_kv_db_manage_address_list():
    addr1 = "0x61d0c37f406d1b19fbf9b5267887d67400849a7f"
    addr2 = "0x61d0c37f406d1b19fbf9b5267887d67400849a7e"

    db = InMemoryAddressDB(metadata_type=List[MonitoredContract])
    db.put(to_bytes(addr1), MonitoredContract(addr=addr1))
    db.put(addr1, (MonitoredContract(addr=addr1), MonitoredContract(addr=addr2)))
    assert db.size == 1, "Incorrect number of record in AddressDB"
    assert db.exists(addr1), f"Unknown address, {addr1}"

    db.put(addr2, None)
    assert db.size == 2, "Incorrect number of record in AddressDB"
    db.remove(addr2)
    assert db.size == 1, "Incorrect number of record in AddressDB"

    assert db.get(address=addr1) == (MonitoredContract(addr=addr1), MonitoredContract(addr=addr2))
    assert db.all() == {
        to_bytes(addr1): (MonitoredContract(addr=addr1), MonitoredContract(addr=addr2))
    }, "Incorrect records when getting all"
