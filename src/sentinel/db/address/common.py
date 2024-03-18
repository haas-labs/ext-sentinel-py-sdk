from sentinel.models.address import AddressType


class CommonAddressDB:
    name = "address"

    def __init__(self) -> None:
        """
        Common Address DB Init
        """
        self._accounts = list()
        self._contracts = list()

    async def check(self, address: str) -> AddressType:
        """
        check address: account/contract
        """
        address = address.strip()
        if address in self._accounts:
            return AddressType.account

        if address in self._contracts:
            return AddressType.contract

        match await self._fetch(address=address):
            case AddressType.account:
                self._accounts.append(address)
                return AddressType.account
            case AddressType.contract:
                self._contracts.append(address)
                return AddressType.contract
            case _:
                return AddressType.undefined
