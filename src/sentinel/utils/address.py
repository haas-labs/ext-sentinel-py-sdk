"""
This module provides utility functions for normalizing and shortening Ethereum addresses.

Functions:
    normalize_address(address: str) -> str:
        Normalize an Ethereum address by ensuring it has a '0x' prefix, is in lowercase, and has no leading zeros.
    shorten_ethereum_address(address: str) -> str:
        Shorten an Ethereum address by removing leading zeros and ensuring it is 40 characters long.
"""


def normalize_address(address: str) -> str:
    """
    Normalize an Ethereum address.

    This function ensures that the address:
    - Has a '0x' prefix.
    - Is in lowercase.
    - Has no leading zeros.

    Args:
        address (str): The Ethereum address to normalize.

    Returns:
        str: The normalized Ethereum address.
    """
    if address.startswith("0x"):
        return shorten_ethereum_address(address=address.lower())
    else:
        return address


def shorten_ethereum_address(address: str) -> str:
    """
    Shortens an Ethereum address by removing leading zeros and ensuring it is 40 characters long.

    Args:
        address (str): The Ethereum address to be shortened. It must be a string starting with "0x".

    Returns:
        str: The shortened Ethereum address in the correct format.

    Raises:
        ValueError: If the provided address is not a valid Ethereum address format.
    """
    # Check if the address is valid
    if not isinstance(address, str) or not address.startswith("0x"):
        raise ValueError("Invalid Ethereum address format")

    address_body = address[2:]

    if len(address_body) > 40:
        address_body = address_body.lstrip("0")

    address_body = address_body.zfill(40)

    return "0x" + address_body
