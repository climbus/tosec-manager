import shutil
from parser import Parser
from pathlib import Path
from typing import Optional

import click

from filecopier import copy_files
from filters import get_bestchoice_filter
from grouper import get_group_by


@click.command()
@click.option("--limit", type=click.INT, help="Maximum number of files per directory.")
@click.option(
    "--copy-to",
    type=click.Path(exists=True),
    help="Directory path where organized files will be copied.",
)
@click.argument(
    "path",
    type=click.Path(exists=True),
    #    help="Path to the directory containing TOSEC files to be processed.",
)
def main(path: str, copy_to: str, limit: Optional[int] = None):
    grouper = get_group_by()
    bestchoice = get_bestchoice_filter(
        formats=["tzx", "tap", "z80"], languages=["pl", "en"]
    )
    parser = Parser()

    files = [parser.parse(p.name) for p in Path(path).iterdir()]

    grouped_files = grouper(bestchoice(files), limit)

    for dirname, group in grouped_files.items():
        print(f"{dirname} ({len(group)})")
        for game in group:
            print(f"    {game.title} {game.year} {game.publisher} {game.extension}")

    copy_files(grouped_files, path, copy_to)


if __name__ == "__main__":
    main()
