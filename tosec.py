import shutil
from parser import Parser
from pathlib import Path

import click

from filters import get_bestchoice_filter
from grouper import get_group_by


@click.command()
@click.option("--copy-to", type=click.Path(exists=True))
@click.argument("path", type=click.Path(exists=True))
def main(path: str, copy_to: str):
    grouper = get_group_by()
    bestchoice = get_bestchoice_filter(
        formats=["tzx", "tap", "z80"], languages=["pl", "en"]
    )
    parser = Parser()

    files = [parser.parse(p.name) for p in Path(path).iterdir()]

    grouped_files = grouper(bestchoice(files))

    for dirname, group in grouped_files.items():
        print(f"{dirname} ({len(group)})")
        for game in group:
            print(f"    {game.title} {game.year} {game.publisher} {game.extension}")

    if copy_to:
        for dirname, group in grouped_files.items():
            dest = Path(copy_to) / dirname
            dest.mkdir(exist_ok=True)
            for game in group:
                print(f"Copying {game.filename} to {dest}")
                shutil.copy(Path(path) / game.filename, dest / game.filename)


if __name__ == "__main__":
    main()
