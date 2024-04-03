from pathlib import Path

from sentinel.channels.fs.common import OutboundFileChannel


class OutboundEventsChannel(OutboundFileChannel):
    name = "events"

    def __init__(self, path: Path, mode: str = "append", buffering: bool = False, **kwargs) -> None:
        super().__init__(
            name=self.name,
            record_type="sentinel.models.event.Event",
            path=path,
            mode=mode,
            buffering=buffering,
            **kwargs,
        )
