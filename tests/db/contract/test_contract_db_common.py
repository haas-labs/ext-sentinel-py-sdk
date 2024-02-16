from sentinel.db.contract.common import CommonContractDB


def test_common_contract_db_init():
    """
    Test Common Contract DB Init
    """
    db = CommonContractDB(network="ethereum", chain_id=1)
    assert isinstance(db, CommonContractDB), "Incorrect instance type for common contract db"
