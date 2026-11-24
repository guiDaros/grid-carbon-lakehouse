from importlib.metadata import version

from typer.testing import CliRunner

from gridcarbon import __version__
from gridcarbon.cli import app

runner = CliRunner()


def test_version_matches_package_metadata() -> None:
    assert __version__ == version("gridcarbon")


def test_version_flag_prints_version_and_exits_zero() -> None:
    result = runner.invoke(app, ["--version"])

    assert result.exit_code == 0
    assert result.output.strip() == f"gridcarbon {__version__}"


def test_help_exits_zero() -> None:
    result = runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "--version" in result.output
