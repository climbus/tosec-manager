from parser import TosecFile
from pathlib import Path
from unittest.mock import patch

import pytest

from filecopier import copy_files
from fixtures import create_tosec_file


@pytest.fixture
def grouped_files():
    return {
        "dir1": [
            create_tosec_file(filename="file1.txt", title="file1"),
            create_tosec_file(filename="file2.txt", title="file2"),
        ],
        "dir2": [create_tosec_file(filename="file3.txt", title="file3")],
    }


def test_copy_files(grouped_files: dict[str, list[TosecFile]]):
    source_path = "/mock/source"
    destination_path = "/mock/destination"

    with (
        patch("filecopier.shutil.copy") as mock_copy,
        patch("filecopier.Path.mkdir") as mock_mkdir,
        patch("filecopier.Path.exists", return_value=True),
    ):

        copy_files(grouped_files, source_path, destination_path)

        # Check if directories are created
        mock_mkdir.assert_any_call(exist_ok=True)

        # Check if files are copied
        mock_copy.assert_any_call(
            Path(source_path) / "file1.txt",
            Path(destination_path) / "dir1" / "file1.txt",
        )
        mock_copy.assert_any_call(
            Path(source_path) / "file2.txt",
            Path(destination_path) / "dir1" / "file2.txt",
        )
        mock_copy.assert_any_call(
            Path(source_path) / "file3.txt",
            Path(destination_path) / "dir2" / "file3.txt",
        )
