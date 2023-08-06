from dataclasses import dataclass, field
from re import match


@dataclass
class Prompt:
    "A Prompt with title: str, file_index: int position in file, and children: list[str]."
    title: str
    file_index: int
    tab_length: int = 0
    level: int = 1
    children: list[str] = field(default_factory=list)
    correct: list = field(default_factory=list)

    def get_level(self, regex: str = r".*\[l([1-7])\](?!\((.*\))?).*") -> int:
        level = int(match(regex, self.title).group(1))
        return level

    def init_level(self) -> None:
        level = self.get_level()
        self.level = level

    def set_level(self, level_val) -> None:
        self.level = level_val

    def raise_level(self) -> None:
        self.set_level(min(self.level + 1, 7))

    def empty_level(self) -> None:
        self.set_level(1)

    def lower_level(self) -> None:
        self.set_level(max(self.level - 2, 1))

    def process(self, threshold_r, threshold_f):
        invalid = not self.file_index
        ratio = self.correct.count(True) / max(len(self.children), 1)
        if ratio > threshold_r:
            self.raise_level()
        elif threshold_f < ratio < threshold_r:
            self.lower_level()
        else:
            self.empty_level()
        if invalid:
            self.level = 0
