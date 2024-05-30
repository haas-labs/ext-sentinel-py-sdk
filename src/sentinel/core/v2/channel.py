from typing import Any, List

from sentinel.core.v2.handler import Handler
from sentinel.utils.imports import import_by_classpath
from sentinel.utils.logger import logger


class Channel(Handler):
    def __init__(self, name: str, record_type: str, **kwargs) -> None:
        super().__init__(name=name, **kwargs)
        _, self.record_type = import_by_classpath(record_type)


class InboundChannel(Channel):
    name = "inbound_channel"

    # Handle inbound message
    async def on_message(self, message: Any) -> None: ...


class OutboundChannel(Channel):
    name = "outbound_channel"

    # Sending a message to a channel
    async def send(self, message: Any) -> None: ...


class SentryChannels:
    def __init__(self, channel_type: str, ids: List[str], channels: List[Channel], sentry_name: str = None) -> None:
        self.sentry_name = sentry_name
        self._channels: List[str] = []

        if len(ids) > 0:
            logger.info(f"{channel_type.capitalize()} channel(-s) activation: {ids}")
        for channel in channels:
            if channel.id in ids:
                self.init(channel)

        if len(self._channels) != len(ids):
            raise RuntimeError(f"Channels mismatch, expected: {sorted(ids)}, activated: {sorted(self._channels)}")

    @property
    def channels(self):
        return self._channels

    def init(self, channel: Channel) -> None:
        try:
            ch_parameters = channel.parameters
            # Add sentry name to a channel for using inside of channel.
            # For example, to make custom group id in inbound Kafka channel
            if self.sentry_name is not None:
                ch_parameters["sentry_name"] = self.sentry_name

            logger.info(f"Initializing channel: channel id: {channel.id}, type: {channel.type}")
            _, ch_class = import_by_classpath(channel.type)
            ch_instance = ch_class(name=ch_class.name, **ch_parameters)
            setattr(self, ch_instance.name, ch_instance)
            self._channels.append(ch_instance.name)
        except AttributeError as err:
            logger.error(f"Channel initialization issue, channel: {channel.id}, error: {err}")


class SentryInputs(SentryChannels):
    def __init__(self, sentry_name: str, ids: List[str], channels: List[Channel]) -> None:
        super().__init__(sentry_name=sentry_name, channel_type="inputs", ids=ids, channels=channels)


class SentryOutputs(SentryChannels):
    def __init__(self, ids: List[str], channels: List[Channel]) -> None:
        super().__init__(channel_type="outputs", ids=ids, channels=channels)
