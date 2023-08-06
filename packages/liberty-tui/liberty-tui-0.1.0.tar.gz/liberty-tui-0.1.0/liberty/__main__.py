from logging import basicConfig, INFO

from .args import args
from .controller import Controller


def main():
    basicConfig(level=INFO, filename="liberty.log", filemode="w")
    _ = Controller(args=args)
