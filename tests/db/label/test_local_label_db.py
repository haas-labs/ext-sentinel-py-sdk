import pytest
from sentinel.db.label_db.local import LabelDB


def test_local_label_db_init():
    """
    Test Local Label DB Init
    """
    label_db = LabelDB(path="tests/db/label/resources/label_db.json")
    assert isinstance(label_db, LabelDB), "Incorrect Label DB type"


@pytest.mark.asyncio
async def test_local_label_db_add_and_search_by_address(tmpdir):
    """
    Test Local Label DB Add and Search
    """
    db_path = tmpdir / "label_db.json"
    suspicious_account_addresses = [
        "0x0bd94b3745b8bb14230887eaf12a7e2664415dfb",
        "0x0bd94b3745b8bb14230887eaf12a7e2664415dfc",
    ]

    label_db = LabelDB(path=db_path)

    for addr in suspicious_account_addresses:
        await label_db.add(
            address=addr,
            tags=["suspicious_account"],
            category="security",
        )
    search_result = await label_db.search_by_address(
        addresses=suspicious_account_addresses,
        tags=["suspicious_account"],
    )
    assert len(search_result) == 2, "Incorrect number of search result"

    founded_addresses = [rec.address for rec in search_result]
    assert founded_addresses == suspicious_account_addresses, "Incorrect suspicious account addresses"


@pytest.mark.asyncio
async def test_local_label_db_add_and_search_by_tag(tmpdir):
    """
    Test Local Label DB Add and Search By Tag
    """
    db_path = tmpdir / "label_db.json"
    suspicious_account_address = "0x0bd94b3745b8bb14230887eaf12a7e2664415dfb"

    label_db = LabelDB(path=db_path)
    await label_db.add(
        address=suspicious_account_address,
        tags=["suspicious_account"],
        category="security",
    )
    search_result = await label_db.search_by_tag(tags=["suspicious_account"])
    assert len(search_result) == 1, "Incorrect number of search result"

    suspicious_account_record = search_result[0]
    assert suspicious_account_record.address == suspicious_account_address, "Incorrect suspicious account address"


@pytest.mark.asyncio
async def test_local_label_db_stats(tmpdir):
    """
    Test Local Label DB | stats
    """
    db_path = tmpdir / "label_db.json"
    suspicious_account_address = "0x0bd94b3745b8bb14230887eaf12a7e2664415dfb"

    label_db = LabelDB(path=db_path, update_tags=["suspicious_account"])

    await label_db.add(
        address=suspicious_account_address,
        tags=["suspicious_account"],
        category="security",
    )

    assert label_db.stats == {"suspicious_account": 1}, "Incorrect label db stats"


@pytest.mark.asyncio
async def test_local_label_db_update(tmpdir):
    """
    Test Local Label DB | Update
    """
    db_path = tmpdir / "label_db.json"
    suspicious_account_address = "0x0bd94b3745b8bb14230887eaf12a7e2664415dfb"

    label_db = LabelDB(path=db_path, update_tags=["suspicious_account"])

    await label_db.add(
        address=suspicious_account_address,
        tags=["suspicious_account"],
        category="security",
    )

    await label_db.update()
    await label_db.update()

    print(label_db._addresses)

    assert not label_db.has_tag(
        suspicious_account_address, "faked_tag"
    ), "Suspicious account has faked tag in the Label DB"

    assert label_db.has_tag(
        suspicious_account_address, "suspicious_account"
    ), "Suspicious account missed in the Label DB"

    assert not label_db.has_tag("0x0123456789", "suspicious_account"), "Wrong suspicious account in the Label DB"
