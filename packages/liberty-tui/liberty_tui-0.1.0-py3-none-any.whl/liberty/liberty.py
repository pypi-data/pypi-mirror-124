# from logging import info
from argparse import Namespace
from dataclasses import dataclass, field
from os.path import isfile
from urwid import ExitMainLoop, Filler, Frame, Text

from .prompt import Prompt
from .file import File
from .ui import display_prompt


@dataclass
class Liberty:
    args: Namespace
    loop: "Loop" = ""
    view: Frame = Frame(Filler(Text("Initializing...")))
    file: File = File("../Liberty.md")
    prompt_index: int = 0
    prompts: list[Prompt] = field(default_factory=list)

    def __post_init__(self):
        if isfile(self.args.path):
            self.file = File(self.args.path)
            self.prompts = self.file.parse_prompts(self.args.level) or [Prompt("Nothing here yet!", 0)]
        else:
            self.prompts = [Prompt("Nothing here yet!", 0)]
        self.view = display_prompt(self)

    def handle_input(self, key: str) -> None:
        if key in ("q", "Q"):
            raise ExitMainLoop()
        view = display_prompt(self)
        self.view = view
