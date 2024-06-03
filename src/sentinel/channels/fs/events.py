from pathlib import Path

from sentinel.channels.fs.common import OutboundFileChannel
from sentinel.core.v2.channel import ChannelModel

DEFAULT_MODE = "append"


class OutboundEventsChannel(OutboundFileChannel):
    name = "events"

    def __init__(
        self, name: str, path: Path, mode: str = DEFAULT_MODE, buffering: bool = False, stop_after: int = 0, **kwargs
    ) -> None:
        super().__init__(
            name=name,
            record_type="sentinel.models.event.Event",
            path=path,
            mode=mode,
            buffering=buffering,
            stop_after=stop_after,
            **kwargs,
        )

    @classmethod
    def from_settings(cls, settings: ChannelModel, **kwargs):
        parameters = settings.parameters
        return cls(
            name=settings.name,
            path=parameters.get("path"),
            mode=parameters.get("mode", DEFAULT_MODE),
            buffering=parameters.get("buffering", False),
            stop_after=parameters.get("stop_after", 0),
            **kwargs,
        )
