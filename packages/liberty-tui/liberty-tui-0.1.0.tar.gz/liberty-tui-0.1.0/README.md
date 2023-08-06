# liberty
A spaced-repetition TUI for free-response active recall.  
Made in Python with Urwid, July 2021 to present.  
Released under the [MIT License](./LICENSE).  
Created by [Kewbish](https://github.com/kewbish).   
On PyPi: [liberty](https://pypi.org/project/liberty)  

## Demo
[![A demo of Liberty.](https://asciinema.org/a/JENe9zaofPh3ODopCTJK6AV6j.svg)](https://asciinema.org/a/JENe9zaofPh3ODopCTJK6AV6j)

## Usage
Run `python liberty.py [name of file]` to run Liberty. The file can be any text file (I suppose any file at all, but I don't think you'll get much use out of an executable) - the way prompts are specified is through the use of a `[lx]` tag, where x is a number from 1 to 7. See [this explanation of the Leitner box system](https://ncase.me/remember/) for more specifics on why this is useful.

Flags:
- `--stats`, `-s`: Print detailed prompt answer stats. Default: false.
- `--nokeys`, `-k`: Do not print keyboard commands at the bottom of the TUI. Default: false.
- `--threshold-r`, `-r`: Threshold between raising and lowering level. Specify as decimal, default: 0.8.
- `--threshold-f`, `-f`: Threshold between lowering level and setting to 0. Specify as decimal, default: 0.6.
- `--level`, `-l`: Leitner level to test. If 0, will test all levels. Default: 0.

## Installation
Run `pip install liberty` to get the latest version from PyPi.

