from argparse import Namespace
from dataclasses import dataclass, field
from urwid import (
    MainLoop,
)

from .liberty import Liberty


@dataclass
class Controller:
    args: Namespace = field(default_factory=Namespace)

    def __post_init__(self):
        liberty = Liberty(self.args)
        loop = MainLoop(liberty.view, unhandled_input=liberty.handle_input)
        liberty.loop = loop
        loop.run()
