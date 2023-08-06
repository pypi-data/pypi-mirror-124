from setuptools import setup
from liberty import version

from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="liberty-tui",
    version=version,
    author="Emilie Ma (kewbish)",
    author_email="kewbish@gmail.com",
    url="https://github.com/kewbish/liberty",
    description="A spaced-repetition TUI for free-response active recall.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT License",
    entry_points={
        "console_scripts": [
            "liberty = liberty.__main__:main",
        ]
    },
    packages=["liberty"],
    install_requires=["urwid"],
    python_requires=">=3",
    classifiers=[
        "Development Status :: 1 - Planning",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
)
