def shorten_ethereum_address(address: str) -> str:
    # Check if the address is valid
    if not isinstance(address, str) or not address.startswith("0x"):
        raise ValueError("Invalid Ethereum address format")

    # Strip the leading '0x' and leading zeros
    shortened_address = address[2:].lstrip("0")

    # Return the address in the desired format with the '0x' prefix
    return "0x" + shortened_address
