class SuspiciousAccountDB:
    name = "suspicious_account"

    def __init__(self) -> None:
        """
        Account DB Init
        """
        # The list of suspicios accounts
        self._db = []

    def add(self, address: str) -> None:
        """
        add address to suspicious accounts
        """
        self._db.append(address)

    def is_suspicios(self, address: str) -> bool:
        """
        returns True if address is suspicious
        """
        if address in self._db:
            return True
        else:
            return False

    def pull_changes(self, remote_uri: str) -> None:
        """
        Pull changes to remote DB
        """
        raise NotImplementedError

    def push_changes(self, remote_uri: str) -> None:
        """
        Push changes to remote DB
        """
        raise NotImplementedError
