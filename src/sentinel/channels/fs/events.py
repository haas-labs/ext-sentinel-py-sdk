from pathlib import Path

from sentinel.channels.fs.common import OutboundFileChannel


class OutboundEventsChannel(OutboundFileChannel):
    name = "events"

    def __init__(self, name: str, path: Path, mode: str = "append", buffering: bool = False, **kwargs) -> None:
        super().__init__(
            name=name,
            record_type="sentinel.models.event.Event",
            path=path,
            mode=mode,
            buffering=buffering,
            **kwargs,
        )
