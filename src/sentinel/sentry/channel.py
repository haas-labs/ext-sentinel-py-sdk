import logging

from typing import List
from sentinel.models.channel import Channel
from sentinel.utils.imports import import_by_classpath

logger = logging.getLogger(__name__)


class SentryChannels:
    def __init__(self, channel_type: str, ids: List[str], channels: List[Channel]) -> None:
        self._channels: List[str] = []
        for channel in channels:
            if channel.id in ids:
                self._load_channel(channel)

    @property
    def channels(self):
        return self._channels

    def _load_channel(self, channel: Channel) -> None:
        try:
            ch_parameters = channel.parameters
            logger.info(f"Initializing channel: channel id: {channel.id}, type: {channel.type}")
            _, ch_class = import_by_classpath(channel.type)
            ch_instance = ch_class(name=ch_class.name, **ch_parameters)
            setattr(self, ch_instance.name, ch_instance)
            self._channels.append(ch_instance.name)
        except AttributeError as err:
            logger.error(f"Channel initialization issue, channel: {channel.id}, error: {err}")


class SentryInputs(SentryChannels):
    def __init__(self, ids: List[str], channels: List[Channel]) -> None:
        super().__init__("inputs", ids, channels)


class SentryOutputs(SentryChannels):
    def __init__(self, ids: List[str], channels: List[Channel]) -> None:
        super().__init__("outputs", ids, channels)
