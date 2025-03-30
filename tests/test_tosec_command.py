from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

from tosec import main


@pytest.fixture
def cli_runner():
    return CliRunner()


def test_main_no_limit(cli_runner: CliRunner, tmp_path: Path):
    with (
        patch("tosec.get_group_by") as mock_grouper,
        patch("tosec.get_bestchoice_filter") as mock_bestchoice,
        patch("tosec.Parser") as mock_parser,
        patch("tosec.copy_files") as mock_copy_files,
    ):

        mock_grouper.return_value = lambda files, limit: {"dir1": files}  # type: ignore
        mock_bestchoice.return_value = lambda files: files  # type: ignore
        mock_parser_instance = mock_parser.return_value
        mock_parser_instance.parse.return_value = MagicMock()

        source_dir = tmp_path / "source"
        destination_dir = tmp_path / "destination"
        source_dir.mkdir()
        destination_dir.mkdir()

        result = cli_runner.invoke(
            main, ["--copy-to", str(destination_dir), str(source_dir)]
        )

        assert result.exit_code == 0
        mock_copy_files.assert_called_once()


def test_main_with_limit(cli_runner: CliRunner, tmp_path: Path):
    with (
        patch("tosec.get_group_by") as mock_grouper,
        patch("tosec.get_bestchoice_filter") as mock_bestchoice,
        patch("tosec.Parser") as mock_parser,
        patch("tosec.copy_files") as mock_copy_files,
    ):

        mock_grouper.return_value = lambda files, limit: {"dir1": files[:limit]}  # type: ignore
        mock_bestchoice.return_value = lambda files: files  # type: ignore
        mock_parser_instance = mock_parser.return_value
        mock_parser_instance.parse.return_value = MagicMock()

        source_dir = tmp_path / "source"
        destination_dir = tmp_path / "destination"
        source_dir.mkdir()
        destination_dir.mkdir()

        result = cli_runner.invoke(
            main, ["--copy-to", str(destination_dir), "--limit", "1", str(source_dir)]
        )

        assert result.exit_code == 0
        mock_copy_files.assert_called_once()
