from argparse import ArgumentParser, ArgumentTypeError


def decimal_float(arg) -> float:
    try:
        f = float(arg)
    except ValueError:
        raise ArgumentTypeError("Must be a floating point number between 0 and 1.")
    if f < 0 or f > 1:
        raise ArgumentTypeError("Must be a floating point number between 0 and 1.")
    return f


def leitner_level(arg) -> int:
    try:
        f = int(arg)
    except ValueError:
        raise ArgumentTypeError("Must be an integer between 0 and 7.")
    if f < 0 or f > 7:
        raise ArgumentTypeError("Must be an integer between 0 and 7.")
    return f


parser = ArgumentParser(description="Free-response spaced repetition TUI.")
parser.add_argument("path", help="Path to prompts source file.")
parser.add_argument(
    "--stats", "-s", help="Print detailed prompt answer stats. Default: false", action="store_true", default=False
)
parser.add_argument(
    "--nokeys", "-k", help="Do not print keyboard commands. Default: false", action="store_true", default=False
)
parser.add_argument(
    "--threshold-r",
    "-r",
    help="Threshold between raising and lowering level. Specify as decimal, default: 0.8",
    type=decimal_float,
    default=0.8,
)
parser.add_argument(
    "--threshold-f",
    "-f",
    help="Threshold between lowering level and setting to 0. Specify as decimal, default: 0.6",
    type=decimal_float,
    default=0.6,
)
parser.add_argument(
    "--level",
    "-l",
    help="Leitner level to test. If 0, will test all levels. Default: 0",
    type=leitner_level,
    default=0,
)
args = parser.parse_args()
