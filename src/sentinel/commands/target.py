from argparse import ArgumentParser, Namespace
from typing import List

from sentinel.commands.common import SentinelCommand


class Command(SentinelCommand):
    def description(self) -> str:
        return "Managing Monitoring Targets"

    def add_options(self, parser: ArgumentParser) -> None:
        super().add_options(parser)

    def run(self, opts: List[str], args: Namespace) -> None:
        super().run(opts, args)
