# Core Handler Code
# - required for async sentries
# - channels and metrics should be based on Handler


class Handler:
    name: str = "unspecified"

    def __init__(self, name: str = None, **kwargs) -> None:
        self.name = name if name is not None else self.name
        self.config = kwargs.copy()

    async def run(self) -> None:
        raise NotImplementedError()
