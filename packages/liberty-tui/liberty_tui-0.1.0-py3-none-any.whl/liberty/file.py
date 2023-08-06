from dataclasses import dataclass, field
from re import compile, match, DOTALL
from os.path import isfile
from urwid import ExitMainLoop

from .prompt import Prompt


@dataclass
class File:
    path: str
    contents: list[str] = field(default_factory=list)

    def parse_prompts(self, level: int, regex: str = r".*\[l[1-7]\](?!\((.*\))?).*") -> list[Prompt]:
        "Produces list of list of all sub-indented blocks below a parent bullet that matches *regex*."
        regexc = compile(regex)
        prompts = []
        if isfile(self.path):
            with open(self.path, "r") as pfile:
                lines = pfile.readlines()
                self.contents = lines
                for i, l in enumerate(lines):
                    if regexc.match(l):
                        tab_length = len(l) - len(l.lstrip("\t"))
                        prompt = Prompt(l[tab_length:], i, tab_length)
                        parent_ind = i + 1
                        while parent_ind < len(lines) and match(fr"^\t{{{tab_length + 1},}}.*", lines[parent_ind]):
                            prompt.children.append(lines[parent_ind][(tab_length + 1) :])
                            parent_ind += 1
                        prompt.init_level()
                        prompts.append(prompt)
        if level != 0:
            return list(filter(lambda p: p.level == level, prompts))
        else:
            return prompts

    def write_all(self, prompts: list[Prompt] = [], regex: str = r"(.*\[l)([1-7])(\](?!\((.*\))?).*)") -> None:
        if len(prompts) == 1 and not prompts[0].file_index:
            raise ExitMainLoop
        for p in prompts:
            sub_sections = match(regex, p.title, DOTALL)
            to_sub = "\t" * p.tab_length + sub_sections.group(1) + str(p.level) + sub_sections.group(3)
            self.contents[p.file_index] = to_sub
        with open(self.path, "w") as x:
            x.writelines(self.contents)
        raise ExitMainLoop
