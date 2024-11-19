def normalize_address(address: str) -> str:
    """
    Normalize addrress
    - address must have 0x prefix
    - use lowercase
    - remove leading zeros
    """
    if address.startswith("0x"):
        return shorten_ethereum_address(address=address.lower())
    else:
        return address


def shorten_ethereum_address(address: str) -> str:
    # Check if the address is valid
    if not isinstance(address, str) or not address.startswith("0x"):
        raise ValueError("Invalid Ethereum address format")

    address_body = address[2:]
    
    if len(address_body) > 40:
        address_body = address_body.lstrip('0')

    address_body = address_body.zfill(40)

    return "0x" + address_body