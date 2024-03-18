import logging

from typing import List, Dict
from sentinel.utils.imports import import_by_classpath

logger = logging.getLogger(__name__)


class SentryChannels:
    def __init__(self, channel_type: str, aliases: List[str], settings: Dict) -> None:
        self.channels = []
        for channel in settings.get(channel_type, []):
            if channel.get("alias") in aliases:
                self._load_channel(channel)

    def _load_channel(self, channel: Dict) -> None:
        ch_alias = channel.get("alias")
        try:
            ch_type = channel.get("type")
            ch_parameters = channel.get("parameters")
            logger.info(f"Initializing channel: {ch_alias}, type: {ch_type}")
            _, ch_class = import_by_classpath(channel.get("type"))
            ch_instance = ch_class(name=ch_class.name, **ch_parameters)
            setattr(self, ch_instance.name, ch_instance)
        except AttributeError as err:
            logger.error(f"{ch_alias} -> Channel initialization issue, {err}")


class SentryInputs(SentryChannels):
    def __init__(self, aliases: List[str], settings: Dict) -> None:
        super().__init__("inputs", aliases, settings)

class SentryOutputs(SentryChannels):
    def __init__(self, aliases: List[str], settings: Dict) -> None:
        super().__init__("outputs", aliases, settings)
