# Core Handler Code
# - required for async sentries
# - channels and metrics should be based on Handler

from enum import Enum


class FlowType(Enum):
    inbound = "inbound"
    outbound = "outbound"


class Handler:
    name: str = "BaseHandler"

    def __init__(self, id: str, flow_type: FlowType, name: str = None, **kwargs) -> None:
        """
        id: handler id
        flow_type: handler flow type
        name: handler name
        kwargs: additional configuration
        """
        self.id = id
        self.flow_type = flow_type
        self.name = name if name is not None else self.name
        self.config = kwargs.copy()

    def init(self) -> None: ...

    async def run(self) -> None:
        raise NotImplementedError()
