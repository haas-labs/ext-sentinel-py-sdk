from typing import List

from sentinel.models.channel import Channel

from sentinel.utils.logger import get_logger
from sentinel.utils.imports import import_by_classpath


class SentryChannels:
    def __init__(self, channel_type: str, ids: List[str], channels: List[Channel], sentry_name: str = None) -> None:
        self.logger = get_logger(__name__)

        self.sentry_name = sentry_name
        self._channels: List[str] = []

        self.logger.info(f"Channel(-s) activation: {ids}")
        for channel in channels:
            if channel.id in ids:
                self._load_channel(channel)

        if len(self._channels) != len(ids):
            raise RuntimeError(f"Channels mismatch, expected: {sorted(ids)}, activated: {sorted(self._channels)}")

    @property
    def channels(self):
        return self._channels

    def _load_channel(self, channel: Channel) -> None:
        try:
            ch_parameters = channel.parameters
            # Add sentry name to a channel for using inside of channel.
            # For example, to make custom group id in inbound Kafka channel
            if self.sentry_name is not None:
                ch_parameters["sentry_name"] = self.sentry_name

            self.logger.info(f"Initializing channel: channel id: {channel.id}, type: {channel.type}")
            _, ch_class = import_by_classpath(channel.type)
            ch_instance = ch_class(name=ch_class.name, **ch_parameters)
            setattr(self, ch_instance.name, ch_instance)
            self._channels.append(ch_instance.name)
        except AttributeError as err:
            self.logger.error(f"Channel initialization issue, channel: {channel.id}, error: {err}")


class SentryInputs(SentryChannels):
    def __init__(self, sentry_name: str, ids: List[str], channels: List[Channel]) -> None:
        super().__init__(sentry_name=sentry_name, channel_type="inputs", ids=ids, channels=channels)


class SentryOutputs(SentryChannels):
    def __init__(self, ids: List[str], channels: List[Channel]) -> None:
        super().__init__(channel_type="outputs", ids=ids, channels=channels)
