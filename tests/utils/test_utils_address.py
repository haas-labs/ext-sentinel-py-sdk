import pytest

from sentinel.utils.address import normalize_address, shorten_ethereum_address


def test_shorten_ethereum_address_failed_transform():
    with pytest.raises(ValueError):
        shorten_ethereum_address(address="a0b86991c6218b36c1d19d4a2e9eb0ce3606eb48")


def test_shorten_ethereum_address_success_transform():
    assert (
        shorten_ethereum_address(address="0x000000000000000000000000a0b86991c6218b36c1d19d4a2e9eb0ce3606eb48")
        == "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
    ), "Incorrect shorten address"

    assert (
        shorten_ethereum_address(address="0x000000000000000a0b86991c6218b36c1d19d4a2e9eb0ce3606eb48")
        == "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
    ), "Incorrect shorten address"

    assert (
        shorten_ethereum_address(address="0x00a0b86991c6218b36c1d19d4a2e9eb0ce3606eb48")
        == "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
    ), "Incorrect shorten address"

    assert (
        shorten_ethereum_address(address="0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48")
        == "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
    ), "Incorrect shorten address"


def test_normalize_address():
    assert (
        normalize_address(address="0xA0b86991C6218b36C1d19d4a2e9EB0ce3606eb48")
        == "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
    ), "Incorrect shorten address"

    assert (
        normalize_address(address="0x000000000000000000000000a0b86991c6218b36c1d19d4a2e9eb0ce3606eb48")
        == "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
    ), "Incorrect shorten address"

    assert (
        normalize_address(address="0x000000000000000a0b86991c6218b36c1d19d4a2e9eb0ce3606eb48")
        == "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
    ), "Incorrect shorten address"

    assert (
        normalize_address(address="0x00a0b86991c6218b36c1d19d4a2e9eb0ce3606eb48")
        == "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
    ), "Incorrect shorten address"

    assert (
        normalize_address(address="0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48")
        == "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
    ), "Incorrect shorten address"

    assert (
        normalize_address(address="0x0bffdd787c83235f6f0afa0faed42061a4619b7a")
        == "0x0bffdd787c83235f6f0afa0faed42061a4619b7a"
    ), "Incorrect shorten address"


def test_normalize_address_without_0x():
    assert (
        normalize_address(address="0bffdd787c83235f6f0afa0faed42061a4619b7a")
        == "0bffdd787c83235f6f0afa0faed42061a4619b7a"
    )
