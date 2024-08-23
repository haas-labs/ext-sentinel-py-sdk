from sentinel.db.contract.abi.standard import StandardABISignatures


def test_abi_signatures_standard_init():
    """
    Test | Standard ABI Signatures | Init
    """
    abi_signatures = StandardABISignatures()
    assert isinstance(abi_signatures, StandardABISignatures), "Incorrect ABI Signature type"

    abi_signatures = StandardABISignatures(
        standards=[
            "ERC20",
        ]
    )
    assert isinstance(abi_signatures, StandardABISignatures), "Incorrect ABI Signature type"

    abi_signatures = StandardABISignatures(standards=["ERC20", "ERC721"])
    assert isinstance(abi_signatures, StandardABISignatures), "Incorrect ABI Signature type"


def test_abi_signatures_standard_erc20():
    """
    Test | Standard ABI Signatures | Load ERC20 Signatures
    """
    abi_signatures = StandardABISignatures(standards=["ERC20"])
    assert isinstance(abi_signatures, StandardABISignatures), "Incorrect ABI Signature type"

    assert abi_signatures.total_records == 12, "Incorrect number of total records for ERC 20"


def test_abi_signatures_standard_erc721():
    """
    Test | Standard ABI Signatures | Load ERC721 Signatures
    """
    abi_signatures = StandardABISignatures(standards=["ERC721"])
    assert isinstance(abi_signatures, StandardABISignatures), "Incorrect ABI Signature type"

    assert abi_signatures.total_records == 17, "Incorrect number of total records for ERC 721"


def test_abi_signatures_standard_erc1155():
    """
    Test | Standard ABI Signatures | Load ERC1155 Signatures
    """
    abi_signatures = StandardABISignatures(standards=["ERC1155"])
    assert isinstance(abi_signatures, StandardABISignatures), "Incorrect ABI Signature type"

    assert abi_signatures.total_records == 12, "Incorrect number of total records for ERC 1155"


def test_abi_signatures_standard_transparent_proxy():
    """
    Test | Standard ABI Signatures | Load Transparent Proxy Signatures
    """
    abi_signatures = StandardABISignatures(standards=["TransparentProxy"])
    assert isinstance(abi_signatures, StandardABISignatures), "Incorrect ABI Signature type"

    assert abi_signatures.total_records == 11, "Incorrect number of total records for Transparent Proxy"


def test_abi_signatures_standard_all():
    """
    Test | Standard ABI Signatures | Load all standard signatures
    """
    abi_signatures = StandardABISignatures(standards=["ERC20", "ERC721", "ERC1155", "TransparentProxy"])
    assert isinstance(abi_signatures, StandardABISignatures), "Incorrect ABI Signature type"

    assert abi_signatures.total_records == 52, "Incorrect number of total records for all standard signatures"


def test_abi_signatures_standard_unknown_standard():
    """
    Test | Standard ABI Signatures | Load all unknown standard
    """
    abi_signatures = StandardABISignatures(
        standards=[
            "ERC21",
        ]
    )
    assert isinstance(abi_signatures, StandardABISignatures), "Incorrect ABI Signature type"

    assert abi_signatures.total_records == 0, "Incorrect number of total records for all standard signatures"


def test_abi_signatures_standard_search():
    """
    Test | Standard ABI Signatures | Search
    """
    abi_signatures = StandardABISignatures(standards=["ERC20", "ERC721", "ERC1155"])

    assert len(list(abi_signatures.search(standard="ERC20"))) == 12, "Incorrect number of signatures for ERC 20"

    assert (
        len(list(abi_signatures.search(signature_type="event"))) == 9
    ), "Incorrect number of signatures for type = event"

    assert (
        len(list(abi_signatures.search(signature_type="function"))) == 31
    ), "Incorrect number of signatures for type = function"

    assert (
        len(list(abi_signatures.search(standard="ERC20", signature_type="event"))) == 2
    ), "Incorrect number of signatures for ERC 20 and type = event"

    assert (
        len(list(abi_signatures.search(standard="ERC20", signature_type="function"))) == 9
    ), "Incorrect number of signatures for ERC 20 and type = function"

    assert (
        len(list(abi_signatures.search(standard="ERC721", signature_type="event"))) == 3
    ), "Incorrect number of signatures for ERC 721 and type = event"

    assert (
        len(list(abi_signatures.search(standard="ERC721", signature_type="function"))) == 14
    ), "Incorrect number of signatures for ERC 721 and type = function"

    assert (
        len(list(abi_signatures.search(standard="ERC1155", signature_type="event"))) == 4
    ), "Incorrect number of signatures for ERC 1155 and type = event"

    assert (
        len(list(abi_signatures.search(standard="ERC1155", signature_type="function"))) == 8
    ), "Incorrect number of signatures for ERC 1155 and type = function"
