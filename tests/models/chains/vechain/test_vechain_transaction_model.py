from sentinel.models.chains.vechain.transaction import VeChainTransaction


def test_vechain_transaction_model_type():
    transaction = VeChainTransaction()
    assert isinstance(transaction, VeChainTransaction), "Incorrect transaction type"
