from pathlib import Path

from sentinel.channels.fs.common import InboundFileChannel
from sentinel.core.v2.channel import ChannelModel
from sentinel.models.chains.canton.update import CantonUpdate


class InboundCantonUpdatesChannel(InboundFileChannel):
    """
    Reads CantonUpdate records from a JSON-lines file, one update per line. Used by local profiles
    and fixtures so Canton sentries can run without a participant node or Kafka.
    """

    name = "updates"

    def __init__(self, name: str, path: Path, **kwargs) -> None:
        super().__init__(name=name, record_type="sentinel.models.chains.canton.update.CantonUpdate", path=path, **kwargs)

    @classmethod
    def from_settings(cls, settings: ChannelModel, **kwargs):
        return cls(
            name=settings.name,
            path=settings.parameters.get("path"),
            time_interval=settings.parameters.get("time_interval", 0),
            **kwargs,
        )

    async def on_message(self, message: CantonUpdate) -> None:
        await self.on_update(message)

    async def on_update(self, update: CantonUpdate) -> None: ...
