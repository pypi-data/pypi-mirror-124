# from logging import info
from urwid import (
    BoxAdapter,
    CheckBox,
    Columns,
    Divider,
    Edit,
    Filler,
    Frame,
    LineBox,
    ListBox,
    Padding,
    Pile,
    SimpleListWalker,
    Text,
)


class MultiLineCont(LineBox):
    def __init__(self, widget, liberty):
        LineBox.__init__(self, widget)
        self.liberty = liberty

    def keypress(self, size, key):
        if key != "meta enter":
            return super(MultiLineCont, self).keypress(size, key)
        self.liberty.loop.widget = display_side(self.liberty, self.original_widget.contents[2][0].edit_text)


class CheckBoxVim(LineBox):
    def __init__(self, widget, liberty, title):
        LineBox.__init__(self, widget, title)
        self.liberty = liberty

    def keypress(self, size, key):
        if key != "meta enter":
            return super(CheckBoxVim, self).keypress(
                size,
                "up" if key in ("k", "up") else "down" if key in ("j", "down") else key,
            )
        liberty = self.liberty
        prompt = liberty.prompts[liberty.prompt_index]
        prompt.correct = [cb[0].get_state() for cb in self.original_widget.contents]
        if list(filter(lambda p: not p.correct, liberty.prompts)) == []:
            liberty.loop.widget = display_final(liberty)
        elif liberty.prompt_index != len(liberty.prompts) - 1:
            liberty.prompt_index += 1
            liberty.loop.widget = display_prompt(liberty)
        else:  # at end of prompts
            liberty.loop.widget = display_final(liberty)


class FinalFiller(Filler):
    def __init__(self, widget, liberty):
        Filler.__init__(self, widget)
        self.liberty = liberty

    def keypress(self, size, key):
        if key not in ("W", "w"):
            return super(FinalFiller, self).keypress(size, key)
        self.liberty.file.write_all(self.liberty.prompts)


def display_prompt(liberty) -> Frame:
    main_panel = Frame(
        Filler(
            Padding(
                MultiLineCont(
                    Pile(
                        [
                            Text(
                                liberty.prompts[liberty.prompt_index].title.rstrip()
                                + f" ({liberty.prompt_index + 1} / {len(liberty.prompts)})"
                            ),
                            Divider("─"),
                            Edit(align="left", multiline=True),
                        ]
                    ),
                    liberty,
                ),
                width=("relative", 40),
                align="center",
            )
        ),
        footer=(Text("(Alt-Enter to proceed)") if not liberty.args.nokeys else None),
    )
    return main_panel


def display_side(liberty, text: str) -> Frame:
    children = [c.replace("\t", "    ").rstrip() for c in liberty.prompts[liberty.prompt_index].children]
    main_panel = Frame(
        Filler(
            Padding(
                Pile(
                    [
                        Text(
                            liberty.prompts[liberty.prompt_index].title.rstrip()
                            + f" ({liberty.prompt_index + 1} / {len(liberty.prompts)})",
                            align="center",
                        ),
                        Columns(
                            [
                                LineBox(
                                    Text(text),
                                    title="Your Response",
                                ),
                                CheckBoxVim(
                                    Pile(
                                        [CheckBox(c) for c in children]
                                        if children
                                        else [CheckBox("Correctly recalled?")]
                                    ),
                                    liberty,
                                    title="Prompt Definition",
                                ),
                            ]
                        ),
                    ]
                ),
                width=("relative", 80),
                align="center",
            )
        ),
        footer=(
            Text("(J / Up to move down, K / Down to move up, Space / Enter to select, Alt-Enter to proceed, Q to quit)")
            if not liberty.args.nokeys
            else None
        ),
    )
    return main_panel


def display_final(liberty) -> Frame:
    def process_prompt(liberty: "Liberty", prompt: "Prompt") -> list:
        prompt.process(liberty.args.threshold_r, liberty.args.threshold_f)
        p = prompt
        prompt_box = []
        prompt_box += [
            Text(
                p.title.rstrip()
                + f" -> [l{p.level}]"
                + (
                    f" ({p.correct.count(True)} / {max(len(p.children), 1)} - {p.correct.count(True) / max(len(p.children), 1) * 100:.1f}%)"
                    if liberty.args.stats
                    else ""
                )
            ),
            Divider("─"),
        ]
        has_correct = any(p.correct)
        has_missing = not (any(p.correct) and all(p.correct))
        if p.children and has_correct:
            prompt_box += [Text("Correct:")]
            prompt_box += [
                Pile([Text(subp.replace("\t", "    ").rstrip()) for i, subp in enumerate(p.children) if p.correct[i]])
            ]
        if p.children and has_missing:
            prompt_box += [Text("Missing:")]
            prompt_box += [
                Pile(
                    [Text(subp.replace("\t", "    ").rstrip()) for i, subp in enumerate(p.children) if not p.correct[i]]
                )
            ]
        if not p.file_index:
            pass
        elif not p.children and has_correct:
            prompt_box += [Text("Correctly recalled.")]
        elif not p.children and has_missing:
            prompt_box += [Text("Incorrectly recalled.")]
        return prompt_box

    prompt_boxes = []
    for p in liberty.prompts:
        prompt_boxes += [Pile(process_prompt(liberty, p))]

    total_children = sum(map(lambda p: max(len(p.children), 1), liberty.prompts))
    total_correct = sum(map(lambda p: p.correct.count(True), liberty.prompts))
    main_panel = Frame(
        FinalFiller(
            Padding(
                Pile(
                    [
                        Text(
                            "Overview"
                            + (
                                f" ({total_correct} / {total_children} – {(total_correct / total_children * 100):.1f}%)"
                                if liberty.args.stats
                                else ""
                            ),
                            align="center",
                        ),
                        BoxAdapter(
                            ListBox(SimpleListWalker([LineBox(p) for p in prompt_boxes])),
                            height=30,
                        ),
                    ]
                ),
                width=("relative", 60),
                align="center",
            ),
            liberty,
        ),
        footer=(Text("(W to update levels, Q to quit without writing)") if not liberty.args.nokeys else None),
    )
    return main_panel
