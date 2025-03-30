import shutil
from parser import TosecFile
from pathlib import Path
from typing import Dict, List


def copy_files(
    grouped_files: Dict[str, List[TosecFile]], source_path: str, destination_path: str
):
    """
    Copy files to the specified destination directory.

    :param grouped_files: Dictionary with directory names as keys and lists of files as values.
    :param source_path: Path to the source directory containing the files.
    :param destination_path: Path to the destination directory where files will be copied.
    """
    for dirname, group in grouped_files.items():
        dest = Path(destination_path) / dirname
        dest.mkdir(exist_ok=True)
        for game in group:
            print(f"Copying {game.filename} to {dest}")
            shutil.copy(Path(source_path) / game.filename, dest / game.filename)
